from django import forms
#from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
from django.forms import ModelForm
from fornecedores.models import *
from centroscustos.models import CentroCustosModel
from contas.models import ContasModel
class CriarFornecedorModelForm(ModelForm):
    choice_tipo_conta = (
        ("corrente", "Corrente"),
        ("pix", "Pix"),
        ("poupanca", "Poupança")
    )
    choice_tipo_fornecedor = (
        ("fisica", "Pessoa Física"),
        ("juridica", "Jurídica"),
        ("outros", "Outros")
    )
    nome = forms.CharField(label="Nome ou razão social", required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control no-resize'}))
    email = forms.CharField(label="Endereço de e-mail", required=False,
                             widget=forms.EmailInput(attrs={'class': 'form-control no-resize'}))
    tipo_fornecedor = forms.CharField(label="Tipo de fornecedor", required=True,
                                 widget=forms.Select(choices=choice_tipo_fornecedor, attrs={"class": "form-control show-tick"}))
    nascimento = forms.DateField(required=False, label="Data de nascimento",
                                    widget=forms.DateInput(attrs={"class": "datepicker form-control"}))
    cpf_cnpj = forms.CharField(label="CPF / CNPJ do fornecedor", required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control no-resize'}))
    endereco = forms.CharField(label="Endereço do fornecedor", required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control no-resize'}))
    municipio = forms.CharField(label="Município", required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control no-resize'}))
    estado = forms.CharField(help_text="Use a sigla do Estado", label="Estado", required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control no-resize'}))
    tipo_conta = forms.CharField(label="Forma de pagamento do fornecedor", required=True,
                                      widget=forms.Select(choices=choice_tipo_conta,
                                                          attrs={"class": "form-control show-tick"}))
    banco = forms.CharField(label="Banco", required=True,
                                widget=forms.TextInput(attrs={'class': 'form-control no-resize'}))
    agencia = forms.CharField(label="Agência", required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control no-resize'}))
    conta = forms.CharField(label="Conta", required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control no-resize'}))
    pix = forms.CharField(label="PIX", required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control no-resize'}))


    class Meta:
        model = FornecedoresModel
        fields = ['nome', 'email', 'tipo_fornecedor', 'nascimento', 'cpf_cnpj', 'endereco', 'municipio', 'estado', 'tipo_conta', 'banco', 'agencia', 'conta', 'pix']

class CriarLancamentoFornecedorFormulario(forms.Form):
    categoria = (
        ("entrada", "Entrada"),
        ("saida", "Saída")
    )
    descricao=forms.CharField(max_length=300, label="Descrição", required=True)
    centro_custos = forms.ModelChoiceField(label="Centro de custos", queryset=CentroCustosModel.objects.filter(status=True).order_by('titulo'))
    conta = forms.ModelChoiceField(label="Conta bancária",queryset=ContasModel.objects.filter(status=True).order_by('titulo'))
    modalidade=forms.ChoiceField(label="Modalidade", choices=categoria)

    data_pagamento = forms.DateField(label="Data do pagamento", required=True,
                                     widget=forms.DateInput(attrs={'class':'datepicker'}))
    parcelas=forms.IntegerField(label="Número de parcelas", min_value=1)
    intervalo=forms.IntegerField(label="Intervalo entre as parcelas", min_value=1)
    valor = forms.DecimalField(label="Valor a registrar", min_value=0, widget=forms.NumberInput(attrs={'placeholder':'R$: 00,00', "step": 0.5}))
    valor_acrescimo = forms.DecimalField(required=False, min_value=0, initial=0, label="Valor de juros e multas", disabled=True,
                                             widget=forms.NumberInput(attrs={"step": 0.5}))
    valor_desconto = forms.DecimalField(required=False, min_value=0, initial=0, label="Valor de desconto", disabled=True,
                                            widget=forms.NumberInput(attrs={"step": 0.5}))

    comprovante= forms.FileField(label="Documento de comprovação", required=False, disabled=True,)
