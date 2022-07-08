from django.db import models


class StatBase(models.Model):
    base_stat = models.IntegerField()
    effort = models.IntegerField()
    name = models.IntegerField()

    class Meta:
        abstract = True
