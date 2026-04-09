from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'Bakery_app/home.html')

def catalog(request):
    return render(request, 'Bakery_app/catalog')