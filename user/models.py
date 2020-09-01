from django.db import models


class User(models.Model):
    id          = models.IntegerField(primary_key=True)
    name        = models.CharField(max_length=120)
    password    = models.CharField(max_length=120)

    def __str__(self):
        return self.name
