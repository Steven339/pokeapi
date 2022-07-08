from django.db import models


class PokemonBase(models.Model):
    name = models.CharField(max_length=15)
    weight = models.FloatField(default=0)
    height = models.FloatField(default=0)

    class Meta:
        abstract = True
