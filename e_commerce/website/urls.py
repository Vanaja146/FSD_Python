from django.urls import path
from . import views

urlpatterns = [
    # Home
    path("", views.home, name="home"),

    # Authentication
    path("signup/", views.signup_user, name="signup"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),

    # Profile
    path("profile/", views.profile, name="profile"),  # ✅ Added profile

    # Products
    path("products/", views.products_page, name="product_list"),
    path("products/<int:product_id>/", views.product_detail, name="product_detail"),
    path("search/", views.search, name="search"),

    # Cart
    path("cart/", views.cart, name="cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"),

    # Checkout
    path("checkout/", views.checkout, name="checkout"),

    # API
    path("api/product/", views.product_list, name="api_product_list"),
]
