from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Diary, Post, Comment


# Diary Serializer
class DiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = ["id", "user", "content", "write_date", "created_at", "updated_at"]
        read_only_fields = ["user", "created_at", "updated_at"]


# User Register Serializer
class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    # 사용자 생성 메서드
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"], password=validated_data["password"]
        )
        return user


# Login Serializer
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


# Post Serializer
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "user", "title", "content", "created_at", "updated_at")


# Comment Serializer
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "post", "user", "content", "created_at")
