from django.db import models


class Toilet(models.Model):

    CATEGORY = (
        ('Restaurant', 'Restaurant'),
        ('Public', 'Public'),
        ('Hotel', 'Hotel'),
    )

    category    = models.CharField(max_length=120, null=False, choices=CATEGORY, default=None)
    place       = models.CharField(max_length=120)

    overal_tidiness    = models.FloatField(default=0)
    overal_space       = models.FloatField(default=0)
    overal_smell       = models.FloatField(default=0)
    overal_design      = models.FloatField(default=0)

    overal_rating      = models.FloatField(default=0)

    def __str__(self):
        return self.place
