from django.db import models
from toilet.models import Toilet
from django.contrib.auth.models import User


class Rating(models.Model):

    user        = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    toilet      = models.ForeignKey(Toilet, on_delete=models.CASCADE, default=None)

    tidiness    = models.IntegerField(default=0)
    space       = models.IntegerField(default=0)
    smell       = models.IntegerField(default=0)
    design      = models.IntegerField(default=0)
    rating      = models.FloatField(default=0)