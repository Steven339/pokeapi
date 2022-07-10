from django.db import models

from pokemonApi.auditors import ModelAuditor


class EvolutionChain(ModelAuditor):
    is_baby = models.BooleanField(default=False)
    external_id = models.IntegerField()
    specie = models.ForeignKey('species.Specie', on_delete=models.CASCADE)


class EvolutionBase(ModelAuditor):
    evolution_type = models.CharField(max_length=25)
    name = models.CharField(max_length=25)

    class Meta:
        abstract = True


class Evolution(EvolutionBase):
    evolution_chain = models.ForeignKey(EvolutionChain, on_delete=models.CASCADE)
    external_id = models.IntegerField()
    specie = models.ForeignKey('species.Specie', on_delete=models.CASCADE)
