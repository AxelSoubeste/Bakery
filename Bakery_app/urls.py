from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_user, name='register'),
    path('add-product', views.add_product, name='add_product'),
    path('edit-product/<int:id>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:id>/', views.delete_product, name='delete_product'),
    path('add-to-cart/<int:id>', views.add_to_cart, name='add_to_cart'),
    path('delete-to-cart/<int:id>', views.delete_to_cart, name='delete_to_cart'),
    path('cart-view', views.cart_view, name='cart_view'),
    path('remove-product/<int:id>', views.remove_product, name='remove_product'),
    path('empty-cart/', views.empty_cart, name='empty_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('success/', views.success, name='success'),
    path('failure/', views.failure, name='failure'),
    path('pending/', views.pending, name='pending'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)