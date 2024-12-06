from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .models import Diary, Post, Comment
from .serializers import (
    DiarySerializer,
    UserRegistrationSerializer,
    UserLoginSerializer,
    PostSerializer,
    CommentSerializer,
)
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from datetime import datetime


# 회원가입 API
class UserRegistrationAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {"token": token.key, "user_id": user.pk, "username": user.username},
            status=status.HTTP_201_CREATED,
        )


# 로그인 API
class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response(
                    {"token": token.key, "user_id": user.pk, "username": user.username},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 일기 등록 API
class DiaryCreateAPIView(generics.CreateAPIView):
    serializer_class = DiarySerializer
    permission_classes = [permissions.IsAuthenticated]

    # DartError: Converting object to an encodable object failed: Instance of 'DateTime'

    # 사용자 정보 포함하여 일기 생성
    def perform_create(self, serializer):
        print(f"DiaryCreateAPIView - 일기 생성")
        serializer.save(
            user=self.request.user, write_date=self.request.data["write_date"]
        )


# 일기 목록 조회 API
class DiaryListAPIView(generics.ListAPIView):
    serializer_class = DiarySerializer
    permission_classes = [permissions.IsAuthenticated]

    # 특정 날짜의 일기 목록 조회
    def get_queryset(self):
        print(f"DiaryListAPIView - 일기 목록 조회")

        date_str = self.request.query_params.get("date", None)
        user_id = self.request.user.id
        if date_str:
            print(f"일기 목록 조회 ({date_str}) - 사용자 {self.request.user}")
            diaries = Diary.objects.filter(user_id=user_id, write_date__date=date_str)
            print(
                f"일기 목록 조회 ({date_str}) - 사용자 {self.request.user} - 일기 목록: {list(diaries.values())}"
            )
            return diaries
        else:
            print(f"일기 목록 조회 ({user_id})")
            return Diary.objects.filter(user_id=user_id)


# 특정 일기 조회 API
class DiaryDetailAPIView(generics.RetrieveAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer
    permission_classes = [permissions.IsAuthenticated]

    # json 형식으로 반환
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        print(f"일기 조회 ({instance.id}) - 사용자 {self.request.user}")
        return Response(serializer.data)


# 일기 수정 API
class DiaryUpdateAPIView(generics.UpdateAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer
    permission_classes = [permissions.IsAuthenticated]

    # 현재 사용자 소유의 일기만 수정 가능하도록 필터링
    def get_queryset(self):
        print(f"DiaryUpdateAPIView - 일기 수정 ({self.kwargs['pk']})")
        return Diary.objects.filter(user=self.request.user)


# 일기 삭제 API
class DiaryDeleteAPIView(generics.DestroyAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer
    permission_classes = [permissions.IsAuthenticated]

    # 현재 사용자 소유의 일기만 삭제 가능하도록 필터링
    def get_queryset(self):
        print(f"DiaryDeleteAPIView - 일기 삭제 ({self.kwargs['pk']})")
        return Diary.objects.filter(user=self.request.user)


class PostCreateAPIView(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# 게시글 목록 조회 API
class PostListAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.all()


# 게시글 수정 API
class PostUpdateAPIView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)


# 게시글 삭제 API
class PostDeleteAPIView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)


# 댓글 등록 API
class CommentCreateAPIView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# 특정 게시글의 댓글 목록 조회 API
class CommentListAPIView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        return Comment.objects.filter(post_id=post_id)


# 특정 날짜의 일기 목록 조회 API
class DiaryListByDateAPIView(generics.ListAPIView):
    serializer_class = DiarySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        date_str = self.kwargs["date"]
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        return Diary.objects.filter(user=self.request.user, created_at__date=date)
