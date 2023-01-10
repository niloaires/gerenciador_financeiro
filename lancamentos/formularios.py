from django import forms
from django.forms import models
from previsoes.models import PrevisoesModel, ClassificacaoDespesas
from django.contrib.contenttypes.models import ContentType
from lancamentos.models import LancamentosModel
from obras.models import ObrasModel
from fornecedores.models import FornecedoresModel
from clientes.models import ClientesModel
from centroscustos.models import CentroCustosModel, PlanosContaModel
from contas.models import ContasModel
class CriarLancamentoFormulario(forms.Form):
    categoria = (
        ("entrada", "Entrada"),
        ("saida", "Saída")
    )
    tipo = (
        ("cliente", "Clientes"),
        ("fornecedor", "Fornecedores"),
        ("obras", "Obras"),
        ("outros", "Outros")
    )
    titulo=forms.CharField(label="Título do lançamento", required=True, widget=forms.TextInput(attrs={'class':'form-control no-resize'}))
    descricao=forms.CharField(label="Descrição", required=True, widget=forms.Textarea(attrs={'class':'form-control no-resize', 'rows':4}))
    categoria=forms.CharField(label="Entrada ou saída", required=True, widget=forms.Select(choices=categoria, attrs={"class":"form-control show-tick"}))
    classificacao_despesa=forms.ModelChoiceField(label="Classificação da despesa", required=True, queryset=ClassificacaoDespesas.objects.all(), widget=forms.Select(attrs={'class':'form-control show-tick'}))
    centro_custos=forms.ModelChoiceField(label="Centro de custos", required=True, queryset=CentroCustosModel.objects.filter(status=True, bloqueado=False), widget=forms.Select(attrs={'class':'form-control show-tick'}))
    conta=forms.ModelChoiceField(label="Conta bancária", required=True, queryset=ContasModel.objects.filter(status=True), widget=forms.Select(attrs={'class':'form-control show-tick'}))
    valor_inicial=forms.DecimalField(label="Valor inicial", required=True, min_value=0.0, widget=forms.NumberInput(attrs={"class":"form-control show-tick"}))
    valor_acrescimo=forms.DecimalField(required=False, initial=0.0, label="Valor de juros e multas", min_value=0.0, widget=forms.NumberInput(attrs={"class":"form-control show-tick", "step":0.5}))
    valor_desconto=forms.DecimalField(required=False, initial=0.0, label="Valor de desconto", min_value=0.0, widget=forms.NumberInput(attrs={"class":"form-control show-tick", "step":0.5}))
    data_pagamento=forms.DateField(required=True, label="Data do pagamento", widget=forms.DateInput(attrs={"class":"datepicker form-control"}))
    comprovante=forms.FileField(required=False, label="Comprovante do pagamento", widget=forms.FileInput(attrs={"class":"form-control"}))

class EditarLancamentoFormulario(forms.ModelForm):
    categoria = (
        ("entrada", "Entrada"),
        ("saida", "Saída")
    )
    tipo = (
        ("cliente", "Clientes"),
        ("fornecedor", "Fornecedores"),
        ("obras", "Obras"),
        ("outros", "Outros")
    )
    #titulo=forms.CharField(label="Título do lançamento", required=True, widget=forms.TextInput(attrs={'class':'form-control no-resize'}))
    descricao=forms.CharField(label="Descrição", required=True, widget=forms.Textarea(attrs={'class':'form-control no-resize', 'rows':4}))
    categoria=forms.CharField(label="Entrada ou saída", required=True, widget=forms.Select(choices=categoria, attrs={"class":"form-control show-tick"}))
    classificacao_despesa=forms.ModelChoiceField(label="Classificação da despesa", required=True, queryset=ClassificacaoDespesas.objects.all(), widget=forms.Select(attrs={'class':'form-control show-tick'}))
    centro_custos=forms.ModelChoiceField(label="Centro de custos", required=True, queryset=CentroCustosModel.objects.filter(status=True, bloqueado=False), widget=forms.Select(attrs={'class':'form-control show-tick'}))
    conta=forms.ModelChoiceField(label="Conta bancária", required=True, queryset=ContasModel.objects.filter(status=True), widget=forms.Select(attrs={'class':'form-control show-tick'}))
    valor_inicial=forms.DecimalField(label="Valor inicial", required=True, min_value=0.0, widget=forms.NumberInput(attrs={"class":"form-control show-tick"}))
    valor_acrescimo=forms.DecimalField(required=False, initial=0.0, label="Valor de juros e multas", min_value=0.0, widget=forms.NumberInput(attrs={"class":"form-control show-tick", "step":0.5}))
    valor_desconto=forms.DecimalField(required=False, initial=0.0, label="Valor de desconto", min_value=0.0, widget=forms.NumberInput(attrs={"class":"form-control show-tick", "step":0.5}))
    data_pagamento=forms.DateField(required=True, label="Data do pagamento", widget=forms.DateInput(attrs={"class":"datepicker form-control"}))
    comprovante=forms.FileField(required=False, label="Comprovante do pagamento", widget=forms.FileInput(attrs={"class":"form-control"}))

    class Meta:
        model = LancamentosModel
        fields = ['descricao', 'categoria', 'classificacao_despesa', 'centro_custos', 'conta', 'valor_inicial',
                  'valor_acrescimo', 'valor_desconto', 'data_pagamento', 'comprovante']
class BuscarLancamentoFormulario(forms.Form):
    categoria = (

        ("entrada", "Entrada"),
        ("saida", "Saída")
    )
    operacao=forms.CharField(label="Entrada ou saída", required=False, widget=forms.SelectMultiple(choices=categoria))
    #planocontas = forms.ModelChoiceField(label="Plano de contas", required=False, queryset=PlanosContaModel.objects.filter(status=True))
    centrocustos = forms.ModelChoiceField(label="Centro de custos", required=False,
                                          queryset=CentroCustosModel.objects.filter(status=True))
    conta = forms.ModelChoiceField(label="Banco ou conta", required=False, queryset=ContasModel.objects.filter(status=True))
    #referencia = forms.ModelChoiceField(label="Referência", required=False, queryset=LancamentosModel.objects.all().values_list('content_type'))
    intervalo = forms.CharField(label="Intervalo entre pagamentos", required=False, widget=forms.TextInput(attrs={'autocomplete':'off'}))