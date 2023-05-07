from django.conf.urls import url
from django.urls import path
from .api import (
    AdminLogin,
    Signup,
    Login,
    ConfirmEmail,
    ForgotPassword,
    ResetPassword,
    CheckAccess,
    UpdatePassword,
)

urlpatterns = [
    path("admin-login", AdminLogin.as_view()),
    path("signup", Signup.as_view()),
    path("login", Login.as_view()),
    path("confirm-email", ConfirmEmail.as_view()),
    path("forgot-password", ForgotPassword.as_view()),
    path("reset-password", ResetPassword.as_view()),
    path("access", CheckAccess.as_view()),
    path("update-password", UpdatePassword.as_view())
]
