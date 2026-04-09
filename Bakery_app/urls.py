from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
]