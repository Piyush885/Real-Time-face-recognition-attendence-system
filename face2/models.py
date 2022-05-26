from django.db import models

# from cloudinary.models import CloudinaryField

# Create your models here.
class Register(models.Model):
    name = models.CharField(max_length=30)
    time = models.CharField(max_length=30)
    
def __str__(self):
    return self.studentno
