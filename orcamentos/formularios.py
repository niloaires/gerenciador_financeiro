from django import forms
from django.forms import models, modelformset_factory, inlineformset_factory, formset_factory
from orcamentos.models import OrcamentosModel, ItensOrcamentosModel
from django.contrib.auth.models import User
from core.models import PerfilModel
from obras.models import ObrasModel
from previsoes.models import ClassificacaoDespesas
from fornecedores.models import FornecedoresModel, choice_tipo_fornecedor
from clientes.models import ClientesModel

class ForcecedoresForms(forms.ModelForm):
    choice_tipo_conta = (
        ("corrente", "Corrente"),
        ("pix", "Pix"),
        ("poupanca", "Poupança")
    )
    nome = forms.CharField(label="Nome do fornecedor", required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label="Endereço de e-mail", required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    tipo_fornecedor=forms.CharField(label="Pessoa física ou Jurídica", required=True, widget=forms.Select(choices=choice_tipo_fornecedor, attrs={'class':'form-control'}))
    cpf_cnpj = forms.CharField(label="CPF ou CNPJ", required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    endereco = forms.CharField(label="Endereço", required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    municipio = forms.CharField(label="Município", required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    estado = forms.CharField(label="Estado", required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    tipo_conta = forms.CharField(label="Tipo de conta bancária", required=False,
                                      widget=forms.Select(choices=choice_tipo_conta,
                                                          attrs={'class': 'form-control'}))
    banco = forms.CharField(label="Nome do banco", required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    agencia = forms.CharField(label="Agência", required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    conta = forms.CharField(label="Número da conta", required=False,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    pix = forms.CharField(label="Pix", required=False,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:

        model = FornecedoresModel
        fields =['nome', 'email', 'tipo_fornecedor', 'cpf_cnpj', 'endereco' ,'municipio', 'estado', 'tipo_conta', 'banco', 'agencia', 'conta', 'pix']

    def clean_nome(self):
        nome=self.cleaned_data.get('nome')
        if self.instance:
            return nome
        else:
            if FornecedoresModel.objects.filter(nome=nome).exists():
                raise forms.ValidationError("Já existe um fornecedor com esse nome!")
            else:
                return nome



class ClassificacaoDespesasForms(forms.ModelForm):
    titulo = forms.CharField(label="Título", required=True, help_text="Tenha certeza que não existe um registro similar",
                           widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = ClassificacaoDespesas
        fields =['titulo']

    def clean_titulo(self):
        titulo=self.cleaned_data.get('titulo')
        if ClassificacaoDespesas.objects.filter(titulo=titulo).exists():
            raise forms.ValidationError("A naturza de despesa que você está tentando adicionar já existe!")
        else:
            return titulo

class OrcamentoFormulario(forms.ModelForm):
    obra = forms.ModelChoiceField(label="Selecione uma obra", required=True,
                                  queryset=ObrasModel.objects.filter(status=True),
                                  widget=forms.Select(attrs={'class': 'form-control col-12 mb-5 mr-sm-2'}))
    class Meta:
        model = OrcamentosModel
        fields = ['obra']



class ItensOrcamentosFormularioModel(forms.ModelForm):
    fornecedor = forms.ModelChoiceField(label="Selecione um fornecedor", required=True,
                                  queryset=FornecedoresModel.objects.filter(status=True),
                                  widget=forms.Select(attrs={'class': 'form-control col', 'placeholder':'Fornecedor'}))
    item = forms.CharField(label="Item", required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control col', 'placeholder':'Item'}))
    classificacao_despesa = forms.ModelChoiceField(label="Classificação da despesa", required=True,
                                        queryset=ClassificacaoDespesas.objects.all().order_by('titulo'),
                                        widget=forms.Select(attrs={'class': 'form-control col',
                                                                   'placeholder': 'Fornecedor'}))
    unidade = forms.CharField(label="Unidade de medida", required=True, initial="UND",
                             widget=forms.TextInput(attrs={'class': 'form-control col', 'placeholder':'Unidade de medida'}))
    quantidade = forms.IntegerField(required=True, initial=1, min_value=0, label="Quantidade",
                                  widget=forms.NumberInput(attrs={"class": "form-control col", 'placeholder':'Quantidade'}))
    preco=forms.DecimalField(label="Valor do item", required=True, min_value=0.0, widget=forms.NumberInput(attrs={'class':'form-control col', 'placeholder':'Valor por item'}))

    class Meta:
        model = ItensOrcamentosModel
        fields=[ 'fornecedor', 'classificacao_despesa', 'item', 'unidade', 'quantidade', 'preco']
Itensformset=formset_factory(extra=1, form=ItensOrcamentosFormularioModel)
ItensModelFormset=modelformset_factory(ItensOrcamentosModel, extra=1, form=ItensOrcamentosFormularioModel)
class PrevisaoOrcamentoform(forms.Form):
    data_previsao=forms.CharField(widget=forms.DateInput(attrs={"class":"datepicker"}))

class DataPrevisaoAprovarOrcamentoForm(forms.Form):
    descricao = forms.CharField(label="Anotações no orçamento",initial='Sem ressalvas', help_text="Campo não obrigatório", required=False,
                                widget=forms.Textarea(attrs={'class': 'form-control no-resize', 'rows': 4}))
    data_previsao = forms.DateField(required=True, label="Data da previsão",
                                     widget=forms.DateInput(attrs={"class": "datepicker form-control"}))