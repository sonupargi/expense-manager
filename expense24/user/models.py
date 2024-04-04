from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    salary = models.FloatField(null=True, blank=True)
    is_user = models.BooleanField(default=True)
    pic = models.ImageField(upload_to="avatars/",null=True , blank=True)
    
    class Meta:
        db_table = 'user'
        