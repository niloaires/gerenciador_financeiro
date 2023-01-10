from django.urls import path, include
from core.views import *
urlpatterns = [
    path("", Inicio, name='painel'),

    path("clientes/", include('clientes.urls')),
    path("contratos/", include('contratos.urls')),
    path("contas_bancos/", include('contas.urls')),
    path("planos_contas/", include('centroscustos.urls_planos_contas')),
    path("centros_custos/", include('centroscustos.urls')),
    path("fornecedores/", include('fornecedores.urls')),
    path("lancamentos/", include('lancamentos.urls')),
    path("obras/", include('obras.urls')),
    path("orcamentos/", include('orcamentos.urls_adm')),
    path("orcamentos/", include('orcamentos.urls')),
    path("previsoes/", include('previsoes.urls')),
    path("relatorios/", include('relatorios.urls'))

]
