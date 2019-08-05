from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import random
import os

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext



def upload_image_path(instance, filename):
    print(instance)
    print(filename)
    new_filename = random.randint(1,35464123)
    name, ext = get_filename_ext(filename)
    final_filename = f'{new_filename}{ext}'
    return f'product/{new_filename}/{final_filename}'

class ProductManager(models.Manager):
    '''extends model manager to add method to get by slug'''
    def get_by_slug(self, slug):
        qs = self.get_queryset().filter(slug=slug)
        if qs.count() ==1:
            return qs.first()

class Product(models.Model):
    title = models.CharField(max_length=120, verbose_name='product_name', unique=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to=upload_image_path, blank=True, null=True)
    slug = models.SlugField(db_index=True)
    
    objects = ProductManager()

    def __str__(self):
        return self.title

    def get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while self.objects.filter(slug=unique_slug).exists:
            unique_slug = f'{unique_slug}-{num}'
            num+=1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_unique_slug()
        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'slug': self.slug})

