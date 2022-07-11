from django.test import TestCase

from evolutions.models import EvolutionChain, Evolution
from evolutions.tasks import create_evolution_chain
from .cases import CASE_1, SPECIE_1, POKEMON_1, STATS_1
from pokemons.models import Pokemon, PokemonStat
from pokemons.tasks import create_pokemon, create_pokemon_stats
from species.models import Specie


class EvolutionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.case_1 = CASE_1
        cls.specie_1 = SPECIE_1
        cls.pokemon_1 = POKEMON_1
        cls.stats_1 = STATS_1
        cls.main_specie = Specie.objects.create(
            external_id=19,
            name='rattata'
        )
        cls.evolution_chain = create_evolution_chain(cls.case_1, cls.main_specie.id)
        cls.evolution_specie_obj, _ = Specie.objects.get_or_create(
            name=cls.specie_1['name'],
            external_id=cls.specie_1['id']
        )
        cls.pokemon_id = create_pokemon(cls.pokemon_1, cls.evolution_specie_obj.id)
        create_pokemon_stats(cls.pokemon_id, cls.stats_1)
        chain_obj = EvolutionChain.objects.filter(pk=cls.evolution_chain).first()
        Evolution.objects.create(
            evolution_chain=chain_obj,
            specie=cls.evolution_specie_obj,
            external_id=cls.evolution_specie_obj.id,
            name=cls.evolution_specie_obj.name
        )

    def test_create_main_specie_and_evolution_chain(self):
        self.assertIsInstance(self.main_specie, Specie)
        self.assertEqual(1, EvolutionChain.objects.all().count())

    def test_create_pokemon_and_their_stats(self):
        self.assertTrue(Pokemon.objects.all().count() > 0)
        self.assertEqual(PokemonStat.objects.filter(pokemon__id=self.pokemon_id).count(), 6)

    def test_create_evolution_from_pokemon(self):
        self.assertEqual(Evolution.objects.all().count(), 1)
        self.assertEqual(Evolution.objects.first().name, self.evolution_specie_obj.name)
