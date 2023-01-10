from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
#from lancamentos.models import LancamentosModel
from django.contrib import admin
import uuid
# Create your models here.
#from previsoes.models import PrevisoesModel
choice_tipo_fornecedor = (
        ("fisica", "Pessoa Física"),
        ("juridica", "Jurídica"),
        ("outros", "Outros")
    )
class FornecedoresModel(models.Model):
    choice_tipo_conta = (
        ("corrente", "Corrente"),
        ("pix", "Pix"),
        ("poupanca", "Poupança")
    )

    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=100, verbose_name='Razão Social / Nome / Nome fantasia', blank=False, null=False)
    tipo_fornecedor=models.CharField(choices=choice_tipo_fornecedor, blank=False, null=False, max_length=10, verbose_name="Tipo de Fornecedor")
    avatar=models.ImageField(upload_to='fornecedores_avatar', blank=True, null=True, verbose_name='Foto do perfil')
    nascimento = models.DateField(blank=True, verbose_name='Data de nascimento', null=True)
    cpf_cnpj = models.CharField(max_length=30, verbose_name='CPF/CNPJ', blank=True, null=False, default='Não informado')
    endereco = models.CharField(max_length=200, verbose_name='Logradouro', blank=True, null=True)
    municipio = models.CharField(max_length=100, verbose_name='Município', blank=True, null=True)
    estado = models.CharField(max_length=100, verbose_name='Estado', blank=True, null=True)
    email = models.EmailField(verbose_name='Endereço de e-mail', blank=True, null=True)
    status = models.BooleanField(default=True, verbose_name='Fornecedor ativo')
    data_registro = models.DateTimeField(auto_now=True, verbose_name='Data de registro')
    data_atualizacao = models.DateTimeField(null=True, blank=True, verbose_name='Última atualização')
    tipo_conta = models.CharField(max_length=100, choices=choice_tipo_conta, null=False, default='N|A', blank=False, verbose_name='Tipo de conta')
    banco = models.CharField(max_length=100, null=False, default='N|A', blank=True, verbose_name='Banco')
    agencia = models.CharField(max_length=8, null=False, default='N|A', blank=True, verbose_name='Agência')
    conta = models.CharField(max_length=32, null=False, default='N|A', blank=True, verbose_name='Número da conta')
    pix = models.CharField(max_length=200, null=False, default='N|A', blank=True, verbose_name='Dados do Pix')
    def previsao_acumulada(self):
        total=0
        qs=self.previsoes_fornecedor.filter(status=True)
        for i in qs:
            total+=i.valor
        return total
    #lancamento=GenericRelation(LancamentosModel)
    class Meta:
        verbose_name='Fornecedor'
        verbose_name_plural='Fornecedores'
    def __str__(self):
        return self.nome

admin.site.register(FornecedoresModel)