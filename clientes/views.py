from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from clientes.models import ClientesModel, ClientesHistoricoModel, CLientesLancamentosModel
from previsoes.models import PrevisoesModel
from clientes.formularios import *
from lancamentos.models import LancamentosModel
from contratos.models import ContratosModel, ContratosClientesLancamentos
from django.contrib.auth.decorators import login_required
import decimal
from core.decorador import precisa_ser_gestor
# Create your views here.

@login_required(login_url='login')
@precisa_ser_gestor
def ClientesView(request):
    contexto ={
        'object_list':ClientesModel.objects.filter(status=True).order_by('nome'),
        'formulario': ClienteFormulario()
    }
    return render(request, 'clientes/lista.html', contexto)
@login_required(login_url='login')
@precisa_ser_gestor
def ClientesCriarView(request):
    formulario = ClienteFormulario(request.POST)
    if request.method == 'POST':
        if formulario.is_valid():
            cliente = formulario.save(commit=False)
            cliente.usuario = request.user
            cliente.save()
            historico = ClientesHistoricoModel.objects.create(
                descricao=str("A conta {} foi criada".format(cliente.nome))
            ).save()

            messages.add_message(request, messages.SUCCESS,
                                 'O cliente {} foi adicionado com sucesso'.format(cliente.nome))
            return redirect('clientes')
@login_required(login_url='login')
@precisa_ser_gestor
def ClienteDetalhesView(request, uuid):
    object = get_object_or_404(ClientesModel, uuid=uuid)
    if request.method=='GET':
        contexto = {
            'object':object,
            'object_list':CLientesLancamentosModel.objects.filter(status=True, cliente=object),
            'formulario_lancamento_cliente':CriarLancamentoClienteFormulario()
        }
        return render(request, 'clientes/detalhes_novo.html', contexto)
@login_required(login_url='login')
@precisa_ser_gestor
def ClienteEditarView(request, uuid):
    object = get_object_or_404(ClientesModel, uuid=uuid)
    if request.method=='POST':
        formulario = ClienteFormulario(request.POST, instance=object)
        if formulario.is_valid():
            formulario.save(commit=False)

            messages.add_message(request, messages.SUCCESS, "O cliente {} foi atualizado com sucesso!".format(object.nome))
            return redirect('clientes_detalhes', object.uuid)

    else:
        contexto = {
            'object':object,
            'formulario_editar': ClienteFormulario(instance=object)
        }
        return render(request, 'clientes/editar_cliente.html', contexto)
@login_required(login_url='login')
@precisa_ser_gestor
def ClienteDesabilitarView(request, uuid):
    object = get_object_or_404(ClientesModel, uuid=uuid)
    object.status=False
    object.save()
    messages.add_message(request, messages.SUCCESS, "O cliente {} foi desabilitado com sucesso!".format(object.nome))
    return redirect('clientes')
@login_required(login_url='login')
@precisa_ser_gestor
def LancamentoObraCriarView(request, uuid):
    if request.method=='POST':
        cliente = ClientesModel.objects.get(uuid=uuid)
        cc = CentroCustosModel.objects.get(pk=request.POST.get('centro_custos'))
        conta = ContasModel.objects.get(pk=request.POST.get('conta'))
        contrato = ContratosModel.objects.get(pk=request.POST.get('contrato'))

        # Criar Previsão:
        PrevisoesModel.objects.create(
            usuario=request.user,
            titulo=request.POST.get('titulo'),
            referencia='N/A',
            centro_custos=cc,
            modalidade=request.POST.get('categoria'),
            valor=decimal.Decimal(request.POST.get('valor_inicial')),
            data_previsao=request.POST.get('data_pagamento'),
            parcelas=1,
            efetivada=True,
            data_pagamento=request.POST.get('data_pagamento'),

        ).save()
        # Estanciar a Previsão
        previsao = PrevisoesModel.objects.latest('pk')
        # Criar Lançamento
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
            comprovante=request.FILES.get('comprovante')

        ).save()
        lancamento = LancamentosModel.objects.latest('pk')
        # Criar LancamentoCliente
        CLientesLancamentosModel.objects.create(
            cliente=cliente,
            lancamento=lancamento
        ).save()
        #Registrar Lançamento no contrato
        ContratosClientesLancamentos.objects.create(
           cliente=cliente,
           contrato=contrato,
           lancamento=lancamento
        ).save()

        messages.add_message(request, messages.SUCCESS, 'O lançamento foi realizado com sucesso!')
        return redirect('lancamentos_detalhes', lancamento.uuid)