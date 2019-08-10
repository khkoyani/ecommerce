from django.db import models
from carts.models import Cart
from product.models import Product
from product.utils import unique_order_id_gen
from django.db.models.signals import pre_save, post_save
from decimal import *
from billing.models import BillingProfile

order_status_choices = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),
)

class OrderManager(models.Manager):
    def get_or_new(self, billing_profile, cart_obj):
        created = False
        order_qs = self.get_queryset().filter(billing_profile=billing_profile, cart=cart_obj, active=True)
        if order_qs.count() == 1:
            order_obj = order_qs.first()
        else:
            order_obj = self.get_queryset().create(billing_profile=billing_profile, cart=cart_obj)
            created=True
        return order_obj, created

class Order(models.Model):
    order_id = models.CharField(blank=True, max_length=120)
    billing_profile = models.ForeignKey(BillingProfile, null=True, blank=True, on_delete=models.CASCADE)
    # billing_profile
    # shipping_address
    # billing_address
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=120, default='created', choices=order_status_choices)
    shipping_total = models.DecimalField(default=Decimal(5.00), decimal_places=2, max_digits=10)
    order_total = models.DecimalField(default=Decimal(0.00), decimal_places=2, max_digits=10)
    active = models.BooleanField(default=True)

    objects = OrderManager()
    def __str__(self):
        return self.order_id

    # self.amount = decimal.Decimal(float(amount))
    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        self.order_total = cart_total + shipping_total
        self.save()
        return self.order_total


def pre_save_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_gen(instance)
    qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=False)
pre_save.connect(pre_save_order_id, sender=Order)


def post_save_cart_total(sender, instance, *args, **kwargs):
    order_qs = Order.objects.filter(cart=instance)
    if order_qs.count()==1:
        order = order_qs.first()
        order.update_total()
post_save.connect(post_save_cart_total, sender=Cart)


def post_save_new_order(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_total()
post_save.connect(post_save_new_order, sender=Order)