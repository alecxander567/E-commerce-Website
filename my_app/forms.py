from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from .models import Product, Feedback

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        

# Seller Login Form
class SellerLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Seller Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Seller Password'}))
    

# Seller Signup Form
class SellerSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # Encrypts password
        if commit:
            user.save()
        return user


class AddProductForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Name'
        })
    )
    price = forms.DecimalField(
    widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Price'
    }),
    validators=[MinValueValidator(0.01)]  # Ensure price is positive
    )
    category = forms.CharField(
    widget=forms.TextInput(attrs={
        'class': 'form-control bg-light',
        'placeholder': 'food'
    }),
    required=False  # Optional field
    )
    quantity = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'quantity'
        })
    )
    

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'quantity']
        

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'comment']

        
