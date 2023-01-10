import datetime

from django import forms
from contas.models import ContasModel
from centroscustos.models import CentroCustosModel, PlanosContaModel
from previsoes.models import ClassificacaoDespesas

opcoes_lancamentos_previsoes=[
                                 ('lacamentos', 'Apenas Lançamentos'),
                                 ('lacamentos_previsoes', 'Lançamentos e Previsões'),
                                 ('lacamentos', 'Apenas Previsões')
]
class FormPesquisaGeral(forms.Form):
    tipo=forms.CharField(label='Defina o tipo de registro a ser exibido no relatório',
                                           required=True,
                                           widget=forms.Select(choices=opcoes_lancamentos_previsoes, attrs={'class':'form-control show-tick col-lg-4  col-sm-4'}))

    data_inicio = forms.DateField(required=True, label="Data inicial da pesquisa",
                                  widget=forms.DateInput(attrs={"class": "datepicker form-control col-lg-4 col-sm-4"}))
    data_fim = forms.DateField(required=True, label="Data final da pesquisa",
                               widget=forms.DateInput(attrs={"class": "datepicker form-control col-lg-4 col-sm-4"}))


class formularoRelatorioLancamentos(forms.Form):
    descricao=forms.CharField(required=False, label='Descrição do lançamento',
                              widget=forms.TextInput(attrs={'class':'form-control col'}))
    centroCusto = forms.ModelMultipleChoiceField(label='Centros de custos', widget=forms.SelectMultiple(
        attrs={'class':'form-control show-tick'}), queryset=CentroCustosModel.objects.all().order_by('titulo'))
    classificacao = forms.ModelMultipleChoiceField(required= False, label='Classificação de despesa', widget=forms.SelectMultiple(
        attrs={'class': 'form-control show-tick'}), queryset=ClassificacaoDespesas.objects.all().order_by('titulo'))
    dataInicial = forms.DateField(required=True, initial=(datetime.datetime.now().today()-datetime.timedelta(365)), label="Data inicial",
                                     widget=forms.DateInput(attrs={"class": "datepicker form-control"}))
    dataFinal = forms.DateField(required=True, initial=datetime.datetime.now().today(), label="Data Final",
                                  widget=forms.DateInput(attrs={"class": "datepicker form-control"}))

    def clean_dataFinal(self):
        dataInicio=self.cleaned_data['dataInicial']
        dataFinal=self.cleaned_data['dataFinal']
        if dataFinal < dataInicio:
            self.add_error('dataFinal', 'A data final da busca é anterior a data inicial')
        else:
            return dataFinal
