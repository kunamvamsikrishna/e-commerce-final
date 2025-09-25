from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter 
router = DefaultRouter()
router.register(r'ordermodelviewset',ordermodelviewset)
urlpatterns = [
    path('create-checkout-session/', payment_checkout, name='create-checkout-session'),

    path('',landing_page,name='landingpage'),
    path('user/',usercv.as_view(),name='usercv'),
    path('create_user/',create_user,name='create_user'),
    path('category/',categorycv.as_view(),name='categorycv'),
    path('product/',productcv.as_view(),name='productcv'),
    path('orderitem/',orderitemcv.as_view(),name='orderitemcv'),
    # path('order/',ordercv.as_view(),name='ordercv'),
    path('',include(router.urls),name='ordermodelviewset'),
    path('user/<int:pk>/',userrud.as_view(),name='userrud'),
    path('category/<int:pk>/',categoryrud.as_view(),name='categoryrud'),
    path('product/<int:pk>/',productrud.as_view(),name='productrud'),
    path('orderitem/<int:pk>/',orderitemrud.as_view(),name='orderitemrud'),
    # path('order/<int:pk>/',orderrud.as_view(),name='orderrud'),
    path('login/',login_page,name='login'),
    path('signup/',signup_page,name='signup'),
    path('get_external_products/', get_external_products, name='get_external_products'),
    path('home/',home_page,name='home'),
    path('logout/',logout_user,name='logout'),
    path('social/',include('social_django.urls',namespace='social')),
    path('orders/',orders_page,name='orders'),
    path('order/<int:order_id>/',view_order_detail,name='view_order_detail'),
    path('add_to_cart/<int:product_id>/',add_to_cart,name='add_to_cart'),
    path('product/<int:product_id>/detail/', product_detail, name='product_detail'),
    path('remove_from_cart/<int:item_id>/',remove_from_cart,name='remove_from_cart'),
    path('cart/',Cart,name='cart'),
    # path('checkout/',checkout,name='checkout'),
    path('place_order/',place_order,name='place_order'),
    path('products/',show_products,name='show_products'),
    # path('view_order_detail/<int:order_id>/',view_order_detail,name='view_order_detail'),
    path('create_product/',create_product,name='create_product'),
    path('fetch_and_save_products/',fetch_and_save_products,name='fetch_and_save_products'),
    
    path('ai_bot/',gemini_ai,name='gemini_ai'),
    path('clear_chat/', clear_chat, name='clear_chat'),
    path('api/search-products/', search_products_api, name='search_products_api'),
]