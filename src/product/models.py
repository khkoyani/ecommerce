from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class Product(models.Model):
    title = models.CharField(max_length=120, verbose_name='product_name', unique=False)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(db_index=True, null=True, blank=True, unique=True)

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
