from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from previsoes.models import PrevisoesModel, ParcelasModel, PrevisoesHistoricoModel
from previsoes.formularios import PrevisoesFormulario, LancarPrevisoesFormulario
from lancamentos.models import LancamentosHistoricoModel, LancamentosModel, PrevisoesLancamentosModel
from contas.models import ContasModel
from core.decorador import precisa_ser_gestor
# Create your views here.
@login_required(login_url='login')
@precisa_ser_gestor
def PrevisoesCriarView(request):
    formulario = PrevisoesFormulario(request.POST, request.FILES)
    if request.POST.get('ratear')=='True':
        ratear=True
    else:
        ratear=False
    if request.method=='POST':
        if formulario.is_valid():
            previsao = formulario.save(commit=False)
            previsao.usuario = request.user
            previsao.ratear=ratear
            previsao.save()

            #historico = CentroCustosHistoricoModel.objects.create(
             #   descricao=str("O centro de custos {} foi criado".format(cc.titulo))
            #).save()


            messages.add_message(request, messages.SUCCESS, 'A previsão foi adicionada com sucesso')
            return redirect('previsoes')
@login_required(login_url='login')
@precisa_ser_gestor
def PrevisoesView(request):
    contexto={
        'object_list':PrevisoesModel.objects.filter(status=True).order_by('-data_registro'),
        'formulario': PrevisoesFormulario,
        'historico':PrevisoesHistoricoModel.objects.all()
    }
    return render(request, 'previsoes/lista.html', contexto)
@login_required(login_url='login')
@precisa_ser_gestor
def PrevisoesDetalhesView(request, uuid):
    object = get_object_or_404(PrevisoesModel, uuid=uuid)
    contexto={
        'object':object,
        'object_list':ParcelasModel.objects.filter(previsao=object, status=True),
        'formulario':PrevisoesFormulario(instance=object),
        'formulario_lancamento': LancarPrevisoesFormulario(initial={"valor_inicial":object.valor})
    }
    return render(request, 'previsoes/detalhes_novo.html', contexto)
@login_required(login_url='login')
@precisa_ser_gestor
def PrevisoesEditarView(request, uuid):
    object = get_object_or_404(PrevisoesModel, uuid=uuid)
    if request.method=='POST':
        formulario = PrevisoesFormulario(request.POST, instance=object)
        if formulario.is_valid():
            formulario.save()
            #historico = CentroCustosHistoricoModel.objects.create(
             #   descricao=str("A conta {} foi editada".format(object.titulo))
            #).save()

            messages.add_message(request, messages.SUCCESS, "A preivsão {} foi atualizada com sucesso!".format(object.titulo))
            return redirect('previsoes_detalhes', object.uuid)
@login_required(login_url='login')
@precisa_ser_gestor
def PrevisoesDesabilitarView(request, uuid):
    object = get_object_or_404(PrevisoesModel, uuid=uuid)
    object.status=False
    object.save()
    ParcelasModel.objects.filter(previsao=object).update(status=False)
    #historico = CentroCustosHistoricoModel.objects.create(
     #   icone='delete',
      #  descricao=str("A previsão {} foi desabilitada".format(object.titulo))
    #).save()
    messages.add_message(request, messages.SUCCESS, "O previsão {} foi desabilitada com sucesso!".format(object.titulo))
    return redirect('previsoes')
@login_required(login_url='login')
@precisa_ser_gestor
def LancarPrevisoesView(request, uuid):
    object=get_object_or_404(PrevisoesModel, uuid=uuid)
    #Adicionar um lançamento novo com base na previsão
    formulario=LancarPrevisoesFormulario(request.POST, request.FILES)
    if formulario.is_valid():
        conta=ContasModel.objects.get(pk=request.POST.get('conta'))
        lancamento=LancamentosModel.objects.create(
            usuario=request.user,
            previsao=object,
            centro_custos=object.centro_custos,
            conta=conta,
            valor_inicial=formulario.cleaned_data['valor_inicial'],
            valor_desconto=formulario.cleaned_data['valor_desconto'],
            valor_acrescimo=formulario.cleaned_data['valor_acrescimo'],
            data_pagamento=formulario.cleaned_data['data_pagamento'],
            comprovante=request.FILES.get('comprovante'),
            descricao="Previsão {}, paga de forma unificada".format(object.titulo)

        ).save()
        lancamento=LancamentosModel.objects.last()
        PrevisoesLancamentosModel.objects.create(
            previsao=object,
            lancamento=lancamento
        ).save()
        #Desabilita as parcelas existentes
        ParcelasModel.objects.filter(previsao=object).update(status=False)
        #Cria uma única parcela
        ParcelasModel.objects.create(
            previsao=object,
            titulo="Pagamento unificado em {}".format(lancamento.data_registro),
            data_vencimento=object.data_previsao,
            valor=lancamento.valor(),
            status=True,
            efetivada=True,
            data_pagamento=formulario.cleaned_data['data_pagamento'])\
            .save()
        #Confirma o pagamento da previsão e registrar a data do pagamento
        object.efetivada=True
        object.data_pagamento=formulario.cleaned_data['data_pagamento']
        object.save()
        #Registrar no histórico
        PrevisoesHistoricoModel.objects.create(
            icone='save',
            descricao=str("A previsão {} foi paga em uma única parcela!".format(object.titulo))
        ).save()

        #Registra uma mensagem de sucesso
        messages.add_message(request, messages.SUCCESS, "A previsão foi convertida em um lançamento.")
        #Redireciona para o novo lançamento
        return redirect('previsoes_detalhes', object.uuid)
@login_required(login_url='login')
@precisa_ser_gestor
def ParcelasDetalhesView(request, uuid):
    object=get_object_or_404(ParcelasModel, uuid=uuid)
    contexto={
        'object':object,
        'formulario_lancamento': LancarPrevisoesFormulario(initial={"valor_inicial":object.valor}),
        'object_list':ParcelasModel.objects.filter(previsao=object.previsao, status=True).exclude(pk=object.pk)
    }
    return render(request, 'previsoes/detalhes_parcela_novo.html', contexto)
@login_required(login_url='login')
@precisa_ser_gestor
def LancarParcelaView(request, uuid):
    if request.method == 'POST':

        formulario = LancarPrevisoesFormulario(request.POST, request.FILES)
        object = ParcelasModel.objects.get(uuid=uuid)
        if formulario.is_valid():
            #Criar um lançamento com base na parcela
            LancamentosModel.objects.create(
                usuario=request.user,
                status=True,
                centro_custos=object.previsao.centro_custos,
                operacao=object.previsao.modalidade,
                descricao=str("Pagamento {}".format(object.titulo)),
                previsao=object.previsao,
                conta=formulario.cleaned_data['conta'],
                valor_inicial=object.valor,
                valor_acrescimo=formulario.cleaned_data['valor_acrescimo'],
                valor_desconto=formulario.cleaned_data['valor_desconto'],
                valor_final=(object.valor-formulario.cleaned_data['valor_desconto']+formulario.cleaned_data['valor_acrescimo']),
                data_pagamento=formulario.cleaned_data['data_pagamento'],
                comprovante=formulario.cleaned_data['comprovante'],

            ).save()
            lancamento=LancamentosModel.objects.last()
            #Registrar no Histórico de Lançamentos
            LancamentosHistoricoModel.objects.create(
                descricao=str("{} foi efetuado em {}".format(lancamento.descricao, lancamento.data_pagamento))
            ).save()
            #Alterar o status da parcela para pago
            object.efetivada=True
            object.data_pagamento=formulario.cleaned_data['data_pagamento']
            object.save()
            previsao=PrevisoesModel.objects.get(uuid=object.previsao.uuid)
            if ParcelasModel.objects.filter(previsao=previsao, efetivada=False):
                messages.add_message(request, messages.SUCCESS,
                                     "Ainda existem parcelas pendentes nesta previsão!")
            else:
                previsao.efetivada=True
                previsao.save()
                messages.add_message(request, messages.SUCCESS, "Todas as parcelas da previsão foram pagas, agora a previsão está registrada como efetivada!")
            messages.add_message(request, messages.SUCCESS, "O pagamento da parcela foi registrado com sucesso!")
            #Falta inserir uma função para converter a previsão em efetivada
            return redirect('previsoes_parcela_detalhes', object.uuid)
@login_required(login_url='login')
@precisa_ser_gestor
def ParcelaDesabilitarView(request, uuid):
    object = get_object_or_404(ParcelasModel, uuid=uuid)
    object.status=False
    object.save()
    historico = PrevisoesHistoricoModel.objects.create(
       icone='delete',
      descricao=str("A parcela {} foi desabilitada".format(object.titulo))
     ).save()


