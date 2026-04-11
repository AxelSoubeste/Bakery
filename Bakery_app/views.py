from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout, login, authenticate

def home(request):
    return render(request, 'Bakery_app/home.html')

def catalog(request):
    return render(request, 'Bakery_app/catalog')

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