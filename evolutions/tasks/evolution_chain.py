import requests
from celery import shared_task, chain

from evolutions.models import Evolution, EvolutionChain
from pokemons.models import Pokemon, PokemonStat
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
def create_evolution_chain(evolution_chain, main_specie_obj_id):
    main_specie_obj = Specie.objects.filter(pk=main_specie_obj_id).first()
    chain_obj = None
    if main_specie_obj:
        """Create evolution chain"""
        chain_obj = EvolutionChain.objects.create(
            external_id=evolution_chain['id'],
            specie=main_specie_obj,
            is_baby=evolution_chain['chain']['is_baby']
        )
    return chain_obj.id


@shared_task
def create_evolutions_from_chain(chain_obj_id, evolves_to):
    chain_obj = EvolutionChain.objects.filter(pk=chain_obj_id).first()
    if chain_obj:
        evolution_list = []
        for evolution in evolves_to:
            evolution_specie_obj = create_pokemon_from_evolution(evolution)
            evolves_to = evolution['evolves_to']

            while len(evolves_to) > 0:
                for evolution_depth in evolves_to:
                    evolution_specie_obj_depth = create_pokemon_from_evolution(evolution_depth)
                    evolution_list.append(Evolution(
                        evolution_chain=chain_obj,
                        specie=evolution_specie_obj_depth,
                        external_id=evolution_specie_obj_depth.id,
                        name=evolution_specie_obj_depth.name
                    ))
                    evolves_to = evolution_depth['evolves_to']

            evolution_list.append(Evolution(
                evolution_chain=chain_obj,
                specie=evolution_specie_obj,
                external_id=evolution_specie_obj.id,
                name=evolution_specie_obj.name
            ))
        Evolution.objects.bulk_create(evolution_list)


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


@shared_task
def create_pokemon_stats(pokemon_obj_id, stats):
    pokemon_obj = Pokemon.objects.filter(pk=pokemon_obj_id).first()
    if pokemon_obj:
        stat_list = []
        for stat in stats:
            stat_obj, _ = PokemonStat.objects.get_or_create(
                base_stat=stat['base_stat'],
                effort=stat['effort'],
                name=stat['stat']['name']
            )
            stat_list.append(stat_obj.id)
        if len(stat_list) > 0:
            pokemon_obj.stats.add(*stat_list)
