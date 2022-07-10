from django.test import TestCase

# Create your tests here.
from .models import Evolution


class EvolutionTests(TestCase):
    evolution_case_1 = {
        ""
    }
    def setUp(self) -> None:
        Evolution.objects.create(

        )
