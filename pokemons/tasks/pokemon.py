import requests
from celery import chain, shared_task

from pokemons.models import Pokemon
from .stats import create_pokemon_stats
from species.models import Specie


def create_pokemon_from_evolution(evolution):
    evolution_specie = requests.get(evolution['species']['url']).json()
    evolution_specie_obj, _ = Specie.objects.get_or_create(
        name=evolution_specie['name'],
        external_id=evolution_specie['id']
    )

    """Create pokemon from specie"""
    for variety in evolution_specie['varieties']:
        pokemon = requests.get(variety['pokemon']['url']).json()
        chain(
            create_pokemon.s(pokemon, evolution_specie_obj.id),
            create_pokemon_stats.s(pokemon['stats'])
        ).apply_async()

    return evolution_specie_obj


@shared_task
def create_pokemon(pokemon, evolution_specie_obj_id):
    evolution_specie_obj = Specie.objects.filter(pk=evolution_specie_obj_id).first()
    pokemon_obj = None
    if evolution_specie_obj:
        pokemon_obj = Pokemon.objects.create(
            name=pokemon['name'],
            weight=pokemon['weight'],
            height=pokemon['height'],
            external_id=pokemon['id'],
            specie=evolution_specie_obj
        )
    return pokemon_obj.id
