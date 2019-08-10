from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from accounts.models import Guest

User = settings.AUTH_USER_MODEL
class BillingManager(models.Manager):
    def get_or_new(self, request):
        user=request.user
        guest_id = request.session.get('guest_id')
        created=False
        obj = None
        if user.is_authenticated and user.email:
            obj, created = self.get_queryset().get_or_create(user=user, email=user.email)
        elif guest_id is not None:
            guest_obj = Guest.objects.get(id=guest_id)
            obj, created = self.get_queryset().get_or_create(email=guest_obj.email)
        return obj, created

class BillingProfile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    email = models.EmailField()
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = BillingManager()

    def __str__(self):
        return self.email
# Create your models here.

def post_save_user_create_billing(instance, sender, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)
post_save.connect(post_save_user_create_billing, sender=User)