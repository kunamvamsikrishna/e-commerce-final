from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer): 
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    # category = CategorySerializer()
    class Meta:
        model = Product
        fields = '__all__'
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'
        
class OrderItemSerializer(serializers.ModelSerializer): 

    # product = ProductSerializer()
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    # orderitem = OrderItemSerializer(many=True)
    # user = UserSerializer()
    class Meta:
        model = Order
        fields = '__all__'

            


