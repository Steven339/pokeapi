from django.db import models

from pokemonApi.auditors import ModelAuditor


class PokemonBase(ModelAuditor):
    name = models.CharField(max_length=15)
    weight = models.FloatField(default=0)
    height = models.FloatField(default=0)

    class Meta:
        abstract = True


class Pokemon(PokemonBase):
    external_id = models.IntegerField()
    specie = models.ForeignKey('species.Specie', on_delete=models.CASCADE)
    stats = models.ManyToManyField('pokemons.PokemonStat')

    def __str__(self):
        return f'{self.id}:{self.name}:{self.specie.name}'
