from django.db import models
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.models import User

# Create your models here.
class service_call(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    details = models.TextField(max_length=500)
