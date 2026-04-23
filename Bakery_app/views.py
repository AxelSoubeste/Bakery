from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.contrib.auth.models import User
from .models import Product, Order, ItemOrder
from django.contrib import messages
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import mercadopago
from django.views.decorators.csrf import csrf_exempt
import os

def staff_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        if not request.user.is_staff:
            return redirect('home')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper

def home(request):
    return render(request, 'Bakery_app/home.html')

def catalog(request):
    product = Product.objects.all()
    return render(request, 'Bakery_app/catalog.html', {'product': product})

@staff_required
def dashboard(request):
    products = Product.objects.all()
    return render(request, 'Bakery_app/dashboard.html', {'products': products})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'Bakery_app/login.html', {'error': 'invalid username or password'})
    return render(request, 'Bakery_app/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST.get('confirm_password')

        if not confirm_password:
            return render(request, 'Bakery_app/register.html', {
                'error': 'You have to confirm the password'
            })

        if password != confirm_password:
            return render(request, 'Bakery_app/register.html', {
                'error': 'The passwords do not match'
            })
        
        if User.objects.filter(username=username).exists():
            return render(request, 'Bakery_app/register.html', {
                'error': 'The user already exist'
            })

        user = User.objects.create_user(username=username, password=password)
        user.is_staff = False
        user.is_superuser = False
        user.save()

        return redirect('login')
    return render(request, 'Bakery_app/register.html')

@staff_required
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        stock = int(request.POST.get('stock'))

        Product.objects.create(
            name=name,
            price=price,
            image=image,
            stock=stock
        )

        return redirect('dashboard')
    return render(request, 'Bakery_app/add_product.html')

def catalog(request):
    products = Product.objects.all()
    return render(request, 'Bakery_app/catalog.html', {'products': products})

@staff_required
def edit_product(request, id):
    product = Product.objects.get(id=id)

    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.stock = request.POST.get('stock')

        if request.FILES.get('image'):
            product.image = request.FILES.get('image')

        product.save()
        return redirect('dashboard')
        
    return render(request, 'Bakery_app/edit_product.html', {'product': product})

@staff_required
def delete_product(request, id):
    product = Product.objects.get(id=id)

    if request.method == 'POST':
        product.delete()
        return redirect('dashboard')
    
    return redirect('dashboard')

def add_to_cart(request, id):
    cart = request.session.get('cart', {})

    if str(id) in cart:
        cart[str(id)]['quantity'] += 1
    else:
        product = Product.objects.get(id=id)

        cart[str(id)] = {
            'name': product.name,
            'price': float(product.price),
            'quantity': 1
        }
    
    request.session['cart'] = cart
    messages.success(request, 'Product added to the cart')
    return redirect('catalog')

def delete_to_cart(request, id):
    cart = request.session.get('cart', {})

    if str(id) in cart:
        del cart[str(id)]

    request.session['cart'] = cart
    messages.success(request, 'Product deleted to the cart')
    return redirect('catalog')

def cart_view(request):
    cart = request.session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart.values())

    return render(request, 'Bakery_app/cart.html', {
        'cart': cart,
        'total': total
    })

def remove_product(request, id):
    cart = request.session.get('cart', {})

    if str(id) in cart:
        cart[str(id)]['quantity'] -= 1

        if cart[str(id)]['quantity'] <= 0:
            del cart[str(id)]
    
    request.session['cart'] = cart
    messages.success(request, 'Product removed to the cart')
    return redirect('catalog')

def empty_cart(request):
    request.session['cart'] = {}
    messages.success(request, 'Empty cart')
    return redirect('catalog')

@login_required
def checkout(request):
    cart = request.session.get("cart", {})

    if not cart:
        return redirect("catalog")

    order = Order.objects.create(user=request.user, status="pending")

    token = os.getenv("MP_ACCESS_TOKEN")

    if not token:
        raise ValueError("Error with Mercado Pago token")
    
    sdk = mercadopago.SDK(token)

    items = []
    for key, item in cart.items():
        items.append({
            'title': item['name'],
            'quantity': item['quantity'],
            'unit_price': float(item['price'])
        })

    preference_data = {
        "items": items,
        "external_reference": str(order.id),
        "back_urls": {
            "success": "http://127.0.0.1:8000/success/",
            "failure": "http://127.0.0.1:8000/failure/",
            "pending": "http://127.0.0.1:8000/pending/"
        }
    }

    preference_response = sdk.preference().create(preference_data)
    preference = preference_response['response']

    if "response" not in preference_response:
        return HttpResponse("Error Mercado Pago")

    preference = preference_response["response"]

    if "init_point" not in preference:
        return HttpResponse(f"Error: {preference}")
    return redirect(preference['init_point'])

def generate_invoice(request, id):
    order = Order.objects.get(id=id)
    items = ItemOrder.objects.filter(order=order)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{id}.pdf"'

    doc = SimpleDocTemplate(response)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph(f"Invoice Order #{order.id}", styles["Title"]))

    for item in items:
        text = f"{item.product.name} - {item.quantity} x ${item.price}"
        content.append(Paragraph(text, styles["Normal"]))

    content.append(Paragraph(f"Total: ${order.total_calculated}", styles["Heading2"]))

    doc.build(content)

    return response

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'Bakery_app/my_orders.html', {'orders': orders})

def success(request):
    status = request.GET.get("status")
    order_id = request.GET.get("external_reference")

    if not order_id:
        return redirect("catalog")

    order = Order.objects.get(id=order_id)

    if status == "approved":
        order.status = "approved"
        request.session["cart"] = {}
    else:
        order.status = "pending"

    order.save()

    return render(request, "success.html", {"order": order})

def failure(request):
    return render(request, "Bakery_app/failure.html")

def pending(request):
    return render(request, "Bakery_app/pending.html")