from django.db import models
from django.contrib import admin
import uuid
from django.contrib.auth.models import User
from decimal import Decimal


# Create your models here.
class ContasModel(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Usuário responsável')
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    titulo = models.CharField(max_length=30, null=True, blank=False, verbose_name='Título da conta')
    agencia = models.CharField(max_length=8, null=False, default='N|A',blank=True, verbose_name='Agência')
    conta = models.CharField(max_length=32, null=False, default='N|A', blank=True, verbose_name='Número da conta')
    digito = models.CharField(max_length=8, null=False, default='N|A', blank=True, verbose_name='Dígito da conta')
    status = models.BooleanField(default=True, verbose_name='Banco ativo')
    saldo = models.DecimalField(max_digits=13, decimal_places=2, default=Decimal('0.00'), blank=True, verbose_name='Saldo disponível')
    class Meta:
        verbose_name = 'Conta'
        verbose_name_plural = 'Contas'

    def __str__(self):
        return self.titulo
    def saldo_em_real(self):
        return str("R$ {}".format(self.saldo))
    def saldo_lancamentos(self):
        saldo=0
        qs=self.lancamentos_conta.filter(status=True)
        for i in qs:
            saldo+=i.valor_final
        return saldo
class ContasAdmin(admin.ModelAdmin):
    list_display = ['saldo_lancamentos', 'titulo', 'uuid']
admin.site.register(ContasModel, ContasAdmin)

class ContasHistoricoModel(models.Model):
    data_registro = models.DateTimeField(auto_now=True, verbose_name='Data de registro')
    icone = models.CharField(max_length=20, blank=True, null=True, default='query_builder')
    descricao = models.TextField(blank=False, null=False)
    class Meta:
        verbose_name = 'Histórico cliente'
        verbose_name_plural = 'Históricos cliente'
    def __str__(self):
        return str("{} em {}".format(self.descricao, self.data_registro))