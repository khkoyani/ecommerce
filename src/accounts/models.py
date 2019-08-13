from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class Guest(models.Model):
    email = models.EmailField(unique=False)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)



class UserManager(BaseUserManager):
    def create_user(self, email, password=None, active=True, staff=False, admin=False):
        if not email:
            raise ValueError('Email is required')

        if not password:
            raise ValueError('Password is required')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.active = active
        user.staff = staff
        user.admin = admin

        user.save(using=self._db)
        return user

    def create_staff(self, email, password=None):
        return self.create(email, password=password, staff=True)

    def create_superuser(self, email, password=None):
        return self.create(email, password=password, staff=True, admin=True)


class User(AbstractBaseUser):
    email = models.EmailField(max_length=254, unique=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_fullname(self):

        return self.email

    def get_shortname(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_active(self):
        return self.active

    @property
    def is_admin(self):
        return self.admin
# Create your models here.
