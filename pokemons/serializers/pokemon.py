# Serializers define the API representation.
from rest_framework import serializers


class PokemonStatsSerializer(serializers.Serializer):
    base_stat = serializers.IntegerField()
    effort = serializers.IntegerField()
    name = serializers.CharField()


class PokemonSerializer(serializers.Serializer):
    name = serializers.CharField()
    weight = serializers.CharField()
    height = serializers.CharField()
    external_id = serializers.CharField()
    specie = serializers.CharField()
    stats = PokemonStatsSerializer(many=True)
