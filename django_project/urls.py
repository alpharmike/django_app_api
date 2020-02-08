"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from rest_framework.authtoken.views import obtain_auth_token
from django_app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', obtain_auth_token, name='api_token_auth'),
    path('api/sign_up/', SignupView.as_view()),
    path('profile/list/', ProfileListView.as_view()),
    path('profile/ret/<int:id>', ProfileRetrieveView.as_view()),
    path('api/profile/update/', ProfileUpdateView.as_view()),
    path('api/profile/delete/', ProfileDeleteView.as_view()),
    # path('post/create/', PostCreateView.as_view()),
    # path('post/list/', PostListView.as_view()),
    # path('post/ret/<int:id>', PostRetrieveView.as_view()),
    # path('post/update/<int:id>', PostUpdateView.as_view()),
    # path('post/delete/<int:id>', PostDeleteView.as_view())
]
