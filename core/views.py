from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Sum
from itertools import chain
from operator import attrgetter
from contas.models import ContasHistoricoModel, ContasModel
from lancamentos.models import LancamentosHistoricoModel, LancamentosModel
from previsoes.models import PrevisoesHistoricoModel, PrevisoesModel
from orcamentos.models import OrcamentosModel
from core.models import PerfilModel
import datetime
hoje = datetime.datetime.now()
# Create your views here.
@login_required(login_url='login')
def Inicio(request):
    h_bancos = ContasHistoricoModel.objects.all()
    h_lancamentos = LancamentosHistoricoModel.objects.all()
    h_previsoes = PrevisoesHistoricoModel.objects.all()
    previsoes=PrevisoesModel.objects.filter(status=True)
    orcamentos=OrcamentosModel.objects.filter(status=True)
    previsoes_mes=previsoes.filter(data_previsao__month=hoje.month).aggregate(acumulado=Sum('valor'))
    proximos_vencimentos=previsoes.filter(efetivada=False).order_by('data_previsao')[:5]
    os_aprovar=orcamentos.filter(aprovado=False)
    lancamentos=LancamentosModel.objects.filter(status=True).order_by('data_pagamento')
    contas=ContasModel.objects.filter(status=True).order_by('titulo')
    entradas=lancamentos.filter(lancamentos_previsoes__previsao__modalidade='entrada').aggregate(acumulado=Sum('valor_final'))
    saidas=lancamentos.filter(lancamentos_previsoes__previsao__modalidade='saida').aggregate(acumulado=Sum('valor_final'))
    contexto = {
        'ultimos_lancamentos':lancamentos[:7],
        'balanco_mes':lancamentos.filter(data_pagamento__month=hoje.month).aggregate(total=Sum('valor_final')),
        'contas_bancarias':contas[:7],
        'historico': sorted(chain(h_bancos, h_lancamentos, h_previsoes), key=attrgetter('data_registro'), reverse=True),
        'acumulado_previsoes': previsoes_mes['acumulado'],
        'saldo_entradas': lancamentos.filter(data_pagamento__month=hoje.month, operacao='entrada').aggregate(total=Sum('valor_final')),
        'saldo_saidas': lancamentos.filter(data_pagamento__month=hoje.month, operacao='saida').aggregate(total=Sum('valor_final')),
        'saldo_contas':contas.aggregate(total=Sum('saldo')),
        'proximos_vencimentos':previsoes.order_by('data_previsao')[:7],
        'os_para_aprovar':os_aprovar
    }
    return render(request, 'core/painel2.html', contexto)
def Logout(request):
    logout(request)
    return redirect('login')
def Login(request):
    if request.method == 'POST':
        usuario = request.POST.get('username')
        senha = request.POST.get('password')
        dados_usuario=authenticate(username=usuario, password=senha)
        if dados_usuario is None:
            messages.error(request, "A sua senha parece estar incorreta.")
            return render(request, 'core/login.html')
        else:
            login(request, dados_usuario)
            perfil=PerfilModel.objects.get(usuario=request.user.pk)
            if perfil.gestor:
                return redirect('painel')
            else:
                return redirect('orcamentos')
    else:
        contexto = {}
        return render(request, 'core/login.html', contexto)