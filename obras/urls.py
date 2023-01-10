from django.urls import path
from obras.views import *

urlpatterns = [
    path("", ObrasView, name='obras'),
    path("lancamentos", ObrasLancamentosView, name='obras_lancamentos'),
    path("<uuid:uuid>", ObrasDetalhesView, name='obras_detalhes'),
    path("finalizar/<uuid:uuid>", ObrasEncerrarView, name='obras_encerrar'),
    path("reabilitar/<uuid:uuid>", ObrasReabilitarView, name='obras_reabilitar'),
    path("adicionar", ObrasCriarView, name='obra_criar'),
    path("lancaremObra/<uuid:uuid>", LancamentoObraCriarView, name='lancamento_obra')


]
