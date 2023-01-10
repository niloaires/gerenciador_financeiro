from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum, Count
from fornecedores.models import FornecedoresModel
from lancamentos.models import FornecedoresLancamentosModel, LancamentosModel
from fornecedores.formularios import CriarFornecedorModelForm, CriarLancamentoFornecedorFormulario
from previsoes.models import PrevisoesModel, PrevisoesFornecedoresModel, ParcelasModel
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
from core.decorador import precisa_ser_gestor
# Create your views here.
@login_required(login_url='login')
@precisa_ser_gestor
def FornecedoresView(request):
    object_list=FornecedoresModel.objects.filter(status=True).order_by('nome')
    contexto = {
        'object_list': object_list,
        'formulario': CriarFornecedorModelForm
    }
    return render(request, 'fornecedores/lista.html', contexto)
@login_required(login_url='login')
@precisa_ser_gestor
def FornecedorCriarView(request):
    formulario = CriarFornecedorModelForm(request.POST)
    if request.method == 'POST':
        if formulario.is_valid():
            fornecedor = formulario.save(commit=False)
            fornecedor.save()

            #historico = ClientesHistoricoModel.objects.create(
            #    descricao=str("A conta {} foi criada".format(cliente.nome))
            #).save()

            messages.add_message(request, messages.SUCCESS,
                                 'O fornecedor {} foi adicionado com sucesso'.format(fornecedor.nome))
            return redirect('fornecedor_detalhes', fornecedor.uuid)
@login_required(login_url='login')
@precisa_ser_gestor
def FornecedorDetalhesView(request, uuid):
    object = get_object_or_404(FornecedoresModel, uuid=uuid)
    object_list = PrevisoesModel.objects.filter(fornecedor__uuid=uuid, status=True, efetivada=False).order_by('-data_registro')
    lancamentos_list = LancamentosModel.objects.filter(previsao__fornecedor__uuid=uuid, status=True).order_by('-data_registro')
    acumulado=FornecedoresLancamentosModel.objects.filter(fornecedor__uuid=uuid).select_related('lancamento').values('lancamento__valor_final').aggregate(total=Sum('lancamento__valor_final'))
    if request.method=='GET':
        contexto = {
            'object':object,
            'object_list':object_list,
            'lancamentos_list':lancamentos_list,
            'formulario_editar':CriarFornecedorModelForm(instance=object),
            'acumulado':acumulado['total']
        }
        return render(request, 'fornecedores/detalhes_novo.html', contexto)
    elif request.method=='POST':
        formulario=CriarFornecedorModelForm(request.POST, instance=object)
        if formulario.is_valid():
            fornecedor=formulario.save()
            messages.add_message(request, messages.SUCCESS,
                                 'O fornecedor {} foi editado com sucesso'.format(fornecedor.nome))
            return redirect('fornecedor_detalhes', fornecedor.uuid)
@login_required(login_url='login')
@precisa_ser_gestor
def CriarLancamentoFornecedor(request, uuid):
    fornecedor=FornecedoresModel.objects.get(uuid=uuid)

    if request.method=='POST':
        formulario = CriarLancamentoFornecedorFormulario(request.POST)
        if formulario.is_valid():
            #Criar uma Previsão
            PrevisoesModel.objects.create(
                usuario=request.user,
                titulo=formulario.cleaned_data['descricao'],
                centro_custos=formulario.cleaned_data['centro_custos'],
                modalidade=formulario.cleaned_data['modalidade'],
                valor=formulario.cleaned_data['valor'],
                data_previsao=formulario.cleaned_data['data_pagamento'],
                parcelas=formulario.cleaned_data['parcelas'],
                intervado=formulario.cleaned_data['intervalo'],
                referencia=str("{} - {}".format(formulario.cleaned_data['modalidade'], fornecedor.nome))

            ).save()
            # Estanciar a previsão recém criada
            previsao = PrevisoesModel.objects.latest('pk')
            #Criar um registro na tabela que une Fornecedor e Previsão
            PrevisoesFornecedoresModel.objects.create(
                fornecedor=fornecedor,
                previsao=previsao
            ).save()
            #Verificar se deve ou não registrar como lançamento
            if request.POST.get('registrar_lancamento')=='on':
                #Iniciar o registro do Lançamento
                LancamentosModel.objects.create(
                    usuario=request.user,
                    operacao=formulario.cleaned_data['modalidade'],
                    centro_custos=formulario.cleaned_data['centro_custos'],
                    descricao=previsao.titulo,
                    previsao=previsao,
                    conta=formulario.cleaned_data['conta'],
                    valor_inicial=formulario.cleaned_data['valor'],
                    valor_desconto=formulario.cleaned_data['valor_desconto'],
                    valor_acrescimo=formulario.cleaned_data['valor_acrescimo'],
                    data_pagamento=formulario.cleaned_data['data_pagamento']

                ).save()
                lancamento=LancamentosModel.objects.latest('pk')
                #Associar o lançamento ao fornecedor
                FornecedoresLancamentosModel.objects.create(
                    fornecedor=fornecedor,
                    lancamento=lancamento
                ).save()
                #Efetivar previsão e todas as suas parcelas.
                previsao.efetivada=True
                previsao.save()
                ParcelasModel.objects.filter(previsao=previsao).update(efetivada=True, data_pagamento=formulario.cleaned_data['data_pagamento'])
                messages.add_message(request, messages.SUCCESS, "O lançamento {} foi registrado".format(lancamento.descricao))
                return redirect('lancamentos_detalhes', lancamento.uuid)
            else:
                messages.add_message(request, messages.SUCCESS,
                                     "A previsão {} foi registrada".format(previsao.titulo))
                return redirect('previsoes_detalhes', previsao.uuid)

        else:
            contexto={
                'formulario':formulario
            }
            return render(request, 'relatorios/pesquisa_geral.html', contexto)


