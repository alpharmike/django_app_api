from django.contrib.auth.models import User
from rest_framework import serializers

from django_app.models import Profile
from django_project import settings


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ["user", "image", "password"]
        extra_kwargs = {
            'password': {'write_only': True}
        }
        # fields = ["id", "first_name", "last_name", "username", "password", "email", "image"]

# class PostSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Post
#         fields = "__all__"
#         # fields = ["name", "id"]
