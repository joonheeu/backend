"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django.urls import path
from .apps import views

urlpatterns = [
    path(
        "api/register/",
        views.UserRegistrationAPIView.as_view(),
        name="user-register",
    ),
    path("api/login/", views.UserLoginAPIView.as_view(), name="user-login"),
    path(
        "api/diaries/create/", views.DiaryCreateAPIView.as_view(), name="diary-create"
    ),
    path("api/diaries/list/", views.DiaryListAPIView.as_view(), name="diary-list"),
    path(
        "api/diaries/<str:date>/",
        views.DiaryListByDateAPIView.as_view(),
        name="diary-list-by-date",
    ),
    path(
        "api/diaries/<int:pk>/update/",
        views.DiaryUpdateAPIView.as_view(),
        name="diary-update",
    ),
    path(
        "api/diaries/<int:pk>/delete/",
        views.DiaryDeleteAPIView.as_view(),
        name="diary-delete",
    ),
    path("posts/", views.PostListAPIView.as_view(), name="list_posts"),
    path("posts/create/", views.PostCreateAPIView.as_view(), name="create_post"),
    path(
        "posts/update/<int:pk>/", views.PostUpdateAPIView.as_view(), name="update_post"
    ),
    path(
        "posts/delete/<int:pk>/", views.PostDeleteAPIView.as_view(), name="delete_post"
    ),
    path(
        "posts/<int:post_id>/comments/",
        views.CommentListAPIView.as_view(),
        name="list_comments",
    ),
    path(
        "comments/create/", views.CommentCreateAPIView.as_view(), name="create_comment"
    ),
]
