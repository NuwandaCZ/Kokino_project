from django.db import models
from django.contrib.auth.models import User


class Toilet(models.Model):

    CATEGORY = (
        ('Restaurant', 'Restaurant'),
        ('Public', 'Public'),
        ('Hotel', 'Hotel'),
    )
    id          = models.IntegerField(primary_key=True, auto_created=True)
    category    = models.CharField(max_length=120, null=False, choices=CATEGORY, default=None)
    place       = models.CharField(max_length=120)
    tidiness    = models.IntegerField()
    space       = models.IntegerField()
    smell       = models.IntegerField()
    design      = models.IntegerField()
    rating      = models.FloatField(default=0)
    users       = models.ManyToManyField(User)

    def __str__(self):
        return self.place
