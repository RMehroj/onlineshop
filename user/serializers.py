import os
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.hashers import check_password
from django.db import transaction
from django.template.loader import render_to_string
from django.utils import timezone

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from core.serializers import DynamicFieldsModelSerializer
from onlineshop.task import send_email, send_html_email
from . import google
from . import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "pk",
            "username",
            "full_name",
            "email",
            "role",
            "password",
            "company",
            "is_verified",
        ]

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company
        fields = ("pk", "name")

    def update(self, instance, validated_data):
        if not validated_data.get("name"):
            validated_data["name"] = instance.owner.email.split("@")[0]
        return super().update(instance, validated_data)

class UserWriteSerializer(DynamicFieldsModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    company = CompanySerializer(required=False)
    role = serializers.ChoiceField(
        choices=[
            ("owner", "Owner"),
        ]
    )
    class Meta:
        model = get_user_model()
        fields = [
            "pk",
            "username",
            "full_name",
            "email",
            "role",
            "password",
            "company",
            "is_verified",
        ]
        read_only_fields = [
            "is_verified",
        ]

    def create(self, validated_data, company=None):
        with transaction.atomic():
            validated_data.setdefault("auth_provider", "email")
            if validated_data["role"] == "owner":
                company = models.Company.objects.create(**validated_data.pop("company"))
            user = get_user_model().objects.create_user(
                **validated_data, company=company
            )
            payload = {
                "user_id": user.pk.__str__(),
                "exp": timezone.localtime(timezone.now()) + timezone.timedelta(hours=1),
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
            url = f"http://127.0.0.1:8000/verify?auth={token}"
            html_message = render_to_string(
                "user/email_confirmation.html",
                context={"url": url},
            )
            send_html_email.delay("Verify your email", html_message, [user.email])
            return user

    def update(self, instance, validated_data):
        if company_data := validated_data.pop("company", None):
            serializer = CompanySerializer(instance.company, data=company_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return super().update(instance, validated_data)

    def validate(self, data):
        if not data.get("company") and data.get("role") == "owner":
            raise serializers.ValidationError(
                detail={"company": "This field is required."}
            )
        return data
    
class UserReadSerializer(DynamicFieldsModelSerializer):
    company = CompanySerializer(read_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            "pk",
            "name",
            "last_name",
            "email",
            "role",
            "company",
            "position",
            "profile_image",
            "is_verified",
        ]


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, data):
        tokens = super().validate(data)
        data = UserReadSerializer(self.user, context=self.context).data
        data.update({"tokens": tokens})
        return data


# class GoogleSocialAuthSerializer(serializers.Serializer):
#     auth_token = serializers.CharField(write_only=True, allow_blank=False)

#     @staticmethod
#     def map_user_data(data: dict):
#         user_data = dict(
#             social_media_id=data["sub"],
#             email=data["email"],
#             first_name=data["given_name"],
#             last_name=data["family_name"],
#             provider="google",
#         )
#         return user_data

#     def validate_auth_token(self, auth_token):
#         user_data = google.Google.validate(auth_token)
#         try:
#             user_data["sub"]
#         except Exception:
#             raise serializers.ValidationError(
#                 detail={"error": "The token is invalid or expired"}
#             )
#         if user_data["aud"] != os.environ.get("GOOGLE_CLIENT_ID"):
#             raise AuthenticationFailed(
#                 detail={"error": "Your Google client id is invalid."}
#             )
#         return self.map_user_data(user_data)