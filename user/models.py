from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class User(models.Model):
    phone = PhoneNumberField(blank=False)
    address = models.TextField(blank=False)
    email = models.EmailField(blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)