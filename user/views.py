from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from django.shortcuts import render, redirect, HttpResponseRedirect 
from django.contrib.auth.hashers import check_password, make_password 
from rest_framework_simplejwt.views import TokenObtainPairView
from . import models, serializers
from django.views import View 


class RegisterView(generics.CreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserWriteSerializer
    authentication_classes = []


class LoginView(TokenObtainPairView):
    authentication_classes = []
    serializer_class = serializers.LoginSerializer


class UserVerifyView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.UserReadSerializer

    def get(self, request):
        data = self.get_serializer(request.user).data
        return Response(data, status=200)

# class GoogleSocialAuthView(generics.GenericAPIView):
#     authentication_classes = []
#     serializer_class = GoogleSocialAuthSerializer

#     def post(self, request):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user_data = serializer.validated_data["auth_token"]
#         data = register_or_login_social_user(**user_data)
#         return Response(data, status=200)