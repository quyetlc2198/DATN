from datetime import date

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
# model signup user
from hotel.models import Categories
from IT4995 import settings  # <- Change to match your main app name


class Signup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=20, default='')
    def __str__(self):
        return self.user.username


class Comments(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    evaluation = models.CharField(max_length=200, default='')
    comment = models.CharField( max_length=200 , null=False, default="good")
    create_date = models.DateField( default= date.today())

    def __str__(self):
        return self.user.username + ' comment: ' + self.category.name