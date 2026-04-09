from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'Bakery_app/home.html')

def catalog(request):
    return render(request, 'Bakery_app/catalog')

@login_required
def dashboard(request):
    return render(request, 'Bakery_app/dashboard.html')

def login(request):
    return render(request, 'Bakery_app/login.html')