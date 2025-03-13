from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, SignUpForm
from django.utils.http import url_has_allowed_host_and_scheme


# Landing page (contains the login form)
def landingpage(request):
    if request.user.is_authenticated:
        return redirect('home')  # Prevents logged-in users from seeing login again

    login_form = LoginForm()
    signup_form = SignUpForm()

    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('home')

    return render(request, 'landingpage.html', {'login_form': login_form, 'signup_form': signup_form})


# Protected homepage (user must be logged in)
@login_required 
def home(request):
    return render(request, 'home.html')


def sign_up(request):
    login_form = LoginForm()
    signup_form = SignUpForm()

    if request.method == "POST":
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            print(f"User {user.username} created!")  # Debugging

            # Authenticate using the correct password field
            user = authenticate(request, username=user.username, password=signup_form.cleaned_data["password1"])

            if user is not None:
                login(request, user)
                messages.success(request, "Account created successfully! 🎉")
                return redirect("home")  # Redirect to home page
            else:
                messages.error(request, "Authentication failed. Try logging in manually.")
        else:
            messages.error(request, "Signup failed. Please check the errors and try again.") 

    return render(request, 'landingpage.html', {'login_form': login_form, 'signup_form': signup_form})


# User logout
def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('landingpage') 

