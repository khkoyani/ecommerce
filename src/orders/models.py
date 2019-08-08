from django.db import models
from carts.models import Cart
from product.models import Product

order_status_choices = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),
)

class Order(models.Model):
    order_id = models.CharField(blank=True, max_length=120)
    # billing_profile
    # shipping_address
    # billing_address
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=120, default='created', choices=order_status_choices)
    shipping_total=models.DecimalField(default=5.99, decimal_places=2, max_digits=5)
    order_total = models.DecimalField(default=0.00, decimal_places=2, max_digits=100)



# Create your models here.
