from django.urls import path
from orcamentos.views import *

urlpatterns = [
    path("add_fornecedor", FornecedorCriar, name='orcamentos_add_fornecedor'),
    path("fornecedores", FornecedorLista, name='orcamentos_fornecedor'),
    path("editar_fornecedor/<uuid:uuid>", FornecedorEditar, name='orcamentos_editar_fornecedor'),
    path("editar_item_orcamento/<int:pk>", ItemOrcamentoEditar, name='orcamentos_editar_item'),
    path("deletar_item_orcamento/<int:pk>", ItemOrcamentoDeletar, name='orcamentos_deletar_item'),
    path("add_naturezaDespesa", NaturezaDespesasCriar, name='orcamentos_add_naturezadespesa'),


    path("", OrcamentosView, name='orcamentos'),
    path("criar", OrcamentosCriarView, name='orcamentos_criar'),
    path("<uuid:uuid>", OrcamentosDetalhesView, name='orcamentos_detalhes'),
    path("confirmar_exclusao/<uuid:uuid>", OrcamentoConfirmarDeletar, name='orcamento_confirmar_exclusao'),
    path("exclusao/<uuid:uuid>", OrcamentoDeletar, name='orcamento_exclusao'),
    #path("aprovar/<uuid:uuid>", OrcamentoAprovarView, name='orcamento_aprovar')
]
