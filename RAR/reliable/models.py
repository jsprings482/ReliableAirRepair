from django.db import models

# Create your models here.
class service(models.Model):
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    details = models.CharField(max_length=500)
    timemade = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timemade}"
