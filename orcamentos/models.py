from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from uuid import uuid4
from obras.models import ObrasModel
from previsoes.models import PrevisoesModel, ClassificacaoDespesas
from fornecedores.models import FornecedoresModel
from decimal import Decimal
# Create your models here.


class OrcamentosModel(models.Model):
    uuid=models.UUIDField(editable=False, unique=True, default=uuid4)
    usuario=models.ForeignKey(User, on_delete=models.CASCADE, related_name='orcamentos_usuario', verbose_name="Usuário")
    obra=models.ForeignKey(ObrasModel, on_delete=models.CASCADE, related_name='orcamentos_obra')
    descricao=models.CharField(max_length=200, blank=False, null=False, default="Sem informações", verbose_name="Descrição")
    numero_ordem=models.PositiveSmallIntegerField(verbose_name="Número da OS", blank=True, null=True)
    aprovado=models.BooleanField(default=False, verbose_name="Orçamento aprovado")
    status=models.BooleanField(default=True, verbose_name="Status do orçamento")
    data_registro=models.DateTimeField(auto_now=True, verbose_name="Data do registro")
    data_autorizacao=models.DateTimeField(blank=True, null=True, verbose_name="Data do registro")

    def save(self, *args, **kwargs):
        atual=0
        qs=OrcamentosModel.objects.filter(obra=self.obra)
        atual+=qs.count()
        if atual==0:
            self.numero_ordem=1
        else:
            atual+=1
            self.numero_ordem=atual

        super(OrcamentosModel, self).save(*args, **kwargs)
    def __str__(self):
        return str("Orçamento {} da obra {}".format(self.numero_ordem, self.obra.nome))


    def valor_orcado(self):
        total=0
        for i in self.itens_orcamento.all():
            sub=i.preco*i.quantidade
            total+=sub
        return total



    class Meta:
        verbose_name_plural="Orçamentos"
        verbose_name="Orçamento"
class OrcamentosHistoricoModel(models.Model):
    data_registro = models.DateTimeField(auto_now=True, verbose_name='Data de registro')
    icone = models.CharField(max_length=20, blank=True, null=True, default='query_builder')
    descricao = models.TextField(blank=False, null=False)
    class Meta:
        verbose_name = 'Histórico de orçamento'
        verbose_name_plural = 'Históricos de orçamentos'
    def __str__(self):
        return str("{} em {}".format(self.descricao, self.data_registro))

class ItensOrcamentosModel(models.Model):
    orcamento=models.ForeignKey(OrcamentosModel, on_delete=models.PROTECT, related_name='itens_orcamento')
    fornecedor = models.ForeignKey(FornecedoresModel, on_delete=models.CASCADE, related_name='item_orcamento_fornecedor')
    classificacao_despesa = models.ForeignKey(ClassificacaoDespesas, on_delete=models.CASCADE,
                                              related_name='item_classificacaodespesa',
                                              verbose_name='Classificaçaõ da despesa')
    item = models.CharField(max_length=100, verbose_name="Item", blank=False, null=False)
    unidade = models.CharField(max_length=20, verbose_name="Unidade")
    quantidade=models.SmallIntegerField(default=1, verbose_name="Quantidade")
    preco=models.DecimalField(decimal_places=2, max_digits=13, default=Decimal(0.00), blank=False, null=False, verbose_name="Preço do item")
    def __str__(self):
        return self.item
    def subtotal(self):
        return self.quantidade*self.preco
    class Meta:
        verbose_name_plural="Itens no orçamento"
        verbose_name="Item no orçamento"
class ItemOrcamentoAdim(admin.ModelAdmin):
    list_display = ["item", "quantidade", "orcamento", "preco", "subtotal"]
    list_filter = ("orcamento", )
admin.site.register(ItensOrcamentosModel, ItemOrcamentoAdim)
admin.site.register(OrcamentosModel)

