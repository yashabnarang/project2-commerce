from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listings(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    seller = models.CharField(max_length=64)
    winner = models.CharField(max_length=64, default=None, blank=True, null=True)
    category = models.CharField(max_length=64)
    starting_bid = models.IntegerField()
    image_url = models.URLField(max_length=200, default=None, blank=True, null=True)
    active = models.BooleanField(default=True)


class Watchlist(models.Model):
    watcher = models.CharField(max_length=64)
    listing_id = models.IntegerField()


class Bids(models.Model):
    bid = models.IntegerField()
    listing_id = models.IntegerField()
    user = models.CharField(max_length=64)

class Comments(models.Model):
    comment = models.CharField(max_length=64)
    listing_id = models.IntegerField()
    user = models.CharField(max_length=64)
    posting_time = models.CharField(max_length=64)


class Categories(models.Model):
    category = models.CharField(max_length=64)
