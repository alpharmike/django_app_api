from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from django.core import serializers
from django_app.models import Profile
from django_app.serializers import ProfileSerializer, UserSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny


class ProfileListView(ListAPIView):
    serializer_class = ProfileSerializer
    allowed_methods = ["GET"]
    # permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.all()


class SignupView(CreateAPIView):
    allowed_methods = ["POST"]
    serializer_class = ProfileSerializer

    # permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        first_name = request.data.get("user.first_name", None)
        last_name = request.data.get("user.last_name", None)
        username = request.data.get("user.username", None)
        password = request.data.get("password", None)
        email = request.data.get("user.email", None)
        image = request.data.get("image", None)
        try:
            if not (first_name and last_name and username and password and email):
                response = Response({"message": "Required Fields Not Filled"})
            else:
                try:
                    user = User.objects.get(username=username)  # exception is raised if user not found
                    if user:
                        response = Response({"message": "Username Already Taken, Please Choose Another One"},
                                            status=status.HTTP_400_BAD_REQUEST)
                except:
                    user = User.objects.create(first_name=first_name, last_name=last_name, email=email,
                                               username=username)
                    user.set_password(password)
                    user.save()
                    profile = Profile.objects.create(image=image, user=user)
                    serializer = self.get_serializer(profile)
                    response = Response({"profile": serializer.data})
        except:
            response = Response({"message": "Server Currently Not Responsible"})
        return response


class ProfileRetrieveView(RetrieveAPIView):
    allowed_methods = ["GET"]
    serializer_class = ProfileSerializer

    def get(self, request, *args, **kwargs):
        id = kwargs.get("id", None)
        if not id:
            return Response({"message": "ID Not Found"})
        user = Profile.objects.get(id=id)
        serializer = self.get_serializer(user)
        return Response({"profile": serializer.data})


class ProfileUpdateView(UpdateAPIView):
    allowed_methods = ["PATCH"]
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        first_name = request.data.get("user.first_name", user.first_name)
        last_name = request.data.get("user.last_name", user.last_name)
        username = request.data.get("user.username", user.username)
        email = request.data.get("user.email", user.email)
        image = request.data.get("image", profile.image)
        try:
            temp_user = User.objects.get(username=username)
            response = Response({"message": "Username Already Taken, Please Choose Another One"},
                                status=status.HTTP_400_BAD_REQUEST)
        except:
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email
            profile.image = image
            print("before")
            user.save(update_fields=["first_name", "last_name", "username", "email"])
            profile.user = user
            print("next")
            profile.save(update_fields=["user", "image"])
            print("after_all")
            serializer = self.get_serializer(profile)
            response = Response({"profile": serializer.data}, status=status.HTTP_200_OK)
        return response


class ProfileDeleteView(DestroyAPIView):
    allowed_methods = ["DELETE"]
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        user.delete()
        return Response({"message": "Successfully Deleted"}, status=status.HTTP_200_OK)

# class PostListView(ListAPIView):
#     serializer_class = PostSerializer
#     allowed_methods = ["GET"]
#     queryset = Post.objects.all()
#
#
# class PostCreateView(CreateAPIView):
#     allowed_methods = ["POST"]
#     serializer_class = PostSerializer
#
#     def post(self, request, *args, **kwargs):
#         body = request.data.get("body", None)
#         sender = request.data.get("sender", None)
#         if not sender:
#             return Response({"message": "User Not Found"})
#         if not body:
#             return Response({"message": "Empty Body"})
#         sender = User.objects.get(id=sender)
#         post = Post.objects.create(body=body, sender=sender)
#         serializer = self.get_serializer(post)
#         return JsonResponse({"post": serializer.data}, status=status.HTTP_200_OK, safe=False)
#
#
# class PostRetrieveView(RetrieveAPIView):
#     allowed_methods = ["POST"]
#     serializer_class = PostSerializer
#
#     def get(self, request, *args, **kwargs):
#         id = kwargs.get("id", None)
#         if not id:
#             return Response("Post Not Found")
#         post = Post.objects.get(id=id)
#         serializer = self.get_serializer(post)
#         return Response({"post": serializer.data})
#
#
# class PostUpdateView(UpdateAPIView):
#     allowed_methods = ["PATCH"]
#     serializer_class = PostSerializer
#
#     def update(self, request, *args, **kwargs):
#         id = kwargs.get("id", None)
#         body = request.data.get("body")
#         if not id:
#             return Response("Post Not Found")
#         post = Post.objects.get(id=id)
#         post.body = body
#         post.save(update_fields=["body"])
#         serializer = self.get_serializer(post)
#         return Response({"post": serializer.data})
#
#
# class PostDeleteView(DestroyAPIView):
#     allowed_methods = ["DELETE"]
#     serializer_class = PostSerializer
#
#     def delete(self, request, *args, **kwargs):
#         id = kwargs.get("id", None)
#         post = Post.objects.get(id=id)
#         post.delete()
#         return Response({"message": "Successfully Deleted"}, status=status.HTTP_200_OK)
