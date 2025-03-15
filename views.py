from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Product  # Only import ONCE
from .forms import LoginForm, SignUpForm, SellerLoginForm, SellerSignupForm
from django.http import HttpResponse
from django.template import loader
from .forms import ProductForm


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


# Log in for seller
def login_seller(request):
    form = SellerLoginForm(data=request.POST or None)  

    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                return redirect('seller')  # Redirect to seller dashboard
            else:
                messages.error(request, "Authentication failed. User not found.")
        else:
            print(form.errors)  # DEBUG: Show form errors
            messages.error(request, "Invalid username or password.")

    return render(request, 'landingpage.html', {"signup_form": form, "login_form": form, "user_type": "Seller"})


# Seller registration
def register_seller(request):
    form = SellerSignupForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])  # Hash the password
        user.save()
        messages.success(request, "Seller account created successfully! 🎉")

        login(request, user)  # Log in the new seller immediately
        return redirect("seller")  # Redirect to seller dashboard

    return render(request, "landingpage.html", { "login_form": form, "signup_form": form, "user_type": "Seller"})


@login_required 
def seller(request):
    return render(request, 'seller.html')


def get_products(request):
    try:
        products = Product.objects.all().values('name', 'price', 'category', 'quantity')
        return JsonResponse({'products': list(products)})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        category = request.POST.get('category')
        quantity = request.POST.get('quantity')

        # Debugging output to check values
        print(f"Received - Name: {name}, Price: {price}, Category: {category}, Quantity: {quantity}")

        try:
            # Create and save the product
            product = Product.objects.create(
                name=name,
                price=price,
                category=category,
                quantity=quantity,
            )
            return JsonResponse({'success': True, 'product_id': product.id})

        except Exception as e:
            print(f"Error occurred: {str(e)}")  # Debugging error
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


# User logout
def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('landingpage') 

