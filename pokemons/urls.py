from django.urls import path

from pokemons.views import PokemonView

urlpatterns = [
    path('<int:pokemon_id>/', PokemonView.as_view(), name='pokemon')
]
