from django.urls import path
from contas.views import *

urlpatterns = [
    path("", ContasView, name='contas'),
    path("adicionar", ContasCriarView, name='contas_criar'),
    path("<uuid:uuid>", ContasDetalhesView, name='contas_detalhes'),
    path("editar/<uuid:uuid>", ContasEditarView, name='contas_editar'),
    path("desabilitar/<uuid:uuid>", ContasDesabilitarView, name='contas_desabilitar'),
]
