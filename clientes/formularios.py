from django import forms
from django.forms import models
from clientes.models import ClientesModel
from contas.models import ContasModel
from centroscustos.models import CentroCustosModel
from contratos.models import ContratosModel
class ClienteFormulario(forms.ModelForm):
    nome = forms.CharField(label="Nome do cliente", required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control no-resize'}))
    cpf_cnpj = forms.CharField(label="CPF ou CNPJ", required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control no-resize'}))
    endereco = forms.CharField(label="Endereço", required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control no-resize'}))
    municipio = forms.CharField(label="Município", required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control no-resize'}))
    estado = forms.CharField(label="Estado", required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control no-resize'}))
    email = forms.CharField(label="Endereço de e-mail", required=False,
                           widget=forms.EmailInput(attrs={'class': 'form-control no-resize'}))
    class Meta:
        model = ClientesModel
        fields = ['nome', 'cpf_cnpj', 'endereco', 'municipio', 'estado', 'email']

class CriarLancamentoClienteFormulario(forms.Form):
    categoria = (
        ("entrada", "Entrada"),
        ("saida", "Saída")
    )


    titulo=forms.CharField(label="Título do lançamento", required=True, widget=forms.TextInput(attrs={'class':'form-control no-resize'}))
    descricao=forms.CharField(label="Descrição", required=True, widget=forms.Textarea(attrs={'class':'form-control no-resize', 'rows':4}))
    categoria=forms.CharField(label="Entrada ou saída", required=True, widget=forms.Select(choices=categoria, attrs={"class":"form-control show-tick"}))
    centro_custos=forms.ModelChoiceField(label="Centro de custos", required=True, queryset=CentroCustosModel.objects.filter(status=True), widget=forms.Select(attrs={'class':'form-control show-tick'}))
    contrato=forms.ModelChoiceField(label="Contrato", required=True, queryset=ContratosModel.objects.filter(status=True), widget=forms.Select(attrs={'class':'form-control show-tick'}))
    conta=forms.ModelChoiceField(label="Conta bancária", required=True, queryset=ContasModel.objects.filter(status=True), widget=forms.Select(attrs={'class':'form-control show-tick'}))
    valor_inicial=forms.DecimalField(label="Valor inicial", required=True, min_value=0.0, widget=forms.NumberInput(attrs={"class":"form-control show-tick"}))
    valor_acrescimo=forms.DecimalField(required=False, initial=0.0, label="Valor de juros e multas", min_value=0.0, widget=forms.NumberInput(attrs={"class":"form-control show-tick", "step":0.5}))
    valor_desconto=forms.DecimalField(required=False, initial=0.0, label="Valor de desconto", min_value=0.0, widget=forms.NumberInput(attrs={"class":"form-control show-tick", "step":0.5}))
    data_pagamento=forms.DateField(required=True, label="Data do pagamento", widget=forms.DateInput(attrs={"class":"datepicker form-control"}))
    comprovante=forms.FileField(required=True, label="Comprovante do pagamento", widget=forms.FileInput(attrs={"class":"form-control"}))