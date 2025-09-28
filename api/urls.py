from django.urls import path
from .views import  RegisterView, ProductListCreateView, ProductDetailView, ProductCreateView, LoginView


urlpatterns = [
    path("register/", RegisterView.as_view(), name="user_register"),
    path('login/', LoginView.as_view(), name='login'),
    path('products/', ProductListCreateView.as_view(), name='product_list_create'),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path('products/add/', ProductCreateView.as_view(), name='add-product'),
]
