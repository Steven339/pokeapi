from django.contrib import admin

# Register your models here.
from evolutions.models.evolution import EvolutionChain, Evolution

admin.site.register(EvolutionChain)
admin.site.register(Evolution)
