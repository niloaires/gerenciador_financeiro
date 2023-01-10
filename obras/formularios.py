from django import forms

from contratos.models import ContratosModel
from previsoes.models import ClassificacaoDespesas
from django.forms import models
from lancamentos.models import LancamentosModel
from obras.models import ObrasModel
from clientes.models import ClientesModel

from contas.models import ContasModel
from fornecedores.models import FornecedoresModel
class FormularioObras(forms.ModelForm):

    nome = forms.CharField(label="Título da obra", required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control no-resize'}))
    cliente = forms.ModelChoiceField(label="Cliente", required=True,
                                           queryset=ClientesModel.objects.filter(status=True),
                                           widget=forms.Select(attrs={'class': 'form-control show-tick'}))
    contrato = forms.ModelChoiceField(label="Contrato", required=True,
                                     queryset=ContratosModel.objects.filter(status=True),
                                     widget=forms.Select(attrs={'class': 'form-control show-tick'}))
    observacoes=forms.CharField(label="Anotações sobre a obra", required=False, widget=forms.TextInput(attrs={"row":"3", 'class': 'form-control no-resize'}))

    endereco = forms.CharField(label="Endereço da obra", required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control no-resize'}))
    inicio_obra = forms.DateField(required=True, label="Data de início a obra",
                                    widget=forms.DateInput(attrs={"class": "datepicker form-control"}))
    previsao = forms.DateField(required=False, label="Data de previsão do encerramento da obra",
                                  widget=forms.DateInput(attrs={"class": "datepicker form-control"}))


    class Meta:
        model=ObrasModel
        fields=['nome', 'cliente', 'contrato', 'endereco', 'inicio_obra','previsao', 'observacoes']
class CriarLancamentoObraFormulario(forms.Form):
    categoria = (
        ("", "Selecione uma modalidade"),
        ("saida", "Saída"),
        ("entrada", "Entrada")

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
    classificacao_despesa = forms.ModelChoiceField(label="Classificação da despesa", required=True,
                                                   queryset=ClassificacaoDespesas.objects.exclude(pk=15).order_by('titulo'),
                                                   widget=forms.Select(attrs={'class': 'form-control show-tick'}))
    fornecedor = forms.ModelChoiceField(label="Fornecedor", required=False,
                                        queryset=FornecedoresModel.objects.filter(status=True),
                                        widget=forms.Select(attrs={'class': 'form-control show-tick'}))
    cliente = forms.ModelChoiceField(label="Cliente", required=False,
                                        queryset=ClientesModel.objects.filter(status=True),
                                        widget=forms.Select(attrs={'class': 'form-control show-tick'}))
    conta=forms.ModelChoiceField(label="Conta bancária", required=True, queryset=ContasModel.objects.filter(status=True), widget=forms.Select(attrs={'class':'form-control show-tick'}))
    codigo_barras = forms.CharField(label="Código de barras", required=False, initial='S/N',
                                    widget=forms.TextInput(attrs={'class': 'form-control no-resize'}))
    parcelas = forms.IntegerField(required=False, initial=1, min_value=0, label="Número de parcelas",
                                  widget=forms.NumberInput(attrs={"class": "form-control"}))
    intervado = forms.IntegerField(required=False, initial=30, min_value=0, label="Intervalo entre parcelas",
                                   widget=forms.NumberInput(attrs={"class": "form-control"}))

    valor_inicial=forms.DecimalField(label="Valor inicial", required=True, min_value=0.0, widget=forms.TextInput(attrs={"class":"form-control show-tick numero"}))
    valor_acrescimo=forms.DecimalField(required=False, disabled=True, initial=0.0, label="Valor de juros e multas", min_value=0.0, widget=forms.TextInput(attrs={"class":"form-control show-tick numero", "step":0.5}))
    valor_desconto=forms.DecimalField(required=False, disabled=True, initial=0.0, label="Valor de desconto", min_value=0.0, widget=forms.TextInput(attrs={"class":"form-control show-tick numero", "step":0.5}))
    data_pagamento=forms.DateField(required=True, label="Data do pagamento", widget=forms.DateInput(attrs={"class":"datepicker form-control"}))
    documento = forms.FileField(required=False, label="Documento",
                                widget=forms.FileInput(attrs={"class": "form-control"}))
    comprovante=forms.FileField(required=False, disabled=True, label="Comprovante do pagamento", widget=forms.FileInput(attrs={"class":"form-control"}))

class FormularioRelatorios(forms.Form):
    opcao_formato_relatorio=(
        ('excel', 'Excel'),
        ('pdf', 'Pdf')
    )
    data_inicio = forms.DateField(required=True, label="Data inicial da pesquisa",
                               widget=forms.DateInput(attrs={"class": "datepicker form-control"}))
    data_fim = forms.DateField(required=True, label="Data final da pesquisa",
                             widget=forms.DateInput(attrs={"class": "datepicker form-control"}))
    formato_relatorio=forms.ChoiceField(choices=opcao_formato_relatorio,required=True, label='Formato do relatório',
                                      widget=forms.Select(attrs={'class':'form-control'}))

class FormularioEncerramentoObra(forms.Form):
    data_encerramento = forms.DateField(required=True, label="Data de encerramento da obra",
                               widget=forms.DateInput(attrs={"class": "datepicker form-control"}))
    encerrar_centrocustos = forms.BooleanField(required= False,
                                               label="Encerrar o centro de custos",
                                               initial=False,
                                               widget=forms.CheckboxInput(attrs={"class":"form-control"}))