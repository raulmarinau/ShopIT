from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User


class Saved_Product(models.Model):
    name = models.TextField()
    link = models.TextField()
    retailer = models.TextField()

    def __str__(self):
        return self.name


class Saved_Product_Info(models.Model):
    price = models.FloatField()
    old_price = models.FloatField()
    date = models.DateTimeField(default=timezone.now)
    product_base = models.ForeignKey('Saved_Product', on_delete=models.CASCADE, related_name='infos')

    def __str__(self):
        return self.product_base.name


class CustomUser_NestedField(models.Model):
    user = models.TextField()
    product_base = models.ForeignKey('Saved_Product', on_delete=models.CASCADE, related_name='users')

    def __str__(self):
        return self.user

