from rest_framework import serializers


class EvolutionSeralizer(serializers.Serializer):
    evolution_type = serializers.CharField()
    external_id = serializers.IntegerField()
    name = serializers.CharField()