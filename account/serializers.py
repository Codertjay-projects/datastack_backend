from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    CharField
)
from django.contrib.auth import authenticate
from .models import User
from helper import helper


# Admin Login Serializer
class AdminLoginSerializer(Serializer):
    username = CharField()
    password = CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_superuser:
            return user
        raise helper.exception.AuthenticationFailed()


# User Login Serializer
class UserLoginSerializer(Serializer):
    username = CharField()
    password = CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user:
            return user
        raise helper.exception.AuthenticationFailed()


# User Signup
class UserSignupSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, data):
        user = User.objects.create_user(**data)
        user.otp = helper.generateOTP(6)

        user.save()

        helper.mail.sendOTP(user.email, user.otp)
        return user
