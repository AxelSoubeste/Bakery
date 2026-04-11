from django.db import models

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.product_name

class User(models.Model):
    id = models.IntegerField(primary_key=True)
    user_name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    password = models.CharField(max_length=128, null=False, blank=False)
    
    def __str__(self):
        return self.user_name