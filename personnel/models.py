"""
Models for personnel.
"""
# pylint: disable=E5142
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    """
    Add information for User.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    # Not knowing if it is correct.
    tel = models.CharField(max_length=12)
    gender = models.CharField(max_length=2)
    birth = models.DateTimeField()
    #Add more
