from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from obras.models import ObrasModel, LancamentosObrasModel
from centroscustos.models import CentroCustosModel, PlanosContaModel
from obras.formularios import *
from contas.models import ContasModel
from previsoes.models import PrevisoesModel, ClassificacaoDespesas
from lancamentos.models import LancamentosModel
from contratos.models import PrevisaoContratoModel
from fornecedores.models import FornecedoresModel
from clientes.models import ClientesModel
import decimal
from core.decorador import precisa_ser_gestor
# Create your views here.
@login_required(login_url='login')
@precisa_ser_gestor
def ObrasView(request):
    contexto={
        'object_list': ObrasModel.objects.filter(status=True),
        'formulario':FormularioObras,
        'formulario_lancamento_obra':CriarLancamentoObraFormulario
    }
    return render(request, 'obras/lista.html', contexto)
@login_required(login_url='login')
@precisa_ser_gestor
def ObrasCriarView(request):
    if request.method == 'POST':
        formulario = FormularioObras(request.POST)
        if formulario.is_valid():
            #Criar um centro de custos específco para a nova obra
            centrocusto=CentroCustosModel.objects.create(
                usuario=request.user,
                plano_contas=PlanosContaModel.objects.get(pk=2),
                titulo=str("Centro de custos da obra {}".format(formulario.cleaned_data['nome'])),
                descricao=str("Centro de custos criado automaticamente para agrupar registros financeiros referentes a obra {}".format(formulario.cleaned_data['nome']))

            ).save()
            centrocusto=CentroCustosModel.objects.last()
            obra = formulario.save(commit=False)
            obra.usuario=request.user
            obra.centrocusto=centrocusto
            obra.save()
            obra = ObrasModel.objects.last()
            messages.add_message(request, messages.SUCCESS, "A obra {} foi adicionada com sucesso".format(obra.nome))
            return redirect('obras')
        else:
            contexto={
                'formulario':formulario,
                'object_list': ObrasModel.objects.filter(status=True)

            }
            return render(request, 'obras/lista.html', contexto)
@login_required(login_url='login')
@precisa_ser_gestor
def ObrasDetalhesView(request, uuid):
    object = get_object_or_404(ObrasModel, uuid=uuid)
    contexto = {
        'object':object,
        'previoes_list':PrevisoesModel.objects.filter(status=True, efetivada=False, centro_custos=object.centrocusto).order_by('data_previsao'),
        'lancamentos_list':LancamentosModel.objects.filter(status=True, centro_custos=object.centrocusto).order_by('-data_pagamento'),
        'formulario_lancamento_obra':CriarLancamentoObraFormulario,
        'formulario_pesquisa_previsoes':FormularioRelatorios,
        'formulario_encerramento_obra':FormularioEncerramentoObra
    }
    return render(request, 'obras/detalhes_novo.html', contexto)


@login_required(login_url='login')
@precisa_ser_gestor
def ObrasEncerrarView(request, uuid):
    object=get_object_or_404(ObrasModel, uuid=uuid)
    object.fim_obra=request.POST.get('data_encerramento')
    object.obra_finalizada=True
    object.save()
    centro_custo=object.centrocusto
    messages.add_message(request, messages.SUCCESS, "A obra {obra} foi encerrada com sucesso!".format(obra=object))
    if request.POST.get("encerrar_centro_custo") == 'True':
        centro_custo.bloqueado=True
        centro_custo.save()
        messages.add_message(request, messages.SUCCESS, "O centro de custos {centrocustos} "
                                                        "foi bloqueado para novos lançamentos!".
                             format(centrocustos=centro_custo.titulo))

        return redirect('obras')
    return redirect('obras')



@login_required(login_url='login')
@precisa_ser_gestor
def ObrasReabilitarView(request, uuid):
    object=get_object_or_404(ObrasModel, uuid=uuid)
    object.fim_obra=request.POST.get('data_encerramento')
    object.obra_finalizada=False
    object.save()
    messages.add_message(request, messages.SUCCESS, "A obra {obra} foi reativada com sucesso!".format(obra=object))
    centro_custo=object.centrocusto
    centro_custo.bloqueado=False
    centro_custo.save()
    messages.add_message(request, messages.SUCCESS, "O centro de custos {cc} foi reativado com sucesso!".format(cc=centro_custo.titulo))
    return redirect('obras')





@login_required(login_url='login')
@precisa_ser_gestor
def ObrasDesabilitarView(request, uuid):
    object=get_object_or_404(ObrasModel, uuid=uuid)
    object.status=False
    object.save()
    messages.add_message(request, messages.SUCCESS, "A obra {} foi desabilitada com sucesso!".format(object))
    return redirect('obras')
@login_required(login_url='login')
@precisa_ser_gestor
def ObrasLancamentosView(request):
    contexto={
        'object_list': LancamentosObrasModel.objects.filter(lancamento__status=True).order_by('obra__nome', 'lancamento__data_pagamento')

    }
    return render(request, 'obras/lancamentos_obras.html', contexto)
@login_required(login_url='login')
@precisa_ser_gestor
def LancamentoObraCriarView(request, uuid):
    if request.method=='POST':
        obra = ObrasModel.objects.get(uuid=uuid)
        centro_custos = CentroCustosModel.objects.get(pk=obra.centrocusto.pk)

        conta = ContasModel.objects.get(pk=request.POST.get('conta'))
        #Verifica se a obra está finalizada
        if obra.obra_finalizada is True:
            messages.add_message(request, messages.INFO,
                                 'A obra {obra} está finalizada, por esse motivo os lançamentos '
                                 'não podem mais ser realizados.'.format(obra=obra.nome))
            return redirect('obras_detalhes', obra.uuid)
        #Se não estiver finalizada, o processo de lançamento continua!
        request_classificacao_despesa = request.POST.get('classificacao_despesa')
        if request_classificacao_despesa is None:
            classificacao_despesa=ClassificacaoDespesas.objects.get(pk=15)
        else:
            classificacao_despesa=ClassificacaoDespesas.objects.get(pk=request.POST.get('classificacao_despesa'))
        request_fornecedor = request.POST.get('fornecedor')
        if request_fornecedor is None:
            fornecedor=FornecedoresModel.objects.get(pk=51)
        else:
            fornecedor = FornecedoresModel.objects.get(pk=request.POST.get('fornecedor'))
        parcelas=request.POST.get('parcelas')
        tipo_registro=request.POST.get('criar_lancamento')

        if tipo_registro!='lancar':
            # Criar Previsão:
            PrevisoesModel.objects.create(
                usuario=request.user,
                codigo_barras=request.POST.get('codigo_barras'),
                ratear=False,
                titulo=request.POST.get('titulo'),
                fornecedor=fornecedor,
                #cliente=cliente,
                centro_custos=centro_custos,
                classificacao_despesa=classificacao_despesa,
                modalidade=request.POST.get('categoria'),
                valor=decimal.Decimal(request.POST.get('valor_inicial')),
                data_previsao=request.POST.get('data_pagamento'),
                parcelas=parcelas,
                efetivada=False,
                documento=request.FILES.get('documento'),

            ).save()

            # Estanciar a Previsão
            previsao = PrevisoesModel.objects.latest('pk')

            # Associar previsão ao contrato
            PrevisaoContratoModel.objects.create(
                previsao=previsao,
                contrato=obra.contrato

            ).save()
            messages.add_message(request, messages.SUCCESS, 'A previsão {} foi registrada com sucesso'.format(previsao.titulo, obra.contrato))
            messages.add_message(request, messages.SUCCESS, 'A previsão {} foi associado ao contrato'.format(previsao.titulo, obra.contrato))
            return redirect('obras_detalhes', obra.uuid)

    # Caso seja um LANÇAMENTO criará a previsão e o lançamento
    if request.POST.get('ratear')=='ratear':
        ratear=True
    else:
        ratear=False
    PrevisoesModel.objects.create(
        usuario=request.user,

        codigo_barras=request.POST.get('codigo_barras'),
        ratear=ratear,
        titulo=request.POST.get('titulo'),
        fornecedor=fornecedor,
        centro_custos=centro_custos,
        classificacao_despesa=classificacao_despesa,
        modalidade=request.POST.get('categoria'),
        valor=decimal.Decimal(request.POST.get('valor_inicial')),
        data_previsao=request.POST.get('data_pagamento'),
        parcelas=1,
        efetivada=True,
        data_pagamento=request.POST.get('data_pagamento'),
        documento=request.FILES.get('comprovante'),

    ).save()
    # Estanciar a Previsão
    previsao = PrevisoesModel.objects.latest('pk')
    # Associar previsão ao contrato
    PrevisaoContratoModel.objects.create(
        previsao=previsao,
        contrato=obra.contrato

    ).save()
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
    # Criar LancamentoObra
    LancamentosObrasModel.objects.create(
        obra=obra,
        lancamento=lancamento
    ).save()
    messages.add_message(request, messages.SUCCESS,
                         'A previsão {} foi registrada com sucesso'.format(previsao.titulo, obra.contrato))
    messages.add_message(request, messages.SUCCESS,
                         'A previsão {} foi associado ao contrato'.format(previsao.titulo, obra.contrato))
    messages.add_message(request, messages.SUCCESS, 'O lançamento foi realizado com sucesso!')

    return redirect('obras_detalhes', obra.uuid)

