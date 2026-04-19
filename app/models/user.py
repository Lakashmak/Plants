from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
# from .managers import CustomUserManager

# class CustomUserManager(models.Manager):

class User(models.Model): # AbstractBaseUser, PermissionsMixin
    name = models.CharField(max_length=100)
    status = models.IntegerField()
    phone_number = models.CharField(max_length=11)
    email = models.CharField(max_length=100)
    delivery_address = models.TextField()
    password_hash = models.CharField(max_length=256)
    last_login = models.DateTimeField(null=True, blank=True)


    # objects = CustomUserManager()

    # USERNAME_FIELD = 'email'

    # REQUIRED_FIELDS = ['name']

