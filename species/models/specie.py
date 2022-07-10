from django.db import models

from pokemonApi.auditors import ModelAuditor


class Specie(ModelAuditor):
    name = models.CharField(max_length=10)
    external_id = models.IntegerField()

    def __str__(self):
        return f'{self.name} - {self.external_id}'

    @property
    def evolution_chain(self):
        return self.evolutionchain_set.first()
