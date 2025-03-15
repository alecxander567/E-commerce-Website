from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    
class Meta:
    db_table = 'my_app_product' 
    
    def __str__(self):
        return self.name
    
