from django import forms
from django.forms import models
from previsoes.models import PrevisoesModel, ClassificacaoDespesas
from contas.models import ContasModel
from centroscustos.models import CentroCustosModel
from fornecedores.models import FornecedoresModel
categoria = (
        ("entrada", "Entrada"),
        ("saida", "Saída")
    )
class PrevisoesFormulario(forms.ModelForm):
    titulo = forms.CharField(label="Título da previsão", required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control no-resize'}))
    codigo_barras = forms.CharField(label="Código de barras", required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control no-resize'}))

    fornecedor = forms.ModelChoiceField(label="Fornecedor", required=True,
                                           queryset=FornecedoresModel.objects.filter(status=True),
                                           widget=forms.Select(attrs={'class': 'form-control show-tick'}))
    centro_custos = forms.ModelChoiceField(label="Centro de custos", required=True,
                                           queryset=CentroCustosModel.objects.filter(status=True),
                                           widget=forms.Select(attrs={'class': 'form-control show-tick'}))
    classificacao_despesa = forms.ModelChoiceField(label="Classificação da despesa", required=True,
                                           queryset=ClassificacaoDespesas.objects.all().order_by('titulo'),
                                           widget=forms.Select(attrs={'class': 'form-control show-tick'}))
    modalidade = forms.CharField(label="Entrada ou saída", required=True,
                                widget=forms.Select(choices=categoria, attrs={"class": "form-control show-tick"}))
    valor = forms.DecimalField(label="Valor previsto", required=True, min_value=0.0,
                                       widget=forms.NumberInput(attrs={"class": "form-control show-tick"}))

    data_previsao = forms.DateField(required=True, label="Data do pagamento",
                                     widget=forms.DateInput(attrs={"class": "datepicker form-control"}))
    parcelas=forms.IntegerField(required=True, initial=1, min_value=0, label="Número de parcelas", widget=forms.NumberInput(attrs={"class": "form-control"}))
    intervado=forms.IntegerField(required=True, initial=30, min_value=0, label="Intervalo entre parcelas", widget=forms.NumberInput(attrs={"class": "form-control"}))
    documento = forms.FileField(required=False, label="Documento",
                                  widget=forms.FileInput(attrs={"class": "form-control"}))
    class Meta:
        model = PrevisoesModel
        fields = ['titulo', 'centro_custos', 'fornecedor', 'classificacao_despesa', 'modalidade', 'valor', 'data_previsao', 'parcelas', 'intervado', 'codigo_barras', 'documento']

class LancarPrevisoesFormulario(forms.Form):
    valor_inicial= forms.DecimalField(label="Valor inicial desta previsão", widget=forms.NumberInput(attrs={"class": "form-control show-tick"}))
    data_pagamento = forms.DateField(label="Data do pagamento", required=True,
                                     widget=forms.DateInput(attrs={'class': 'datepicker form-control show-tick'}))
    valor_acrescimo = forms.DecimalField(label="Acréscimo", required=True, widget=forms.NumberInput(attrs={'class': 'form-control show-tick', "value":0.00}))
    valor_desconto = forms.DecimalField(label="Desconto", required=True, widget=forms.NumberInput(attrs={'class': 'form-control show-tick', "value":0.00}))
    conta = forms.ModelChoiceField(label="Conta bancária", required=True, queryset=ContasModel.objects.filter(status=True),
                                   widget=forms.Select(attrs={'class': 'form-control show-tick'}))
    comprovante = forms.FileField(required=False, label='Documento de comprovação do pagamento',
                                  widget=forms.FileInput())
