import os
from django.contrib.auth import get_user_model, password_validation
from core.serializers import DynamicFieldsModelSerializer

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from . import google

class UserWriteSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "pk",
            "email",
            "password",
            "is_verified",
        ]
        read_only_fields = [
            "is_verified",
        ]

class UserReadSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "pk",
            "username",
            "full_name",
            "phone",
            "email",
            "gender",
            "is_verified",
            "is_complete",
        ]


# class LoginSerializer(TokenObtainPairSerializer):
#     def validate(self, data):
#         tokens = super().validate(data)
#         data = UserReadSerializer(self.user, context=self.context).data
#         data.update({"tokens": tokens})
#         return data


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