from django.urls import path
from . import views
from rest_framework.authtoken import views as drf_views

urlpatterns = [
    path('products/', views.product_list, name='product-list'),               # ✅ GET all products
    path('products/create/', views.product_create, name='product-create'),    # ✅ POST new product
    path('products/update/<int:pk>/', views.product_update, name='product-update'),  # ✅ PUT
    path('products/delete/<int:pk>/', views.product_delete, name='product-delete'),  # ✅ DELETE
    path('token/', drf_views.obtain_auth_token, name='api-token-auth'),       # ✅ Token authentication
]
