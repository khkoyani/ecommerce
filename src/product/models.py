from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.http import Http404
from .utils import unique_slug_generator, upload_image_path
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.db.models import Q

class Extended_QuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True, active=True)

    def search(self, query):
        lookups = (Q(title__icontains=query) | Q(description__icontains=query) | Q(price__icontains=query) |
                   Q(tag__title__icontains=query)
                   )
        return self.filter(lookups).distinct()

# if tag is a foriegn field instead of a field like title then do like as follows
# Q(tag__title__icontains=query) NOTE: its not tag__set__title


#     def get_obj_by_slug
class ProductManager(models.Manager):
    def get_queryset(self):
        return Extended_QuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().all()
    # normally .all has to be called on a queryset object. but defining the method in
    # the model manager like this will allow to be called as Product.objects.all
    def get_objects_by_slug(self, slug):
        return self.get_queryset().filter(slug=slug) or None

    def get_single_object_by_slug (self, slug):
        qs = self.get_objects_by_slug(slug)
        if qs is None:
            raise Http404('Object not found')
        if qs.count() > 1:
            raise Http404(f'Multiple objects for slug "{qs.first.slug}"')
        return qs.first()

    def search(self, query):
        return self.get_queryset().search(query)




class Product(models.Model):
    title = models.CharField(max_length=120, verbose_name='product_name', unique=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(db_index=True, null=True, blank=True, unique=True)
    image = models.ImageField(upload_to=upload_image_path, blank=True, null=True)
    feature = models.BooleanField(default=False)

    objects = ProductManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product:detail', kwargs={'slug': self.slug})


@receiver(pre_save, sender=Product)
def product_pre_save_receiver(sender, instance, *args, **kwargs):
    print(f' args = {args}')
    print(f' kwargs = {kwargs}')
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

# pre_save.connect(product_pre_save_receiver, sender=Product)

