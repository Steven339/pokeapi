from celery import shared_task

from pokemons.models import Pokemon, PokemonStat


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
