import requests
from celery import chain
from django.core.management.base import BaseCommand

from evolutions.tasks import create_evolution_chain, create_evolutions_from_chain
from species.models import Specie


class Command(BaseCommand):
    help = 'Displays current time'

    def add_arguments(self, parser):
        parser.add_argument('--id', type=int, help='It is a evolution chain id')

    def handle(self, *args, **kwargs):
        evolution_chain_id = kwargs['id']
        result = requests.get(f'https://pokeapi.co/api/v2/evolution-chain/{evolution_chain_id}/').json()
        specie = requests.get(result['chain']['species']['url']).json()
        """Create main chain specie"""
        main_specie_obj, _ = Specie.objects.get_or_create(
            name=specie['name'],
            external_id=specie['id']
        )
        chain(
            create_evolution_chain.s(result, main_specie_obj.id),
            create_evolutions_from_chain.s(result['chain']['evolves_to'])
        ).apply_async()
