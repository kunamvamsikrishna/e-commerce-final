# from unicodedata import category    
from pickle import TRUE
from django.db import models
from rest_framework import generics,mixins
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.

class User(AbstractUser):
    gender = models.CharField(max_length=200,blank=True,null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/',blank=True,null=True)
   
class Category(models.Model):
     name = models.CharField(max_length=100)

class Product(models.Model):
    title = models.CharField(max_length=200,blank=False,null=True)
    name = models.CharField(max_length=200,blank=True,null=True)
    price = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    discountPercentage = models.DecimalField(max_digits=5,decimal_places=2,blank=True,null=True)
    category = models.CharField(max_length=100,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    image = models.CharField(max_length=200,blank=True,null=True)
    thumbnail = models.CharField(max_length=200,blank=True,null=True)
    stock = models.IntegerField(default=0,blank=True,null=True)
    rating = models.DecimalField(max_digits=3,decimal_places=2,default=0.0,blank=True,null=True)
    brand = models.CharField(max_length=100,blank=True,null=True)
    sku = models.CharField(max_length=50,blank=True,null=True)
    weight = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    dimensions = models.JSONField(blank=True,null=True) 
    warrantyInformation = models.CharField(max_length=200,blank=True,null=True)
    shippingInformation = models.CharField(max_length=200,blank=True,null=True)
    returnPolicy = models.CharField(max_length=200,blank=True,null=True)
    availabilityStatus = models.CharField(max_length=50,blank=True,null=True)
    minimumOrderQuantity = models.IntegerField(default=1,blank=True,null=True)
    tags = models.JSONField(blank=True,null=True) 
    reviews = models.JSONField(blank=True,null=True)  
    def get_cart_quantity(self, user=None):
        if user and user.is_authenticated:
            cart_item = CartItem.objects.filter(user=user, products=self).first()
            return cart_item.quantity if cart_item else 0
        return 0

    def in_cart(self, user=None):
        if user and user.is_authenticated:
            return CartItem.objects.filter(user=user, products=self).exists()
        return False

class Cart(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,blank=True,null=True)

class CartItem(models.Model):
      user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
      products = models.ForeignKey(Product,on_delete=models.CASCADE,blank=True,null=True)
      quantity = models.IntegerField(default=0)
      @property
      def total_price(self):
        return self.quantity * self.products.price
    #  @property
    #  def grand_price(self):
    #     for i in 

class Order(models.Model):
    choices=[(0,'Cart'),(1,'Pending'),(2,'Confirmed'),(3,'Shipped'),(4,'Delivered'),(5,'Cancelled')]
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    # cart_items = models.ManyToManyField(CartItem,blank=True)
    total_price = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    status = models.PositiveSmallIntegerField(choices=choices, default=0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    @property
    def grand_total(self):
        return sum(item.total_price for item in self.orderitem_set.all())   

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,blank=True,null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,blank=True,null=True)
    quantity = models.IntegerField(default=1)
    class Meta:
        unique_together = ('order', 'product')
    @property
    def total_price(self):
        return self.quantity * self.product.price

from django.db import models

class ChatMessage(models.Model):
    SENDER_CHOICES = (
        ('user', 'User'),
        ('bot', 'Bot'),
    )
    message = models.TextField()
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return f"{self.sender} at {self.timestamp}"


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.CharField(blank=True)
    