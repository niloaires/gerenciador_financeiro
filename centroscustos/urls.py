from django.urls import path
from centroscustos.views import *

urlpatterns = [
    #path("", PlanoContasView, name='planocontas'),
    #path("adicionar", PlanoContasCriarView, name='planocontas_criar'),
    #path("<uuid:uuid>", PlanoContasDetalhesView, name='planocontas_detalhes'),
    #path("editar/<uuid:uuid>", PlanoContasEditarView, name='planocontas_editar'),
    #path("desabilitar/<uuid:uuid>", PlanoContasDesabilitarView, name='planocontas_desabilitar'),

    path("", CentrosCustosView, name='centrocustos'),
    path("adicionar", CentroCustosCriarView, name='centrocustos_criar'),
    path("<uuid:uuid>", CentroCustosDetalhesView, name='centrocustos_detalhes'),
    path("editar/<uuid:uuid>", CentroCustosEditarView, name='centrocustos_editar'),
    path("desabilitar/<uuid:uuid>", CentroCustosDesabilitarView, name='centrocustos_desabilitar'),
]
