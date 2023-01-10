from django.db import models
from django.db.models.signals import post_save
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from uuid import uuid4
from decimal import Decimal
from django.contrib.auth.models import User
from django.contrib import admin
from previsoes.models import PrevisoesModel, ClassificacaoDespesas
from fornecedores.models import FornecedoresModel
from contas.models import ContasModel
from centroscustos.models import CentroCustosModel
import os
from PIL import *

# Create your models here.
def path_and_rename(instance, filename):
    upload_to = 'comprovantes_lancamentos'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.uuid, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)
class LancamentosModel(models.Model):
    categoria = (
        ("entrada", "Entrada"),
        ("saida", "Saída")
    )

    usuario=models.ForeignKey(User, on_delete=models.PROTECT, related_name='lancamentos_user')
    uuid = models.UUIDField(unique=True, editable=False, default=uuid4)
    status=models.BooleanField(default=True, verbose_name="Lançamento Ativo")
    operacao = models.CharField(choices=categoria, verbose_name="Operação", max_length=10, blank=False,
                                null=False)
    centro_custos = models.ForeignKey(CentroCustosModel, on_delete=models.CASCADE, related_name='lancamentos_centrocusto',
                                      verbose_name='Centro de custos')
    descricao=models.TextField(blank=False, null=False, default="Sem informações", verbose_name="Descrição do lançamento")
    previsao=models.ForeignKey(PrevisoesModel, on_delete=models.PROTECT, related_name='lancamentos_previsao')
    classificacao_despesa = models.ForeignKey(ClassificacaoDespesas, on_delete=models.CASCADE,
                                              related_name='lancamentos_classificacaodespesa',
                                              verbose_name='Classificaçaõ da despesa')
    conta=models.ForeignKey(ContasModel, on_delete=models.PROTECT, related_name='lancamentos_conta')
    valor_inicial=models.DecimalField(max_digits=13, decimal_places=2, blank=False, null=True, verbose_name="Valor inicial")
    valor_desconto=models.DecimalField(max_digits=13, decimal_places=2, blank=True, null=True, default=0.00, verbose_name="Desconto")
    valor_acrescimo=models.DecimalField(max_digits=13, decimal_places=2,  blank=True, null=True, default=0.00, verbose_name="Juros e multas")
    valor_final=models.DecimalField(max_digits=13, decimal_places=2,  blank=True, null=True, default=0.00, verbose_name="Valor final")
    data_pagamento=models.DateField(blank=False, null=False, verbose_name="Data do pagamento")
    data_registro=models.DateTimeField(auto_now=True, verbose_name="Data do registro")
    comprovante=models.FileField(upload_to=path_and_rename, blank=True, null=True)
    #objects=lancamentosBusca.as_manager()
    def save(self, *args, **kwargs):
        self.classificacao_despesa=self.previsao.classificacao_despesa
        valor=(self.valor_inicial + self.valor_acrescimo - self.valor_desconto)
        if self.operacao=='saida' and valor>0:
            self.valor_final = valor*-1
        else:
            self.valor_final = valor
        super(LancamentosModel, self).save(*args, **kwargs)
    def modalidade(self):
        return self.previsao.modalidade
    def __str__(self):
        return self.descricao

    def __unicode__(self):
        return self.descricao

    def valor(self):
        return self.valor_final
    class Meta:
        verbose_name_plural="Lançamentos"
        verbose_name="Lançamento"
        ordering=['-data_pagamento', '-data_registro']
def registrar_na_conta_bancaria(sender, instance, created, **kwargs):

    if created:
        lancamento=LancamentosModel.objects.get(pk=instance.pk)
        conta=ContasModel.objects.get(lancamentos_conta=lancamento)
        conta.saldo+=lancamento.valor()
        conta.save()


post_save.connect(registrar_na_conta_bancaria, sender=LancamentosModel, dispatch_uid="my_unique_identifier")
class LancamentosHistoricoModel(models.Model):
    data_registro = models.DateTimeField(auto_now=True, verbose_name='Data de registro')
    icone = models.CharField(max_length=20, blank=True, null=True, default='query_builder')
    descricao = models.TextField(blank=False, null=False)
    class Meta:
        verbose_name = 'Histórico de lançamento'
        verbose_name_plural = 'Históricos de lançamentos'
    def __str__(self):

        return str("{} em {}".format(self.descricao, self.data_registro))

class PrevisoesLancamentosModel(models.Model):
    uuid = models.UUIDField(unique=True, editable=False, default=uuid4)
    status = models.BooleanField(default=True)
    previsao=models.ForeignKey(PrevisoesModel, on_delete=models.CASCADE, related_name='previsoes_lancamento')
    lancamento=models.ForeignKey(LancamentosModel, on_delete=models.CASCADE, related_name='lancamentos_previsoes')
    data_registro = models.DateTimeField(auto_now=True, verbose_name="Data do registro")
    def __str__(self):
        return str("{} pago em  {}".format(self.previsao.titulo, self.lancamento.data_registro))
    class Meta:
        verbose_name_plural = 'Previsões lançadas'
        verbose_name = 'Previsão lançada'

class FornecedoresLancamentosModel(models.Model):
    uuid = models.UUIDField(unique=True, editable=False, default=uuid4)
    status = models.BooleanField(default=True)
    fornecedor = models.ForeignKey(FornecedoresModel, on_delete=models.CASCADE, related_name='fornecedores_lancamento')
    lancamento = models.ForeignKey(LancamentosModel, on_delete=models.CASCADE, related_name='lancamentos_fornecedores')
    data_registro = models.DateTimeField(auto_now=True, verbose_name="Data do registro")
    def __str__(self):
        return str("lançado em  {} para o fornecedor {}".format(self.lancamento.data_registro, self.fornecedor.nome ))
    class Meta:
        verbose_name_plural = 'Lançamentos de fornecedores'
        verbose_name = 'Lançamento de fornecedor'

@admin.action(description='Atualizar valores finais')
def atualizar_saidas(modeladmin, request, queryset):
    for obj in queryset:
        if obj.operacao=='saida' and obj.valor_inicial>0:
            obj.valor_inicial=obj.valor_inicial*-1
            obj.save()
@admin.action(description='Atualizar classificação de despesa')
def atualizar_classificacao(modeladmin, request, queryset):
    for object in queryset:
        object.classificacao_despesa=object.previsao.classificacao_despesa
        object.save()
class LancamentosAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'status',  'valor_inicial', 'valor_acrescimo', 'valor_desconto', 'valor_final', 'data_pagamento')
    actions = [atualizar_saidas, atualizar_classificacao]
admin.site.register(LancamentosModel, LancamentosAdmin)
admin.site.register(LancamentosHistoricoModel)
admin.site.register(PrevisoesLancamentosModel)