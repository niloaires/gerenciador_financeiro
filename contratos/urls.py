from django.urls import path, include
from contratos.views import *
urlpatterns = [
    path("", ContratosView, name='contratos'),
    path("adicionar", ContratosCriarView, name='contratos_criar'),
    path("<uuid:uuid>", ContratoDetalhesView, name='contratos_detalhes'),
    path("aditivar/<uuid:uuid>", ContratoAditivarView, name='contrato_adivitar')
    #path("desabilitar/<uuid:uuid>", ClienteDesabilitarView, name='clientes_desabilitar'),
    #path("lancaremCliente/<uuid:uuid>", LancamentoObraCriarView, name='lancamento_cliente')


]
