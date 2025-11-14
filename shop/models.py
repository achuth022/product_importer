from django.db import models


class Product(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.sku} - {self.name}"
