from django.db import models
import uuid
from django.contrib.auth.models import User
from django.contrib import admin
from contas.models import ContasModel
import datetime
#from previsoes.models import ParcelasModel
# Create your models here.
class PlanosContaModel(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Usuário responsável')
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    titulo = models.CharField(max_length=30, null=True, blank=False, verbose_name='Título do plano de contas')
    descricao = models.CharField(max_length=200, null=True, blank=True, verbose_name='Descrição do plano de contas')
    status = models.BooleanField(default=True, verbose_name='Plano de ativo')
    data_registro = models.DateTimeField(auto_now=True, verbose_name='Data de registro')
    data_atualizacao = models.DateTimeField(null=True, blank=True, verbose_name='Última atualização')

    class Meta:
        verbose_name = 'Plano de contas'
        verbose_name_plural = 'Planos de contas'
    def __str__(self):
        return self.titulo

class CentroCustosModel(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Usuário responsável')
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    plano_contas=models.ForeignKey(PlanosContaModel, on_delete=models.CASCADE, related_name='centros_plano')
    titulo = models.CharField(max_length=200, null=True, blank=False, verbose_name='Título do centro de custos')
    descricao = models.CharField(max_length=200, null=True, blank=False, verbose_name='Descrição do centro de custos', help_text="Descrição do centro de custos")
    limite_gastos = models.DecimalField(max_digits=13, decimal_places=2, blank=True, null=True, default=0.00,
                                     verbose_name="Limite de gastos mensais")
    status = models.BooleanField(default=True, verbose_name='Centro de custos ativo')
    data_registro = models.DateTimeField(auto_now=True, verbose_name='Data de registro')
    data_atualizacao = models.DateTimeField(null=True, blank=True, verbose_name='Última atualização')
    bloqueado=models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Centro de custos'
        verbose_name_plural = 'Centros de custos'
    def __str__(self):
        return self.titulo

    def acumulado_mes(self):
        total=0
        #qs=self.previsoes_centrocusto.prefetch_related('parcelas_previsao').filter(parcelas_previsao__status=True, parcelas_previsao__data_vencimento__month=datetime.datetime.now().month).values('parcelas_previsao__valor')
        qs=self.lancamentos_centrocusto.filter(data_pagamento__month=datetime.datetime.now().month).values('valor_final')
        for i in qs:
            total+=i['valor_final']
        return total


class CentroCustosHistoricoModel(models.Model):
    data_registro = models.DateTimeField(auto_now=True, verbose_name='Data de registro')
    icone = models.CharField(max_length=20, blank=True, null=True, default='query_builder')
    descricao = models.TextField(blank=False, null=False)
    class Meta:
        verbose_name = 'Histórico centro de custos'
        verbose_name_plural = 'Históricos centro de custos'
    def __str__(self):
        return str("{} em {}".format(self.descricao, self.data_registro))

admin.site.register(PlanosContaModel)

admin.site.register(CentroCustosModel)