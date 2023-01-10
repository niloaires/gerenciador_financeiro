from django import forms
from django.forms import models
from contratos.models import ContratosModel
from contas.models import ContasModel
from clientes.models import ClientesModel
from centroscustos.models import CentroCustosModel
from contratos.models import ContratosModel, AditivosModel
class ContratoFormulario(forms.ModelForm):
    titulo = forms.CharField(label="Título do contrato", required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control no-resize'}))
    cliente = forms.ModelChoiceField(label="Cliente vinculado ao contrato", required=True,
                                           queryset=ClientesModel.objects.filter(status=True),
                                           widget=forms.Select(attrs={'class': 'form-control show-tick'}))
    data_pactuacao = forms.DateField(required=True, label="Data de início do contrato",
                                     widget=forms.DateInput(attrs={"class": "datepicker form-control"}))
    data_encerramento = forms.DateField(required=True, label="Data de encerramento do contrato",
                                     widget=forms.DateInput(attrs={"class": "datepicker form-control"}))
    valor_pactuado = forms.DecimalField(required=False, initial=0.0, label="Valor pactuado em contrato", min_value=0.0,
                                        widget=forms.NumberInput(
                                            attrs={"class": "form-control show-tick", "step": 0.5}))
    class Meta:
        model = ContratosModel
        fields = ['titulo', 'cliente', 'data_pactuacao', 'data_encerramento', 'valor_pactuado']

class ContratoAdtivoFormulario(forms.Form):
    tipo_aditivo = (
        ("prazo", "Aditivo de prazo"),
        ("valor", "Aditivo de valor"),
        ("prazo_valor", "Aditovo de prazo e valor")
    )
    tipo = forms.CharField(label="Natureza do aditivo", required=True,
                                widget=forms.Select(choices=tipo_aditivo, attrs={"class": "form-control show-tick"}))
    novo_prazo = forms.DateField(required=False, label="Nova data de encerramento do contrato",
                                        widget=forms.DateInput(attrs={"class": "datepicker form-control"}))
    acrescimo_valor = forms.DecimalField(required=False, initial=0.0,  label="Valor adicional do contrato", min_value=0.0,
                                        widget=forms.NumberInput(
                                            attrs={"class": "form-control show-tick", "step": 0.5}))

    def clean(self):
        tipo=self.cleaned_data.get('tipo')
        if tipo == 'prazo':
            novo_prazo=self.cleaned_data.get('novo_prazo')
            if not novo_prazo:
                raise forms.ValidationError("Por ser um aditivo de prazo, é necessário informar uma data")
            else:
                return novo_prazo
        elif tipo=='valor':
            acrescimo_valor = self.cleaned_data.get('acrescimo_valor')
            if acrescimo_valor == 0.0:
                raise forms.ValidationError("Por ser um aditivo de valor, é necessário informar um valor")
            else:
                return acrescimo_valor
        elif tipo=='prazo_valor':
            acrescimo_valor = self.cleaned_data.get('acrescimo_valor')
            novo_prazo = self.cleaned_data.get('novo_prazo')
            if acrescimo_valor == 0.0 or not novo_prazo:
                raise forms.ValidationError("Por ser um aditivo de pazo e valor, as duas informações são indispensáveis")
            else:
                return acrescimo_valor



