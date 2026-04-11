from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from functools import wraps

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
    return render(request, 'Bakery_app/catalog')

@staff_required
def dashboard(request):
    return render(request, 'Bakery_app/dashboard.html')

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