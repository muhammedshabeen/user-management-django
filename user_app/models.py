from django.db import models
from django.contrib.auth.models import AbstractUser
from core.managers import CustomUserManager


class CustomUser(AbstractUser):    
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    USER_CHOICES = [
        ('Admin', 'Admin'),
        ('User', 'User'),
    ]
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100,unique=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=10)
    d_o_b = models.DateField(null=True)
    gender = models.CharField(max_length=15,choices=GENDER_CHOICES)
    user_type = models.CharField(max_length=15,choices=USER_CHOICES,default='Admin')
    image = models.FileField(upload_to='profile')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()