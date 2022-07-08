from django.db import models

from pokemons.models.pockemon import Pokemon
from pokemons.models.stat_base import StatBase


class PokemonStat(StatBase):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
