from django.shortcuts import render, redirect
from .models import Cart, Product, Order
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
import razorpay
from django.conf import settings

# Create your views here.
@login_required(login_url='login')
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def about(request):
    return render(request, 'about.html',{})

def login_user(request):
    if request.method == 'POST': # if user submits 
        username = request.POST['username'] # grab it 
        password = request.POST['password']
        user = authenticate(request, username=username, password=password) # authenticate
        if user is not None: # this checks condition if user is present in db
            login(request, user)  # this remember user 
            messages.success(request, ("You have successfully logged in! "))
            return redirect('home')
        else:
            messages.success(request, ("There is an Error! Enter as per register credenstials"))
            return redirect('login')        
    else: 
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You have successfully logout, Thanks for visiting website"))
    return redirect('home')
 
def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST) # takes signup form data 
        if form.is_valid(): # checks if everything is filled or not
            form.save() # saved it creates new user in db
            messages.success(request,("You have sucessfully registered") )
            return redirect('login')
        else:
            return render(request, 'register.html', {'form':form})
    else:
        form = SignUpForm() # if user open registered did not post anything
        return render(request, 'register.html', {'form':form})
    
    
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id) # get products based on id 
    cart_item = Cart(user=request.user , product=product, quantity=1) # this creates new cart with products
    cart_item.save()
    return redirect ('home')

 
def cart(request):
    cart_display = Cart.objects.filter(user=request.user).order_by('-date') # Get all cart objects belonging to the current logged-in user
    return render(request, 'cart.html', {'cart_displays': cart_display})

def remove_cart(request, item_id):
    cart_item = Cart.objects.get(id=item_id, user=request.user)
    cart_item.delete()
    return redirect('cart')


def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'product_detail.html', {'product': product} )
    

def checkout(request):
    checkout_item = Cart.objects.filter(user=request.user) # gets cart objects 
    if request.method == 'POST': # checks user submit
        if not checkout_item.exists(): # if checkout does not exist as in no selected items in cart
            return redirect('cart')

        address  = request.POST["address"] # grabs the input 
        state = request.POST['state']
        phone_no = request.POST['phone_no']
        country = request.POST['country']
        pincode = request.POST['pincode']
        
        for item in checkout_item: # loop through items 
               Order.objects.create( # create new order jere user becomes customer
               customer=request.user,
               product=item.product,
               address=address,
               state=state,
               phone_no=phone_no,
               country=country,
               pincode=pincode
               )
        checkout_item.delete()
        messages.success(request, "Order placed successfully")
        return redirect('order_history')
    else:
        total =  sum (item.product.sale_price if item.product.on_sale else item.product.price 
    for item in checkout_item)
    
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        
        razorpay_order = client.order.create({
            'amount': int(total * 100),  # Razorpay needs amount in paise
            'currency': 'INR',
            'payment_capture': 1
        })
        
        return render(request, 'checkout.html', {
            'cart_items': checkout_item,
            'razorpay_order_id': razorpay_order['id'],
            'razorpay_key': settings.RAZORPAY_KEY_ID,
            'total': total
        })
    
def order_history(request):
     order_item =   Order.objects.filter(customer=request.user)
     return render(request, 'order_history.html', {'order_items': order_item})