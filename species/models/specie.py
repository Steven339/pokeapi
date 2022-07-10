from django.db import models

from pokemonApi.auditors import ModelAuditor


class Specie(ModelAuditor):
    name = models.CharField(max_length=10)
    external_id = models.IntegerField()
    evolution_chain = models.ForeignKey(
        'evolutions.EvolutionChain',
        on_delete=models.CASCADE,
        related_name='evolution_chain'
    )

    def __str__(self):
        return f'{self.name} - {self.external_id}'
