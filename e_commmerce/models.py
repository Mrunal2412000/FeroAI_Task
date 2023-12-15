from django.db import models
from django.contrib.auth.models import AbstractUser

from rest_framework_simplejwt.tokens import RefreshToken
# Create your models here.

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    email = models.EmailField(unique=True,null=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

class Product(models.Model):
    name = models.CharField(max_length=30, null=False)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2,null=False)
    stock_quantity = models.PositiveIntegerField(null=False)

    def __str__(self) -> str:
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    is_ordered = models.BooleanField(default=False) #True after ordering the products

class CartOrder(models.Model): #Intermediate Table between Cart and Order for ManyToMany relationship for products in Order table
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('placed', 'Placed'),
        ('confirmed', 'Confirmed'),
        ('in_transit', 'in_transit'),
        ('reached_nearby_hub', 'reached_nearby_hub'),
        ('out_for_delivery', 'out_for_delivery'),
        ('delivered', 'delivered'),
        ('delivery_attempted', 'delivery_attempted'),
        ('cancelled', 'cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES)
    address = models.TextField()
    products = models.ManyToManyField(Product, through=CartOrder,related_name='orders')
    delivery_attempt_count = models.IntegerField(default=0) #Added this because of delivery_attempted status
