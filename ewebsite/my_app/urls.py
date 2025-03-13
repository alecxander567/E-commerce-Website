from django.urls import path
from .views import landingpage, home, user_logout, sign_up


urlpatterns = [
    path('', landingpage, name='landingpage'),
    path('sign_up/', sign_up, name='sign_up'),
    path('home/', home, name='home'),
    path('logout/', user_logout, name='user_logout'),
   
]