from django.urls import path
from previsoes.views import *
from previsoes.relatorios import *
urlpatterns = [
    path("", PrevisoesView, name='previsoes'),
    path("adicionar", PrevisoesCriarView, name='previsoes_criar'),
    path("<uuid:uuid>", PrevisoesDetalhesView, name='previsoes_detalhes'),
    path("editar/<uuid:uuid>", PrevisoesEditarView, name='previsoes_editar'),
    path("desabilitar/<uuid:uuid>", PrevisoesDesabilitarView, name='previsoes_desabilitar'),
    path("previsao/lancar/<uuid:uuid>", LancarPrevisoesView, name='previsoes_criar_lancamento_unificado'),
    path("parcela/<uuid:uuid>", ParcelasDetalhesView, name='previsoes_parcela_detalhes'),
    path("parcela/lancar/<uuid:uuid>", LancarParcelaView, name='previsoes_parcela_lancar'),
    path("parcela/desabilitar/<uuid:uuid>", ParcelaDesabilitarView, name='previsoes_parcela_desabilitar'),
    path("relatorio", some_view, name="previsoes_relatorio")


]
