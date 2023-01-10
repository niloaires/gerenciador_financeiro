from django.urls import path
from lancamentos.views import *

urlpatterns = [
    path("", LancamentosView, name='lancamentos'),
    path("adicionar", LancamentoCriarView, name='lancamento_adicionar'),
    path("<uuid:uuid>", LancamentoDetalhesView, name='lancamentos_detalhes'),
    path("editar/<uuid:uuid>", LancamentosEditarView, name='lancamento_editar'),
    path("desabilitar/<uuid:uuid>", LancamentoDesabilitarView, name='lancamento_desabilitar'),


    path("ajax", AutoCompleteLancamentosPesquisa, name="Ajax-Previsao")

]
