from django.db import models


class Specie(models.Model):
    external_id = models.IntegerField()
    name = models.CharField(max_length=10)
