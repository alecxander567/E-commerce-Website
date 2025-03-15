from django.urls import path
from . import views
from .views import landingpage, home, user_logout, sign_up, seller, login_seller, register_seller, add_product, get_products
urlpatterns = [
    path('', landingpage, name='landingpage'),
    path('sign-up/', sign_up, name='sign_up'),
    path('home/', home, name='home'),
    path('seller/', seller, name='seller'),
    path('login-seller/', login_seller, name='login_seller'),
    path('register-seller/', register_seller, name='register_seller'),
    path('add-product/', add_product, name='add_product'),  # Fixed duplicate
    path('get-products/', get_products, name='get_products'),
    path('logout/', user_logout, name='user_logout'),
]
