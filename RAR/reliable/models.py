from django.db import models
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.models import User

# Create your models here.
class service_call(models.Model):
    username=models.CharField(max_length=20)
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    details = models.TextField(max_length=500)
    timemade = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.timemade}]: {self.fname} {self.lname} ({username})"
