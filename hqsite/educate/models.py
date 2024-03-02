from django.db import models
from django.contrib.auth.models import User

from django.conf import settings


class Product(models.Model):
    author = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    time_start = models.DateTimeField()
    price = models.FloatField(default=0)
    min_students = models.SmallIntegerField(default=0)
    max_students = models.SmallIntegerField(default=0)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='products', blank=True) # у одного
    # продукта может быть много пользователей, у одного пользователя может быть много продуктов

    def __str__(self):
        return self.name

class Group(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='group_members', blank=True) # у одной
    # группы может быть несоклько пользователе, и у одного пользователя может быть несколько групп,
    # но из разных продкутов только

    def __str__(self):
        return self.name

class Lesson(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    video = models.CharField(max_length=511)

    def __str__(self):
        return self.name
