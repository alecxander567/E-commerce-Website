from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import LoginForm 

# Landing page (contains the login form)
def landingpage(request):
    form = LoginForm()  # Initialize the login form

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home.html')  # Redirect to home page after successful login

    return render(request, 'landingpage.html', {'form': form}) 

# Protected homepage (user must be logged in)
@login_required 
def home(request):
    return render(request, 'home.html')


# User logout
def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('landingpage')  
