from django.db import models
from django.db.models import Sum
from django.contrib import admin
import uuid
from decimal import Decimal
from django.contrib.auth.models import User
from clientes.models import ClientesModel
from contratos.models import ContratosModel
from centroscustos.models import CentroCustosModel
from previsoes.models import PrevisoesModel
from lancamentos.models import LancamentosModel

# Create your models here.
class ObrasModel(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Usuário responsável')
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255, verbose_name='Título da obra', blank=False, null=False)
    observacoes = models.TextField(blank=True, verbose_name='Observações', null=True)
    status = models.BooleanField(default=True, verbose_name='Status da obra')
    cliente = models.ForeignKey(ClientesModel, on_delete=models.CASCADE, related_name='obras_cliente')
    contrato = models.ForeignKey(ContratosModel, on_delete=models.CASCADE, related_name='obras_contrato')
    centrocusto = models.ForeignKey(CentroCustosModel, on_delete=models.CASCADE, related_name='obras_centrocustos')
    endereco = models.CharField(max_length=255, blank=True, null=True, verbose_name='Endereço da obra')
    inicio_obra = models.DateField(blank=True, null=True, verbose_name='Data do início da obra')
    fim_obra = models.DateField(blank=True, null=True, verbose_name='Data da conlusão da obra')
    previsao = models.DateField(blank=True, null=True, verbose_name='Data prevista para o fim da obra')
    obra_finalizada=models.BooleanField(default=False)
    despesa_total = models.DecimalField(max_digits=13, decimal_places=2, default=Decimal('0.00'),
                                        verbose_name='Despesa Total',
                                        blank=True)
    def __str__(self):
        return self.nome
    def acumulado(self):
        total = 0
        qs = LancamentosModel.objects.filter(status=True, centro_custos=self.centrocusto)
        for i in qs:
            total+=i.valor_final
        return total
    class Meta:
        verbose_name = 'Obra'
        verbose_name_plural = 'Obras'

class LancamentosObrasModel(models.Model):
    obra = models.ForeignKey(ObrasModel, on_delete=models.CASCADE, related_name='obra_lancamento')
    lancamento = models.ForeignKey(LancamentosModel, on_delete=models.CASCADE, related_name='lancamento_obra')
    def __str__(self):
        return self.lancamento.descricao
        #return str ("{} do contrato {} e cliente {}".format(self.obra.nome, self.obra.contrato.titulo, self.obra.cliente.nome))
    def valor_previsao(self):
        total = 0
        for i in PrevisoesModel.objects.filter(status=True, centro_custos=self.centrocusto):
            total+= i.valor
            return total
    def valor_lancado(self):
        total=0
        for i in LancamentosModel.objects.filter(status=True, lancamentos_previsoes__previsao__centro_custos=self.centrocusto):
            total+=i.valor_final
            return total
class ObrasAdmin(admin.ModelAdmin):
    list_display = ['nome', 'uuid']
admin.site.register(ObrasModel, ObrasAdmin)