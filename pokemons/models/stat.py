from django.db import models

from pokemonApi.auditors import ModelAuditor
from pokemons.models.pockemon import Pokemon


class StatBase(ModelAuditor):
    base_stat = models.IntegerField()
    effort = models.IntegerField()
    name = models.CharField(max_length=25)

    class Meta:
        abstract = True


class PokemonStat(StatBase):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='stats')
