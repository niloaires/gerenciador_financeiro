from django import forms
from django.forms import models
from centroscustos.models import CentroCustosModel
from centroscustos.models import PlanosContaModel
class PlanoContasFormulario(forms.ModelForm):
    titulo = forms.CharField(label="Título do Plano de contas", required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control no-resize'}))
    descricao = forms.CharField(label="Descrição", required=True,
                                widget=forms.Textarea(attrs={'class': 'form-control no-resize', 'rows': 4}))
    class Meta:
        model = PlanosContaModel
        fields = ['titulo', 'descricao']

class CentroCustosFormulario(forms.ModelForm):
    titulo = forms.CharField(label="Título do Centro de custos", required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control no-resize'}))
    plano_contas = forms.ModelChoiceField(label="Plano de contas", required=True,
                                   queryset=PlanosContaModel.objects.filter(status=True),
                                   widget=forms.Select(attrs={'class': 'form-control show-tick'}))
    descricao = forms.CharField(label="Descrição", required=True,
                                widget=forms.Textarea(attrs={'class': 'form-control no-resize', 'rows': 4}))
    limite_gastos = forms.DecimalField(required=False, initial=0.0, label="Limite mensal de gastos", min_value=0.0,
                                        widget=forms.NumberInput(
                                            attrs={"class": "form-control show-tick", "step": 0.5}))
    class Meta:
        model = CentroCustosModel
        fields = ['titulo', 'plano_contas', 'descricao', 'limite_gastos']