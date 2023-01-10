from django.contrib import admin
from django.urls import path
from fornecedores.views import *
urlpatterns = [
    path("", FornecedoresView, name='fornecedores'),
    path("adicionar", FornecedorCriarView, name='fornecedor_criar'),
    path("<uuid:uuid>", FornecedorDetalhesView, name='fornecedor_detalhes'),
    path("lancar/<uuid:uuid>", CriarLancamentoFornecedor, name='fornecedor_criar_lancamento')

]