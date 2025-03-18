from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator 
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)    
    
    def __str__(self):
        return self.name
    

class Feedback(models.Model):
    RATING_CHOICES = (
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    )
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='feedbacks')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.buyer.username}'s feedback on {self.product.name}"
    
    
class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.product.quantity >= self.quantity:
            self.product.quantity -= self.quantity  # Reduce stock
            self.product.save()
            self.total_price = self.product.price * self.quantity
            super().save(*args, **kwargs)
        else:
            raise ValueError("Not enough stock available!")
    
    def __str__(self):
        return f"Order by {self.buyer.username} - {self.product.name} ({self.quantity})"
    



    
    
    
