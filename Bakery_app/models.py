from django.db import models

class Catalog(models.Model):
    product_name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.product_name