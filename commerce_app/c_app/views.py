from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse
from rest_framework import mixins,generics
from .serailzer import *
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from rest_framework import viewsets
import requests
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from django.contrib import messages
# from .gemini_service import GeminiProductService
import re
from django.conf import settings

import google.generativeai as genai
def landing_page(request):
    return render(request,'langingpage.html')

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
    return render(request,'login.html')

def signup_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        print(username)
        email = request.POST.get('email')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        user = User.objects.create_user(username=username,email=email,password=password,gender=gender)
        user.save()
        return redirect('login')
    return render(request,'signup.html')

def logout_user(request):
    logout(request)
    return redirect('login')


@login_required
def orders_page(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders.html', {'orders': orders})
    

    








@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    item, created = CartItem.objects.get_or_create(user=request.user, products=product)
    
    action = request.POST.get('action', 'add')
    if action == 'increase':
        item.quantity += 1
        messages.success(request, "Quantity increased!")
    elif action == 'decrease':
        if item.quantity > 1:
            item.quantity -= 1
            messages.success(request, "Quantity decreased!")
        else:
            item.delete()
            messages.success(request, "Item removed from cart!")
            return redirect('cart')
    else:  # action == 'add'
        if not created:
            item.quantity += 1
            messages.success(request, "Quantity increased!")
        else:
            messages.success(request, "Item added to cart!")
    
    item.save()
    
    # If the request is from the dashboard, return to dashboard
    if request.META.get('HTTP_REFERER', '').endswith('/dashboard/'):
        return redirect('home')
    return redirect('cart')

@login_required
def Cart(request):
    # cart = CartItem.objects.filter(cart=request.cart)
        cart_items=CartItem.objects.filter(user=request.user)
        print(cart_items[0].products.price)
        total_price = sum(item.total_price for item in cart_items)
        # print(total_price)
        context = {
            'cart_items':cart_items,
            'total_amount' : total_price
        }
        return render(request,'cart.html',context)

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('cart')




@login_required
def view_order_detail(request, order_id):
    print(f"Accessing order_id: {order_id}")  # Debug print
    try:
        # Get the order with a more specific error message
        order = Order.objects.get(id=order_id)
        print(f"Found order: {order}")  # Debug print

        # Security check
        if order.user != request.user:
            messages.error(request, "You don't have permission to view this order.")
            return redirect('orders')
        
        # Get all items for this order
        order_items = OrderItem.objects.select_related('product').filter(order=order)
        print(f"Found {len(order_items)} items")  # Debug print
        
        # Calculate order details
        subtotal = sum(item.product.price * item.quantity for item in order_items)
        total_items = sum(item.quantity for item in order_items)
        
        context = {
            'order': order,
            'items': order_items,
            'subtotal': subtotal,
            'total_items': total_items,
            'shipping': 0,  # You can modify this based on your shipping logic
            'tax': 0,      # You can modify this based on your tax logic
        }
        print(f"Rendering template with context: {context}")  # Debug print
        return render(request, 'view_oders_.html', context)
    
    except Order.DoesNotExist:
        print(f"Order {order_id} not found")  # Debug print
        messages.error(request, f"Order #{order_id} not found!")
        return redirect('orders')
    except Exception as e:
        print(f"Error in view_order_detail: {str(e)}")  # Debug print
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('orders')


def create_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        category = request.POST.get('category')
        category_instance = Category.objects.get(id=category)
        product = Product.objects.create(name=name,price=price,category=category_instance)
        product.save()
        return redirect('create_product')
    category = Category.objects.all()
    return render(request,'create_product.html',{'categorys':category})


class usercv(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
from rest_framework.response import Response
@api_view(['POST'])
def create_user(request):
    if request.method == 'POST':
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        gender = request.data.get('gender')
        profile_pic = request.data.get("profile_pic")
        print(profile_pic)
        user = User.objects.create_user(username=username,email=email,password=password,gender=gender,profile_pic=profile_pic)
        user.save()
        return Response({'message':'User created successfully'})

class categorycv(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class productcv(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class orderitemcv(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

# class ordercv(generics.ListCreateAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer

class userrud(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class categoryrud(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class productrud(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class cartitemcv(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

class cartitemrud(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

class orderitemrud(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

# class orderrud(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer

class ordermodelviewset(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # def get_queryset(self):
    #     return Order.objects.filter(user=self.request.user)





def get_external_products(request):
    url = "https://dummyjson.com/products"

    try:
        response = requests.get(url)
        response.raise_for_status()  # raises error for 4xx/5xx

        data = response.json().get('products',[])  # dict containing 'products'
        return JsonResponse(data, safe=False)

    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)


def fetch_and_save_products(request):
    url = "https://dummyjson.com/products"
    response = requests.get(url)
    if response.status_code == 200:
        products = response.json().get('products', [])
        for item in products:
            image_url = item.get('images')
            image=image_url[0] 
            print(image) # Get the first image URL or None
            Product.objects.get_or_create(name=item['title'],price=item['price'],description=item['description'],image=image,stock=item['stock'],rating=item['rating'],category=item['category'],brand=item.get('brand','unknown'),
                                          sku=item['sku'], weight=item['weight'], dimensions=item['dimensions'], warrantyInformation=item['warrantyInformation'], shippingInformation=item['shippingInformation'], returnPolicy=['returnPolicy'], availabilityStatus=item['availabilityStatus'], minimumOrderQuantity=item['minimumOrderQuantity'], tags=item['tags'], reviews=item['reviews'])
        return JsonResponse({'message': 'Products saved'})
    return JsonResponse({'error': 'Failed to fetch data'}, status=500)


def show_products(request):
    url = "https://dummyjson.com/products"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    products = data.get('products', [])
    print(products)
        # return 
    return JsonResponse(products,safe=False)
    # except requests.exceptions.RequestException as e:
    #     return render(request, 'home.html', {'error': str(e)})



@login_required
@permission_classes(["is_authenticated"])
def home_page(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    
    # Handle search
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(name__icontains=search_query)
        if products.count() == 1:
            # If exactly one product is found, redirect to its detail page
            return redirect('product_detail', product_id=products.first().id)
    
    # Handle category filter
    selected_category_id = request.GET.get('category')
    if selected_category_id:
        category = Category.objects.get(id=selected_category_id)
        if category.name != "All Categories":
            products = products.filter(category=category.name)
    
    # Handle price filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass
    
    # Annotate products with cart information
    if request.user.is_authenticated:
        for product in products:
            product.cart_quantity = product.get_cart_quantity(request.user)
            product.in_cart = product.in_cart(request.user)
    # if not products.exists():
    #     products="NO PRODUCTS FOUND!!! 🥲🥲😔"
    context = {
                'categories': categories,
                'products': products,
                'selected_category_id': int(selected_category_id) if selected_category_id else None,
            }
    
    # Annotate products with cart information
  
    return render(request, 'dashboard.html',context)

@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # if request.user.is_authenticated:
    #     for product in product:
    product.cart_quantity = product.get_cart_quantity(request.user)
    product.in_cart = product.in_cart(request.user)
    
    print(product)
    return render(request, 'product_detail.html', {'product': product})





from django.shortcuts import render
from .models import ChatMessage
import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)


@login_required
def gemini_ai(request):
    if request.method == "POST":
        question = request.POST.get("question")
        print(request.user)
        # user=request.POST.get("request.user")
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Answer the following question:\n\n{question}"

        try:
            response = model.generate_content(prompt)
            answer = response.text
        except Exception as e:
            answer = f"Error: {str(e)}"
        
        # Save user's question and bot's response
        ChatMessage.objects.create(message=question, sender='user',user=request.user)
        ChatMessage.objects.create(message=answer, sender='bot',user=request.user)

    # Get chat history (latest first)
    user_history = ChatMessage.objects.filter(user=request.user).order_by('timestamp')
    # history = ChatMessage.objects
    return render(request, "chat.html", {"history": user_history})


from django.views.decorators.http import require_POST
@require_POST
@login_required
def clear_chat(request):
    ChatMessage.objects.filter(user=request.user).delete()
    return redirect('gemini_ai')  # update with your URL name


# views.py
from django.conf import settings
from django.views import View
from django.http import JsonResponse
from django.db.models import Q
import stripe

def search_products_api(request):
    query = request.GET.get('q', '')
    if len(query) >= 2:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(category__icontains=query) |
            Q(description__icontains=query)
        )[:5]  # Limit to 5 results for performance
        
        products_data = [{
            'id': p.id,
            'name': p.name,
            'price': p.price,
            'category': p.category,
            'image': p.image,
            'brand': p.brand
        } for p in products]
        
        return JsonResponse({'products': products_data})


stripe.api_key = settings.STRIPE_SECRET_KEY

def payment_checkout(request):

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'inr',
                'unit_amount':5000, #₹199 in paise
                'product_data': {
                    'name': 'Order summary',
                },
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri('/home/'),
        cancel_url='http://localhost:8000/payment/cancel/',
    )
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        return redirect('cart')
    order = Order.objects.create(user=request.user)
    for item in cart_items:
        OrderItem.objects.create(order=order,product=item.products,quantity=item.quantity)
    cart_items.delete()    
    return redirect(session.url)



def place_order(request):
    # CreateCheckoutSessionView()
    return redirect('orders')

