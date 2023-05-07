from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from helper import helper
import uuid


class MyAccountManager(BaseUserManager):
    def create_user(self, username, email, password):
        user = self.model(username=username, email=email)

        user.set_password(password)
        user.is_verified = False
        user.is_2fa = False
        user.is_active = True
        user.is_superuser = False
        user.isPaid = False
        user.todayDownloads = 0
        user.fingerPrint = helper.genSecretKey()
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            username=username, email=email, password=password)
        user.is_superuser = True
        user.is_verified = True
        # user.is_2fa = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    # Integrity Fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)

    # additional fields
    isPaid = models.BooleanField(default=False)
    fingerPrint = models.CharField(max_length=100)
    todayDownloads = models.IntegerField(default=0)

    # permissions and verification fields
    is_2fa = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    # login data fields
    otp = models.IntegerField(blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    expiry = models.DateTimeField(blank=True, null=True)

    # required configs
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]
    objects = MyAccountManager()

    def __str__(self):
        return self.id

    class Meta:
        db_table = "users"
