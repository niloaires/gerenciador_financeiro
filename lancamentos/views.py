from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib import messages
from django.http import JsonResponse
from lancamentos.models import *
from previsoes.models import *
from lancamentos.formularios import CriarLancamentoFormulario, BuscarLancamentoFormulario, EditarLancamentoFormulario
from django.db.models import Sum, Q
from lancamentos.serializadores import *
from rest_framework.response import Response
from clientes.models import ClientesModel
from fornecedores.models import FornecedoresModel
from obras.models import ObrasModel
from django.core import serializers
from itertools import chain
import json
from datetime import datetime
import decimal
from django.contrib.auth.decorators import login_required
from core.decorador import precisa_ser_gestor
# Create your views here.
@login_required(login_url='login')
@precisa_ser_gestor
def LancamentosView(request):


    busca=BuscarLancamentoFormulario(request.GET)
    filtro=(Q(status=True))
    if request.GET.get('operacao'):
        filtro.add(Q(operacao__in=request.GET.getlist('operacao')), Q.AND)
    if request.GET.get('centrocustos'):
        filtro.add(Q(centro_custos=request.GET.get('centrocustos')), Q.AND)
    if request.GET.get('planocontas'):
        filtro.add(Q(plano_contas=request.GET.get('planocontas')), Q.AND)
    if request.GET.get('conta'):
        filtro.add(Q(conta=request.GET.get('conta')), Q.AND)
    if request.GET.get('intervalo'):
        data_final=str(request.GET.get('intervalo'))[-10:23]
        data_inicial=str(request.GET.get('intervalo'))[0:10]
        inicial=datetime.strptime(data_inicial, '%d/%m/%Y')
        final=datetime.strptime(data_final, '%d/%m/%Y')
        filtro.add(Q(data_pagamento__range=[inicial, final]), Q.AND)
    qs=LancamentosModel.objects.filter(filtro).order_by('-data_registro', '-data_pagamento')
    acumulado = qs.aggregate(total=Sum('valor_final'))
    contexto = {
        'object_list': qs,
        'formulario_busca':BuscarLancamentoFormulario,
        'formulario':CriarLancamentoFormulario,
        'historico': LancamentosHistoricoModel.objects.all(),
        'total':acumulado['total'],


    }
    return render(request, 'lancamentos/lista.html', contexto)
@login_required(login_url='login')
@precisa_ser_gestor
def LancamentoCriarView(request):
    if request.method=='POST':
        formulario = CriarLancamentoFormulario(request.POST)
        cc=CentroCustosModel.objects.get(pk=request.POST.get('centro_custos'))
        conta=ContasModel.objects.get(pk=request.POST.get('conta'))
        classificacaodespesa=ClassificacaoDespesas.objects.get(pk=request.POST.get('classificacao_despesa'))
        #Caso o Centro de custos esteja bloqueado
        if cc.bloqueado is True:
            messages.add_message(request, messages.INFO,
                                 "A sua tentativa de lançamento falhou, o Centro de custos {} está indisponível para novos registros!".format(cc.titulo))
            return redirect('lancamentos')
        #Se o centro de custos estiver liberado...
        # Criar Previsão:
        PrevisoesModel.objects.create(
            usuario=request.user,
            titulo=request.POST.get('titulo'),
            centro_custos=cc,
            modalidade=request.POST.get('categoria'),
            valor=decimal.Decimal(request.POST.get('valor_inicial')),
            data_previsao=request.POST.get('data_pagamento'),
            parcelas=1,
            efetivada=True,
            data_pagamento=request.POST.get('data_pagamento'),
            classificacao_despesa=classificacaodespesa,
            ratear=False,


        ).save()
        #Estanciar a Previsão
        previsao=PrevisoesModel.objects.latest('pk')
        #Criar Lançamento
        LancamentosModel.objects.create(
            usuario=request.user,
            operacao=request.POST.get('categoria'),
            centro_custos=previsao.centro_custos,
            descricao=request.POST.get('descricao'),
            previsao=previsao,
            conta=conta,
            valor_inicial=decimal.Decimal(request.POST.get('valor_inicial')),
            valor_desconto=decimal.Decimal(request.POST.get('valor_desconto')),
            valor_acrescimo=decimal.Decimal(request.POST.get('valor_acrescimo')),
            data_pagamento=request.POST.get('data_pagamento'),
            comprovante=request.POST.get('comprovante')

            ).save()
        lancamento=LancamentosModel.objects.latest('pk')
        messages.add_message(request, messages.SUCCESS, "O lançamento: {} foi registrado com sucesso!".format(lancamento))
        return redirect('lancamentos_detalhes', lancamento.uuid)


@login_required(login_url='login')
@precisa_ser_gestor
def LancamentosEditarView(request, uuid):
    object = get_object_or_404(LancamentosModel, uuid=uuid)
    if request.method=='GET':
        formulario = EditarLancamentoFormulario(instance=object)
    elif request.method=='POST':
        formulario=EditarLancamentoFormulario(request.POST, instance=object)
        if formulario.is_valid():
            formulario.save()
            messages.add_message(request, messages.SUCCESS,
                                 "O lançamento {lancamento} foi editado com sucesso com sucesso.".
                                 format(lancamento=object.descricao))
            return redirect('lancamentos_detalhes', object.uuid)
        else: #Se o formulário apresentar erros
            for erro in formulario.errors:
                messages.add_message(request, messages.ERROR,
                                     "{}".format(erro))
            return redirect(request.META['HTTP_REFERER'])
@login_required(login_url='login')
@precisa_ser_gestor
def LancamentoDetalhesView(request, uuid):
    object = get_object_or_404(LancamentosModel, uuid=uuid)
    contexto={
        'object':object,
        'formulario_editar':EditarLancamentoFormulario(instance=object, initial={'categoria':object.categoria}),
        'object_list': LancamentosModel.objects.filter(status=True, centro_custos=object.centro_custos),
        'parcelas_relacionadas':ParcelasModel.objects.filter(status=True, efetivada=False, previsao=object.previsao)
    }
    return render(request, 'lancamentos/detalhes_novo.html', contexto)
@login_required(login_url='login')
@precisa_ser_gestor
def LancamentoDesabilitarView(request, uuid):
    object = get_object_or_404(LancamentosModel, uuid=uuid)
    object.status=False
    object.save()
    historico = LancamentosHistoricoModel.objects.create(
       icone='delete',
      descricao=str("O lançamento {} foi desabilitado com sucesso".format(object))
     ).save()
    # Registra uma mensagem de sucesso
    messages.add_message(request, messages.SUCCESS, "O lançamento foi desabilitado com sucesso.")
    return redirect('lancamentos')
@login_required(login_url='login')
@precisa_ser_gestor
def AjaxPrevisao(request):
    if 'pk' in request.GET:
        previsao = PrevisoesModel.objects.get(pk=request.GET('pk')).values('valor')
        return JsonResponse(previsao, safe=False)
@login_required(login_url='login')
@precisa_ser_gestor
def AutoCompleteLancamentosPesquisa(request):
    categoria=request.GET.get('categoria')
    if categoria=='obras':
        obras = ObrasModel.objects.filter(status=True).values('pk', 'nome')
        data = []
        for i in obras:
            data.append(i)
    if categoria=='fornecedores':
        fornecedores = FornecedoresModel.objects.filter(status=True).values('pk', 'nome')
        data = []
        for i in fornecedores:
            data.append(i)
    if categoria=='clientes':
        clientes = ClientesModel.objects.filter(status=True).values('pk', 'nome')
        data = []
        for i in clientes:
            data.append(i)
    return JsonResponse(data, safe=False)

    """
    clientes = ClientesModel.objects.filter(status=True).values('pk', 'nome')
    fornecedores = FornecedoresModel.objects.filter(status=True).values('pk', 'nome')
    obras = ObrasModel.objects.filter(status=True).values('pk', 'nome')
    data=[]
    for i in obras:
        data.append(i)
    for i in fornecedores:
        data.append(i)
    for i in clientes:
        data.append(i)
    return JsonResponse(data, safe=False)
    """



