from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status, generics
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer, RegisterSerializer
from utils.cache_helpers import cache_response

User = get_user_model()


class UserListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @cache_response(ttl=60)
    def get(self, request, *args, **kwargs):
        qs = User.objects.all().order_by("-date_joined")
        serializer = UserSerializer(qs, many=True)
        return Response(serializer.data)


class UserDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @cache_response(ttl=30)
    def get(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserMeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @cache_response(ttl=20)
    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserRegisterAPIView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]  # anyone can register

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # generate JWT tokens
            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "message": "User registered successfully ✅",
                    "user": UserSerializer(user).data,
                    "tokens": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 👇 helps Swagger show request body fields
    def get_serializer_class(self):
        return RegisterSerializer
