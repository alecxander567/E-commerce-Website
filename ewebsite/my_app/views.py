from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Product, Feedback, Order
from .forms import LoginForm, SignUpForm, SellerLoginForm, SellerSignupForm, FeedbackForm
from django.views.decorators.csrf import csrf_exempt
import json
from django.db import transaction
from django.db.models import Sum

# Landing page (contains the login form)
def landingpage(request):
    if request.user.is_authenticated:
        return redirect('/landingpage/')  # Prevents logged-in users from seeing login again

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
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


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
    products = Product.objects.all().values('id', 'name', 'category', 'price', 'quantity')
    return JsonResponse({"products": list(products)})
 
 
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


def buyers_page(request):
    products = Product.objects.all()  # Fetch all products
    return render(request, 'home.html', {'products': products})


@csrf_exempt
def purchase_product(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            quantity = int(data.get('quantity', 1))  # Default to 1 if not specified

            # Get the product
            product = Product.objects.get(id=product_id)

            if product.quantity >= quantity:
                product.quantity -= quantity  # Subtract the purchased quantity
                product.save()
                return JsonResponse({'success': True, 'new_quantity': product.quantity})
            else:
                return JsonResponse({'success': False, 'error': 'Not enough stock'})

        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Product not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        name = request.POST.get('name')
        price = request.POST.get('price')
        category = request.POST.get('category')
        quantity = request.POST.get('quantity')

        # Update product details
        product.name = name
        product.price = price
        product.category = category
        product.quantity = quantity
        product.save()
        
        return redirect('seller')  # Redirect to seller page

    return render(request, 'edit_product.html', {'product': product})


@login_required
def delete_product(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        product.delete()
        return JsonResponse({'success': True, 'message': 'Product deleted successfully!'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    

@login_required  # Ensure user is logged in
def add_feedback(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    feedback = form.save(commit=False)
                    feedback.buyer = request.user
                    feedback.product = product
                    feedback.save()
                    
                    # Update product rating if needed
                    # product.update_average_rating()
                    return redirect('home')  # or 'product_detail', product_id=product_id
            except Exception as e:
                messages.error(request, f"Error saving feedback: {str(e)}")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = FeedbackForm()
    
    return render(request, 'submit_feedback.html', {'form': form, 'product': product})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    feedbacks = Feedback.objects.filter(product=product).order_by('-created_at')

    return render(request, 'home.html', {
        'product': product,
        'feedbacks': feedbacks,
    })
    

def buy_product(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            product_id = data.get("product_id")
            quantity = data.get("quantity")

            # 🔥 Convert quantity to an integer
            quantity = int(quantity)  # Ensure it's an int

            product = Product.objects.get(id=product_id)
            total_price = product.price * quantity  # Calculate total price

            new_order = Order.objects.create(
                buyer=request.user,  # Ensure the user is authenticated
                product=product,
                quantity=quantity,
                total_price=total_price
            )

            return JsonResponse({"success": True, "message": "Order added!", "order_id": new_order.id})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    
    return JsonResponse({"success": False, "error": "Invalid request"})


def get_orders(request):
    orders = Order.objects.select_related('product').all()

    order_list = []
    for order in orders:
        order_list.append({
            "id": order.id,  # Add this line
            "product_name": order.product.name,  # Ensure Product has a 'name' field
            "quantity": order.quantity,
            "total_price": float(order.total_price),  # Convert Decimal to float
            "order_date": order.order_date.strftime("%Y-%m-%d %H:%M:%S")  # Format date
        })

    return JsonResponse({"orders": order_list})


@csrf_exempt
def delete_order(request, order_id):
    if request.method == "DELETE":
        try:
            order = Order.objects.get(id=order_id)
            product = Product.objects.get(id=order.product.id)

            # Restore the product's quantity
            product.quantity += order.quantity
            product.save()

            order.delete()
            return JsonResponse({"message": "Order deleted and quantity restored successfully!"})
        except Order.DoesNotExist:
            return JsonResponse({"error": "Order not found"}, status=404)
        except Product.DoesNotExist:
            return JsonResponse({"error": "Product not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        

def sales_chart(request):
    # Aggregate the total quantity of each product sold
    sales_data = (
        Order.objects.values("product__name")
        .annotate(total_sold=Sum("quantity"))
        .order_by("-total_sold")[:5]  # Get top 5 most sold products
    )

    # Prepare data for Chart.js
    products = [item["product__name"] for item in sales_data]
    sales = [item["total_sold"] for item in sales_data]

    return render(request, "sales_chart.html", {"products": products, "sales": sales})


# User logout
def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('landingpage') 

