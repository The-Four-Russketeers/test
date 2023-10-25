from django.db import models

# Create your models here. This is for database stuff.
class UserInfo(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)