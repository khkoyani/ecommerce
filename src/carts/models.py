from django.db import models
from django.conf import settings
from product.models import Product
from django.db.models.signals import pre_save, m2m_changed

User = settings.AUTH_USER_MODEL

class CartManager(models.Manager):
    def new(self, user):
        user_obj = None
        if user is not None and user.is_authenticated:
            user_obj = user
        return self.get_queryset().create(user=user_obj)

    def first(self):
        return self.get_queryset().all().first()

    def get_or_new(self, request):
        cart_id = request.session.get('cart_id', None)
        # it was qs=Cart.objects.filter now its self.getqueryset
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj=False
            cart_obj = qs.first()
            if cart_obj.user is None and request.user.is_authenticated:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            # was cart.objects.new now its self.new
            cart_obj = self.new(user=request.user)
            new_obj=True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj




class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)
    subtotal = models.DecimalField(default=0.00, max_digits=50, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=50, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)

def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    if action=='post_add' or action=='post_remove' or action=='post_clear':
        products = instance.products.all()
        total = 0
        for item in products:
            total += item.price
        instance.subtotal = total
        instance.save()
m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)

def pre_save_cart_receiver(sender, instance, *arags, **kwargs):
    total = instance.subtotal + 10
    instance.total = total
pre_save.connect(pre_save_cart_receiver, sender=Cart)

