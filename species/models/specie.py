from django.db import models

from pokemonApi.auditors import ModelAuditor


class SpecieBase(ModelAuditor):
    name = models.CharField(max_length=10)


class Specie(SpecieBase):
    external_id = models.IntegerField()
