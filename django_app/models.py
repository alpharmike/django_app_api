from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.admin import User
from rest_framework.authtoken.models import Token

from django_project import settings


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to="users")


# class Post(models.Model):
#     body = models.TextField(max_length=1000)
#     time = models.DateTimeField(auto_now=True)
#     sender = models.ForeignKey(Profile, on_delete=models.CASCADE)
