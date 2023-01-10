from django.db import models
from django.db.models.signals import post_save
from django.contrib import admin
import uuid
from dateutil.relativedelta import *
from decimal import Decimal
from django.contrib.auth.models import User
from contas.models import ContasModel
from centroscustos.models import CentroCustosModel
from fornecedores.models import FornecedoresModel
#from clientes.models import ClientesModel
from django.utils.crypto import get_random_string
import os
from uuid import uuid4
# Create your models here.
class ClassificacaoDespesas(models.Model):
    titulo = models.CharField(max_length=300, null=True, blank=False, verbose_name='Título da classificaçãod de despesa')
    def __str__(self):
        return self.titulo
    class Meta:
        verbose_name='Classificação de despesa'
        verbose_name_plural='Classificações de despesa'

class PrevisoesModel(models.Model):
    def path_and_rename(instance, filename):
        upload_to = 'documentos_previsoes'
        ext = filename.split('.')[-1]
        # get filename
        if instance.pk:
            filename = '{}.{}'.format(instance.uuid, ext)
        else:
            # set filename as random string
            filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(upload_to, filename)

    categoria=(
        ("entrada", "Entrada"),
        ("saida", "Saída")
    )
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Usuário responsável')
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    codigo_barras=models.CharField(null=False, blank=True, default='N\A', max_length=300, verbose_name='Código de barras')
    ratear=models.BooleanField(blank=False)
    titulo = models.CharField(max_length=300, null=True, blank=False, verbose_name='Título da previsão de lançamento')
    fornecedor=models.ForeignKey(FornecedoresModel, blank=True, null=True, on_delete=models.CASCADE, related_name='previsoes_fornecedor', verbose_name='Fornecedor')
    cliente=models.ForeignKey('clientes.ClientesModel', blank=True, null=True, on_delete=models.CASCADE, related_name='previsoes_clientes', verbose_name='Fornecedor')
    centro_custos=models.ForeignKey(CentroCustosModel, on_delete=models.CASCADE, related_name='previsoes_centrocusto', verbose_name='Centro de custos')
    classificacao_despesa=models.ForeignKey(ClassificacaoDespesas, on_delete=models.CASCADE, related_name='previsoes_classificacaodespesa', verbose_name='Classificaçaõ da despesa')
    modalidade=models.CharField(choices=categoria, verbose_name="Entrada ou Saída", max_length=10, blank=False, null=False)
    valor=models.DecimalField(blank=True, null=True, max_digits=13, decimal_places=2, default=Decimal('0.00'))
    data_previsao=models.DateField(blank=False, null=False, verbose_name="Data de pagamento", help_text="Caso seja um pagamento em várias parcelas, indique a data da primeira parcela.")
    parcelas=models.SmallIntegerField(verbose_name="Número de parcelas", default=1, blank=False, null=False)
    intervado=models.SmallIntegerField(verbose_name="Intervalo entre as parcelas", default=30, blank=True, null=False)
    status = models.BooleanField(default=True, verbose_name='Previsão de lançamento ativa')
    efetivada = models.BooleanField(default=False, verbose_name='Previsão de lançamento efetivada')
    data_registro = models.DateTimeField(auto_now=True, verbose_name='Data de registro')
    data_pagamento = models.DateTimeField(null=True, blank=True, verbose_name='Data do pagamento')
    data_atualizacao = models.DateTimeField(null=True, blank=True, verbose_name='Última atualização')
    documento=models.FileField(upload_to=path_and_rename, blank=True, null=False)

    class Meta:
        verbose_name="Previsão de pagamento"
        verbose_name_plural="Previsões de pagamento"
        get_latest_by="pk"
    def __str__(self):
        return self.titulo
    def save(self, *args, **kwargs):
        valor_inicial=self.valor

        if self.modalidade=='saida' and valor_inicial>0:
            novo_valor=valor_inicial*-1
            self.valor = novo_valor
        else:
            self.valor=valor_inicial

        super(PrevisoesModel, self).save(*args, **kwargs)

class ParcelasModel(models.Model):
    uuid=models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    titulo=models.CharField(blank=True, null=False, max_length=200, verbose_name="Título da parcela")
    previsao=models.ForeignKey(PrevisoesModel, on_delete=models.CASCADE, related_name='parcelas_previsao')
    data_vencimento=models.DateField(blank=True, null=False, verbose_name="Data do vencimento da parcela")
    valor=models.DecimalField(blank=True, null=True, max_digits=13, decimal_places=2, default=Decimal('0.00'))
    status=models.BooleanField(default=True, verbose_name='Parcela ativa')
    efetivada=models.BooleanField(default=False, verbose_name='Pagamento efetivado')
    data_pagamento = models.DateField(blank=True, null=True, verbose_name="Data do pagamento da parcela")
    data_registro=models.DateTimeField(auto_now=True, verbose_name='Data de registro')
    class Meta:
        verbose_name='Parcela'
        verbose_name_plural='Parcelas'
    def __str__(self):
        return self.titulo

class PrevisoesHistoricoModel(models.Model):
    data_registro = models.DateTimeField(auto_now=True, verbose_name='Data de registro')
    icone = models.CharField(max_length=20, blank=True, null=True, default='query_builder')
    descricao = models.TextField(blank=False, null=False)
    class Meta:
        verbose_name = 'Histórico de previsão'
        verbose_name_plural = 'Históricos de previsões'
    def __str__(self):
        return str("{} em {}".format(self.descricao, self.data_registro))

class PrevisoesFornecedoresModel(models.Model):
    previsao=models.ForeignKey(PrevisoesModel, on_delete=models.CASCADE, related_name='previsoes_fornecedores')
    fornecedor=models.ForeignKey(FornecedoresModel, on_delete=models.CASCADE, related_name='fornecedores_previsao')
    data_registro=models.DateTimeField(auto_now=True, verbose_name='Data do registro')


def criar_parcela(sender, instance, created, **kwargs):

    if created:
        n = 0
        valor=0
        previsao = PrevisoesModel.objects.get(pk=instance.pk)

        if previsao.ratear is True:
            valor=previsao.valor/previsao.parcelas
        else:
            valor=previsao.valor
        for i in range(previsao.parcelas):
            if previsao.parcelas==1:
                n=1
            else:
                n += 1
            ParcelasModel.objects.create(
                titulo="{} | parcela {} de {}".format(previsao.titulo, n, previsao.parcelas),
                previsao=previsao,
                valor=valor,
                data_vencimento=previsao.data_previsao + relativedelta(days=+(previsao.intervado * i))
            ).save()

post_save.connect(criar_parcela, sender=PrevisoesModel, dispatch_uid="my_unique_identifier")
class PrevisoesModelAdmin(admin.ModelAdmin):
    list_display = ['centro_custos', 'fornecedor', 'classificacao_despesa', 'modalidade', 'valor']
admin.site.register(PrevisoesModel, PrevisoesModelAdmin)
class ParcelaPrevisaoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'valor', 'status', 'efetivada']

admin.site.register(ParcelasModel, ParcelaPrevisaoAdmin)
admin.site.register(PrevisoesHistoricoModel)
admin.site.register(ClassificacaoDespesas)

