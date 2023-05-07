from typing import OrderedDict
from django.contrib.auth import login
from rest_framework import response
from rest_framework.generics import CreateAPIView, ListAPIView
from helper import helper
from .serializers import AdminLoginSerializer, UserLoginSerializer, UserSignupSerializer, authenticate
from .models import User


# Admin Login
# post
# /v1/auth/admin-login
class AdminLogin(CreateAPIView):
    serializer_class = AdminLoginSerializer

    def post(self, request):
        helper.checkParams(request, ["username", "password"])
        helper.verify_recaptcha(request)

        user = self.get_serializer(data=request.data)
        user.is_valid(raise_exception=True)
        user = user.validated_data

        return helper.createResponse(
            helper.message.LOGIN_SUCCESS,
            {
                "username": user.username,
                "email": user.email,
                "token": helper.get_token(user),
            },
        )


# User Signup
# post
# /v1/auth/signup
class Signup(CreateAPIView):
    serializer_class = UserSignupSerializer

    def post(self, request):
        helper.checkParams(
            request, ["username", "email", "password"])
        helper.verify_recaptcha(request)

        # checking if username already present
        if User.objects.filter(username=request.data["username"]).count() > 0:
            raise helper.exception.NotAcceptable(
                helper.message.USER_NAME_EXISTS)

        # checking if email already present
        if User.objects.filter(email=request.data["email"]).count() > 0:
            raise helper.exception.NotAcceptable(
                helper.message.USER_EMAIL_EXISTS)

        # check password length
        if len(request.data["password"]) < 8:
            raise helper.exception.ParseError(helper.message.PASSWORD_LENGTH)

        user = self.get_serializer(data=request.data)
        user.is_valid(raise_exception=True)
        user.save()

        user = User.objects.get(email=request.data['email'])

        return helper.createResponse(
            helper.message.SIGNUP_USER_SUCCESS,
            {
                "username": user.username,
                "email": user.email,
                "token": helper.get_token(user),
            },
        )

        # return helper.createResponse(helper.message.SIGNUP_USER_SUCCESS, status_code=422)


# User Login
# post
# /v1/auth/login
class Login(CreateAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        helper.checkParams(request, ["username", "password"])
        helper.verify_recaptcha(request)

        user = self.get_serializer(data=request.data)
        user.is_valid(raise_exception=True)
        user = user.validated_data

        return helper.createResponse(
            helper.message.LOGIN_SUCCESS,
            {
                "username": user.username,
                "email": user.email,
                "token": helper.get_token(user),
            },
        )


# Confirm Email / 2FA
# post
# /v1/auth/confirm-email
class ConfirmEmail(CreateAPIView):
    def post(self, request):
        helper.checkParams(request, ["email", "otp"])
        helper.verify_recaptcha(request)

        try:
            user = User.objects.get(
                email=request.data["email"], otp=request.data["otp"]
            )
        except Exception:
            raise helper.exception.ParseError(
                helper.message.VERIFY_OTP_MISMATCH)

        user.is_verified = True
        user.save()

        return helper.createResponse(
            helper.message.LOGIN_SUCCESS,
            {
                "username": user.username,
                "email": user.email,
                "token": helper.get_token(user),
            },
        )


# Forgot Password
# post
# /v1/auth/forgot-password
class ForgotPassword(CreateAPIView):
    def post(self, request):
        helper.checkParams(request, ["email"])
        helper.verify_recaptcha(request)

        try:
            user = User.objects.get(
                email=request.data["email"], is_superuser=False)
        except Exception:
            raise helper.exception.NotAcceptable(
                helper.message.MODULE_NOT_FOUND("User")
            )

        user.otp = helper.generateOTP(6)
        user.save()

        helper.mail.sendOTP(user.email, user.otp)

        return helper.createResponse(helper.message.MOBILE_OTP_SENT_SUCCESS)


# Reset Password
# post
# /v1/auth/reset-password
class ResetPassword(CreateAPIView):
    def post(self, request):
        helper.checkParams(request, ["email", "otp", "password"])
        helper.verify_recaptcha(request)

        # check password length
        if len(request.data["password"]) < 8:
            raise helper.exception.ParseError(helper.message.PASSWORD_LENGTH)

        try:
            user = User.objects.get(
                email=request.data["email"], otp=request.data["otp"], is_superuser=False
            )
        except Exception:
            raise helper.exception.ParseError(
                helper.message.VERIFY_OTP_MISMATCH)

        user.set_password(request.data["password"])
        user.otp = None
        user.save()

        return helper.createResponse(
            helper.message.RESET_PASSWORD_SUCCESS,
            {
                "token": helper.get_token(user)
            }
        )


# Verify Access
# get
# /v1/auth/access
class CheckAccess(ListAPIView):
    permission_classes = [helper.permission.IsAuthenticated]

    def list(self, request):
        return helper.createResponse(helper.message.ACCESS_TRUE, {
            "success": True,
            "is_2fa": request.user.is_2fa,
            "is_active": request.user.is_active
        })


# Update Password
# post
# /v1/auth/update-password
class UpdatePassword(CreateAPIView):
    permission_classes = [helper.permission.IsAuthenticated]
    serializer_class = UserLoginSerializer

    def post(self, request):
        helper.checkParams(request, ["old_password", "new_password"])
        helper.isEmpty(request.data["old_password"], "old_password")

        # check password length
        if len(request.data["new_password"]) < 8:
            raise helper.exception.ParseError(helper.message.PASSWORD_LENGTH)

        user = authenticate(
            **{
                "username": request.user.username,
                "password": request.data["old_password"],
            }
        )

        if user != None:
            user.set_password(request.data["new_password"])
            user.save()
            return helper.createResponse(helper.message.CHANGE_PASSWORD_SUCCESS)
        else:
            return helper.createResponse(helper.message.PASSWORD_MISMATCH, status_code=400)
