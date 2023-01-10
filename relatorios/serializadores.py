from rest_framework import serializers
from lancamentos.models import LancamentosModel
from centroscustos.models import CentroCustosModel
from previsoes.models import PrevisoesModel

class CentrosCustosSerializadores(serializers.ModelSerializer):
    lancamentos_centrocusto=serializers.StringRelatedField(many=True)
    class Meta:
        model = CentroCustosModel
        fields = ['titulo', 'descricao', 'lancamentos_centrocusto']

class LancamentosSerializadores(serializers.ModelSerializer):
    class Meta:
        model=LancamentosModel
        fields=['descricao', 'pk']