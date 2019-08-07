from django.db import models
from django.db.models.signals import pre_save
from product.utils import unique_slug_generator
from product.models import Product
from django.dispatch import receiver
from django.urls import reverse

class Tag(models.Model):
    title=models.CharField(max_length=120, unique=True)
    slug=models.SlugField(unique=True, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    products = models.ManyToManyField(Product, blank=True)
    exclusive = models.BooleanField(default=False)

    def __str__(self):
        return self.title


@receiver(pre_save, sender=Tag)
def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
