from django.db import models

# class User(models.Model):
#     id          = models.IntegerField(primary_key=True)
#     name        = models.CharField(max_length=120)
#     password    = models.CharField(max_length=120)
#
#     def __str__(self):
#         return self.name


class Toilet(models.Model):
    CATEGORY = (
        ('Restaurant', 'Restaurant'),
        ('Public', 'Public'),
        ('Hotel', 'Hotel'),
    )
    id          = models.IntegerField(primary_key=True, auto_created=True)
    category   = models.CharField(max_length=120, null=False, choices=CATEGORY, default=None)
    place       = models.CharField(max_length=120)

    def __str__(self):
        return self.place
