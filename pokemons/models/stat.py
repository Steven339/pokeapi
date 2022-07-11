from django.db import models

from pokemonApi.auditors import ModelAuditor


class PokemonStat(ModelAuditor):
    base_stat = models.IntegerField()
    effort = models.IntegerField()
    name = models.CharField(max_length=25)

    def __str__(self):
        return f'{self.name} - base:{self.base_stat} - effort:{self.effort}'
