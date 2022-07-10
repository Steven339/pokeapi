from django.shortcuts import render

# Create your views here.
from rest_framework import serializers, views
from rest_framework.response import Response

from evolutions.serializers import EvolutionSerializer
from evolutions.serializers.evolution_chain import EvolutionChainSerializer
from pokemons.models import Pokemon
from pokemons.serializers.pokemon import PokemonSerializer


class YourSerializer(serializers.Serializer):
    """Your data serializer, define your fields here."""
    comments = serializers.IntegerField()
    likes = serializers.IntegerField()


class PokemonView(views.APIView):
    def get(self, request, pokemon_id):
        pokemon = Pokemon.objects.filter(external_id=pokemon_id).select_related(
            'specie'
        ).prefetch_related(
            'stats', 'specie__evolution_set', 'specie__evolution_set__evolution_chain'
        ).first()
        if pokemon:
            result = PokemonSerializer(pokemon).data
            evolution_chain_obj = pokemon.specie.evolution_set.first().evolution_chain
            evolution_chain = EvolutionChainSerializer(evolution_chain_obj).data
            evolutions = EvolutionSerializer(
                evolution_chain_obj.evolution_set,
                many=True
            ).data
            result['evolution_chain'] = evolution_chain
            result['evolution_chain']['evolutions'] = evolutions
            return Response(result)
        return Response(status=404)
