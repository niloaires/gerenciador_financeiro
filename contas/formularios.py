from django import forms
from django.core.exceptions import ValidationError
from django.forms import models
import datetime
from contas.models import ContasModel

class ContaFormulario(forms.ModelForm):
    titulo = forms.CharField(label="Título da conta bancária", required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control no-resize'}))
    agencia = forms.CharField(label="Número da agência", required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control no-resize'}))
    conta = forms.CharField(label="Número da conta", required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control no-resize'}))
    digito = forms.CharField(label="Dígito", required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control no-resize'}))
    saldo = forms.DecimalField(label="Saldo da conta bancária", required=True, initial=0.0,
                                       widget=forms.NumberInput(attrs={"class": "form-control show-tick"}))
    class Meta:
        model = ContasModel
        fields = ['titulo', 'agencia', 'conta', 'digito', 'saldo']

class MovimentacoesFormulario(forms.Form):
    inicial=forms.DateField(label='Data inicial',required=True, widget=forms.DateInput(attrs={'class':'datepicker form-control '}))
    final=forms.DateField(label='Data final', required=True, widget=forms.DateInput(attrs={'class':'datepicker form-control'}))
    def clean(self):
        super(MovimentacoesFormulario, self).clean()
        inicial=self.cleaned_data.get('inicial')
        final=self.cleaned_data.get('final')
        #Lógica de validaçao
        if datetime.datetime(inicial)>datetime.datetime(final):
            raise ValidationError("A data inicial é maior que a data final")

