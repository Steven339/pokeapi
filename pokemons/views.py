from django.shortcuts import render

# Create your views here.
from rest_framework import serializers, views
from rest_framework.response import Response

from evolutions.serializers import EvolutionSerializer
from pokemons.models import Pokemon
from pokemons.serializers.pokemon import PokemonSerializer


class YourSerializer(serializers.Serializer):
    """Your data serializer, define your fields here."""
    comments = serializers.IntegerField()
    likes = serializers.IntegerField()


class PokemonView(views.APIView):
    def get(self, request, pokemon_id):
        pokemon = Pokemon.objects.filter(external_id=pokemon_id).select_related(
            'specie', 'specie__evolution_chain'
        ).prefetch_related('stats', 'specie__evolution_chain__evolution_set').first()
        if pokemon:
            result = PokemonSerializer(pokemon).data
            evolutions = EvolutionSerializer(
                pokemon.specie.evolution_chain.evolution_set.all(),
                many=True
            ).data
            result['evolutions'] = evolutions
            return Response(result)
        return Response(status=404)
