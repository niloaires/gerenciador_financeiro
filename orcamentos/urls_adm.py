from django.urls import path
from orcamentos.views import *

urlpatterns = [
    path("", OrcamentosViewAdm, name='orcamentos_adm'),
    path("<uuid:uuid>", OrcamentosDetalhesViewAdm, name='orcamentos_detalhes_adm'),
    path("aprovar/<uuid:uuid>", OrcamentosAprovarViewAdm, name='orcamentos_aprovar_adm')


]
