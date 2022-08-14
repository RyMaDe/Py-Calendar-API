from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import RegisterUserSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import serializers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from django.views import View
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from rest_framework.renderers import TemplateHTMLRenderer
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .serializers import loginSerializer
from .forms import UpdateUserForm, UpdateUserPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin


class CustomUserCreate(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=RegisterUserSerializer,
        responses={
            201: "CREATED",
            400: "Bad Request",
        }
    )
    def post(self, request):
        reg_serializer = RegisterUserSerializer(data=request.data)
        if reg_serializer.is_valid():
            newuser = reg_serializer.save()
            if newuser:
                return Response(status=status.HTTP_201_CREATED)
        return Response(reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserCreateSite(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "signup.html"

    def get(self, request):
        serializer = RegisterUserSerializer()
        return Response({"serializer": serializer})

    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            newuser = serializer.save()
            if newuser:
                return redirect(reverse("users:Login_user"))
        return Response({"serializer": serializer})


class LoginUserSite(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "login.html"

    def get(self, request):
        serializer = loginSerializer()
        return Response({"serializer": serializer})

    def post(self, request):
        serializer = loginSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect(reverse("CalendarSite:calendarSite"))

        return Response({"serializer": serializer})


class LogoutUserSite(LoginRequiredMixin, View):
    login_url = reverse_lazy("users:Login_user")
    redirect_field_name = None

    def get(self, request):
        logout(request)
        return redirect(reverse("users:Login_user"))


class UpdateUserDetails(LoginRequiredMixin, View):
    login_url = reverse_lazy("users:Login_user")
    redirect_field_name = None
    template_name = "settings.html"

    def get(self, request):
        user = self.request.user
        form = UpdateUserForm(instance=user)
        return render(request, self.template_name, {"form":form})

    def post(self, request):
        user = self.request.user
        form = UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            newuser = form.save()
            if newuser:
                return redirect(reverse("CalendarSite:calendarSite"))
        return render(request, self.template_name, {"form":form})


class UpdateUserPassword(LoginRequiredMixin, View):
    login_url = reverse_lazy("users:Login_user")
    redirect_field_name = None
    template_name = "settings_password.html"

    def get(self, request):
        form = UpdateUserPasswordForm()
        return render(request, self.template_name, {"form":form})

    def post(self, request):
        user = self.request.user
        form = UpdateUserPasswordForm(request.POST, instance=user)
        if form.is_valid():
            newuser = form.save()
            update_session_auth_hash(request, user)
            if newuser:
                return redirect(reverse("CalendarSite:calendarSite"))
        form = UpdateUserPasswordForm()
        return render(request, self.template_name, {"form":form})


class DeleteUser(LoginRequiredMixin, View):
    login_url = reverse_lazy("users:Login_user")
    redirect_field_name = None
    template_name = "settings_delete.html"

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        user = self.request.user
        user.delete()
        return redirect(reverse("users:Login_user"))


# The below classes have been added for the drf-yasg integration with SimpleJWT
# so that the info pulls through correctly in the schema/documentation.
class TokenObtainPairResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class DecoratedTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenObtainPairResponseSerializer,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class DecoratedTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenRefreshResponseSerializer,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
