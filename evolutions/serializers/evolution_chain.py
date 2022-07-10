from rest_framework import serializers


class EvolutionChainSerializer(serializers.Serializer):
    external_id = serializers.IntegerField()
    specie = serializers.CharField()
