from django.urls import path
from relatorios.views import *
from relatorios.novasViews import *

urlpatterns = [
    path("", busca, name='relatorios_busca'),
    path("pesquisar", view_relatorio, name='relatorios_pesquisar'),
    path("lancamentos", lancamentos_pdf, name='relatorio_lancamentos'),
    path("lancamento/<uuid:uuid>", lancamento_especifico, name='relatorio_especifico'),
    path("previsao/<uuid:uuid>", previsa_especifica, name='previsao_especifica'),
    path("fornecedores", fornecedores_pdf, name='relatorio_fornecedores'),
    path("contas_a_pagar", contas_a_apagar_pdf, name='relatorio_contas_a_pagar'),
    path("centros_custo", relatorio_centro_custos, name='relatorio_centros_custos'),
    path("centros_custo/<uuid:uuid>", relatorio_centro_custos_especifico, name='relatorio_centros_custos_especifico'),
    path("relatorio__previsao__centro_custos/<uuid:uuid>", relatorio_centro_custos_especifico, name='relatorio__previsao__centro_custos'),
    path("obra/<uuid:uuid>", relatorio_obra_especifica, name='relatorio_obra_especifica'),
    path("cliente/<uuid:uuid>", relatorio_cliente_especifico, name='relatorio_cliente_especifico'),
    path("os/<uuid:uuid>", os_especifica, name='relatorio_os_especifica'),
    path("pdf", gerarPDFRelatorio, name='relatorios_teste_pdf'),
    path("xls", gerarXSLRelatorio, name='relatorios_teste_xls'),
    path("novo-relatorio", novoRelatorio, name='novo_relatorio'),
    path("resultado-busca", resultadoBusca, name='resultado_busca')


]
