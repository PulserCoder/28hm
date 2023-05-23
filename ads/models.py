from django.db import models


class Ads(models.Model):
    Id = models.IntegerField(primary_key=True)
    STATUS_CHOICES = [
        (True, 'Опубликовано'),
        (False, 'Не опубликовано')
    ]
    name = models.CharField(max_length=50)
    author = models.CharField(max_length=60)
    price = models.IntegerField()
    description = models.TextField()
    address = models.CharField(max_length=100)
    is_published = models.BooleanField(default=False, choices=STATUS_CHOICES)


class Categories(models.Model):
    name = models.CharField(max_length=50)