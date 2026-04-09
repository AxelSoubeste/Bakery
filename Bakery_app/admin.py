from django.contrib import admin
from .models import Catalog

# Register your models here.
@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price')