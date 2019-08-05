from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=120, verbose_name='product_name', unique=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title
# Create your models here.
