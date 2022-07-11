from celery import shared_task

from evolutions.models import Evolution, EvolutionChain
from pokemons.tasks import create_pokemon_from_evolution
from species.models import Specie


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
                        name=evolution_specie_obj_depth.name,
                        evolution_type=Evolution.EVOLUTION_TYPE_CHOICES[1]
                    ))
                    evolves_to = evolution_depth['evolves_to']

            evolution_list.append(Evolution(
                evolution_chain=chain_obj,
                specie=evolution_specie_obj,
                external_id=evolution_specie_obj.id,
                name=evolution_specie_obj.name,
                evolution_type=Evolution.EVOLUTION_TYPE_CHOICES[0]
            ))
        Evolution.objects.bulk_create(evolution_list)
