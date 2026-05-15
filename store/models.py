from django.db import models
import datetime
from django.contrib.auth.models import User
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural  = 'categories'

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    description = models.CharField(max_length=250, default='', blank=True, null=True)
    image = models.ImageField(upload_to='upload/products/')
    category= models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    on_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    
    def __str__(self):
        return self.name
    
    
class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, unique=True)
    phone_no = models.CharField(max_length=20)
    password = models.CharField(max_length=128)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address =  models.CharField(max_length=150, default='', blank=True)
    phone_no = models.CharField(max_length=20)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)
    city = models.CharField(max_length=50, default='')
    state = models.CharField(max_length=100, default='')
    country = models.CharField(max_length=50, default='')
    pincode = models.CharField(max_length=12, help_text="Enter postal code", default='') 
    
    def __str__(self):
        return str(self.product)
    
    
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    date = models.DateField(default=datetime.datetime.today)
    
    
