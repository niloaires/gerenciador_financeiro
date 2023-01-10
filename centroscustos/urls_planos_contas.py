from django.urls import path
from centroscustos.views import *

urlpatterns = [
    path("", PlanoContasView, name='plano_contas'),
    path("adicionar", PlanoContasCriarView, name='planocontas_criar'),
    path("<uuid:uuid>", PlanoContasDetalhesView, name='planocontas_detalhes'),
    path("editar/<uuid:uuid>", PlanoContasEditarView, name='planocontas_editar'),
    path("desabilitar/<uuid:uuid>", PlanoContasDesabilitarView, name='planocontas_desabilitar'),


]
