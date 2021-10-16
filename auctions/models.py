from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Auctions(models.Model):
    pass


class Bid(models.Model):
    pass


class Comments(models.Model):
    pass


class Categories(models.Model):
    pass
