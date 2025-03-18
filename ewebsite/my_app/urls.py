from django.urls import path
from .views import landingpage, home, user_logout, sign_up, seller, login_seller, register_seller, add_product, get_products, buyers_page,  purchase_product, edit_product, delete_product, add_feedback, buy_product, get_orders, delete_order, sales_chart

urlpatterns = [
    path('', landingpage, name='landingpage'),
    path('sign-up/', sign_up, name='sign_up'),
    path('home/', home, name='home'),
    path('seller/', seller, name='seller'),
    path('login-seller/', login_seller, name='login_seller'),
    path('register-seller/', register_seller, name='register_seller'),
    path('add-product/', add_product, name='add_product'),  
    path('get-products/', get_products, name='get_products'),
    path('buyers/', buyers_page, name='buyers_page'),
    path('purchase-product/', purchase_product, name='purchase_product'),
    path("edit_product/<int:product_id>/", edit_product, name="edit_product"),
    path("delete_product/<int:product_id>/", delete_product, name="delete_product"),
    path('product/<int:product_id>/feedback/', add_feedback, name='add_feedback'),
    path("buy-product/", buy_product, name="buy_product"),
    path('get-orders/', get_orders, name='get-orders'),
    path('delete-order/<int:order_id>/', delete_order, name='delete_order'),
    path("sales_chart/", sales_chart, name="sales_chart"), 
    path('logout/', user_logout, name='user_logout'),
]
