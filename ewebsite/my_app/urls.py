from django.urls import path
from django.contrib.auth import views as auth_views
from .views import landingpage, home

urlpatterns = [
    path('', landingpage, name='landingpage.html'), 
    path('home/', home, name='home.html'),  
    path('login/', auth_views.LoginView.as_view(template_name='landingpage.html'), name='user_login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='landingpage'), name='logout'),
]