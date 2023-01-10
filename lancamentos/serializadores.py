from rest_framework import serializers
from obras.models import ObrasModel


class ListaSerializer(serializers.Serializer):
    pk=serializers.IntegerField()
    nome=serializers.CharField()
