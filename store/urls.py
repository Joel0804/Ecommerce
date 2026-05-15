from .import views
from django.urls import path


urlpatterns = [
    path('', views.home, name='home'),
    path('about',views.about, name='about'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register_user, name='register'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart,name='add_to_cart'), 
    path('cart', views.cart, name='cart'),
    path('remove_cart/<int:item_id>',views.remove_cart,name='remove_cart'),
    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
    path('checkout', views.checkout, name='checkout'),  
    path('order_history', views.order_history, name='order_history'), 
] 

