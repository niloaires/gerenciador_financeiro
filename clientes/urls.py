from django.urls import path, include
from clientes.views import *
urlpatterns = [
    path("", ClientesView, name='clientes'),
    path("adicionar", ClientesCriarView, name='clientes_criar'),
    path("<uuid:uuid>", ClienteDetalhesView, name='clientes_detalhes'),
    path("editar/<uuid:uuid>", ClienteEditarView, name='clientes_editar'),
    path("desabilitar/<uuid:uuid>", ClienteDesabilitarView, name='clientes_desabilitar'),
    path("lancaremCliente/<uuid:uuid>", LancamentoObraCriarView, name='lancamento_cliente')


]
