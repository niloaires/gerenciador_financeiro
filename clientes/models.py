from django.db import models
from django.contrib import admin
import uuid
from lancamentos.models import LancamentosModel

# Create your models here.
class ClientesModel(models.Model):
    uuid=models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    nome=models.CharField(max_length=200, blank=False, null=False)
    cpf_cnpj=models.CharField(max_length=30, blank=True, null=True)
    endereco = models.CharField(max_length=200, verbose_name='Logradouro', blank=True, null=True)
    municipio = models.CharField(max_length=100, verbose_name='Município', blank=True, null=True)
    estado = models.CharField(max_length=50, verbose_name='Estado', blank=True, null=True)
    email = models.EmailField(verbose_name='Endereço de e-mail', blank=True, null=True)
    status = models.BooleanField(default=True, verbose_name='Cliente Ativo')
    data_registro = models.DateTimeField(auto_now=True, verbose_name='Data de registro')
    data_atualizacao = models.DateTimeField(null=True, blank=True, verbose_name='Última atualização')
    class Meta:
        verbose_name='Cliente'
        verbose_name_plural='Clientes'
    def __str__(self):
        return self.nome

admin.site.register(ClientesModel)
class ClientesHistoricoModel(models.Model):
    data_registro = models.DateTimeField(auto_now=True, verbose_name='Data de registro')
    icone = models.CharField(max_length=20, blank=True, null=True, default='query_builder')
    descricao = models.TextField(blank=False, null=False)
    class Meta:
        verbose_name = 'Histórico cliente'
        verbose_name_plural = 'Históricos cliente'
    def __str__(self):
        return str("{} em {}".format(self.descricao, self.data_registro))
class CLientesLancamentosModel(models.Model):
    lancamento=models.ForeignKey(LancamentosModel, on_delete=models.CASCADE, related_name='lancamentos_cliente')
    cliente=models.ForeignKey(ClientesModel, on_delete=models.CASCADE, related_name='cliente_lancamento')


    status=models.BooleanField(default=True)
    def __str__(self):
        return str("{} - operação de {} - cliente: {}".format(self.lancamento.descricao, self.lancamento.get_operacao_display(), self.cliente.nome))