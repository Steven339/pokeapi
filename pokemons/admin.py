from django.contrib import admin

# Register your models here.
from pokemons.models import Pokemon, PokemonStat


admin.site.register(Pokemon)
admin.site.register(PokemonStat)

