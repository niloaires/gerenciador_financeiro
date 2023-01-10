from django.db import models
from django.contrib import admin
import uuid
from decimal import Decimal
from django.contrib.auth.models import User
from clientes.models import ClientesModel, CLientesLancamentosModel
from lancamentos.models import LancamentosModel
from previsoes.models import PrevisoesModel
from django.db.models.signals import post_save
# Create your models here.
class ContratosModel(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Usuário responsável')
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    titulo = models.CharField(verbose_name='Título da obra', max_length=200, blank=False, null=False)
    cliente = models.ForeignKey(ClientesModel, on_delete=models.CASCADE, related_name='contratos_cliente')
    data_pactuacao = models.DateField(blank=False, null=False, verbose_name='Data de pactuação')
    data_encerramento = models.DateField(blank=False, null=False, verbose_name='Data de encerramento')
    valor_pactuado = models.DecimalField(max_digits=13, decimal_places=2, blank=False, null=False, default=Decimal('0.00'), verbose_name='Valor pactuado')
    status = models.BooleanField(default=True)
    class Meta:
        verbose_name='Contrato'
        verbose_name_plural='Contratos'
    def __str__(self):
        return str("{} - {}".format(self.titulo, self.cliente.nome))
    def valor_total(self):
        total=self.valor_pactuado
        adtivos=AditivosModel.objects.filter(status=True, contrato_id=self.pk)
        if adtivos:
            for i in adtivos:
                total+=i.acrescimo_valor
                return total
        return total

class AditivosModel(models.Model):
    tipo_aditivo = (
        ("prazo", "Aditivo de prazo"),
        ("valor", "Aditivo de valor"),
        ("prazo_valor", "Aditovo de prazo e valor")
    )
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Usuário responsável')
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    tipo=models.CharField(max_length=15, choices=tipo_aditivo, blank=False, null=False, verbose_name='Tipo de aditivo')
    contrato=models.ForeignKey(ContratosModel, on_delete=models.CASCADE, related_name='aditivos_contrato')
    novo_prazo=models.DateField(blank=True, null=True, verbose_name='Novo prazo')
    acrescimo_valor=models.DecimalField(max_digits=13, decimal_places=2, blank=True, null=True, verbose_name='Valor acrescido')
    status = models.BooleanField(default=True)

    def __str__(self):
        return str("{} - {}".format(self.get_tipo_display(), self.contrato.titulo))
    class Meta:
        verbose_name='Aditivo'
        verbose_name_plural='Aditivos'

class ContratosClientesLancamentos(models.Model):
    cliente=models.ForeignKey(ClientesModel, on_delete=models.CASCADE, related_name='cliente_contrato_lancamento')
    contrato=models.ForeignKey(ContratosModel, on_delete=models.CASCADE, related_name='contrato_ciente_lancamento')
    lancamento=models.ForeignKey(LancamentosModel, on_delete=models.CASCADE, related_name='lancamento_contrato_cliente')
    status=models.BooleanField(default=True)
class PrevisaoContratoModel(models.Model):
    status=models.BooleanField(default=True)
    previsao=models.ForeignKey(PrevisoesModel, on_delete=models.CASCADE)
    contrato=models.ForeignKey(ContratosModel, on_delete=models.CASCADE)

admin.site.register(ContratosModel)
admin.site.register(AditivosModel)