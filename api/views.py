from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status, generics
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model,authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Product
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, ProductSerializer
from utils.cache_helpers import cache_response
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()



class RegisterView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            "detail": f"🎉 Welcome {user.username}, your account has been created!",
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
    


class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)  
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        print("DEBUG ->", username, password)

        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "detail": f"🎉 Welcome back, {user.username}!",
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            }, status=status.HTTP_200_OK)

        return Response(
            {"detail": "❌ Invalid credentials, try again."},
            status=status.HTTP_401_UNAUTHORIZED
        )

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated] 
