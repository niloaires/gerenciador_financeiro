from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from contratos.models import *
from previsoes.models import PrevisoesModel
from core.decorador import precisa_ser_gestor
from contratos.formularios import *
from lancamentos.models import LancamentosModel
from django.contrib.auth.decorators import login_required
import decimal
# Create your views here.
@login_required(login_url='login')
@precisa_ser_gestor
def ContratosView(request):
    contexto ={
        'object_list':ContratosModel.objects.filter(status=True).order_by('titulo'),
        'formulario': ContratoFormulario()
    }
    return render(request, 'contratos/lista.html', contexto)
@login_required(login_url='login')
@precisa_ser_gestor
def ContratosCriarView(request):
    formulario = ContratoFormulario(request.POST)
    if request.method == 'POST':
        if formulario.is_valid():
            contrato = formulario.save(commit=False)
            contrato.usuario = request.user
            contrato.save()


            messages.add_message(request, messages.SUCCESS,
                                 'O contrato {} foi adicionado com sucesso'.format(contrato.titulo))
            return redirect('contratos')
@login_required(login_url='login')
@precisa_ser_gestor
def ContratoDetalhesView(request, uuid):
    object = get_object_or_404(ContratosModel, uuid=uuid)
    if request.method=='GET':
        contexto = {
            'object':object,
            'object_list':LancamentosModel.objects.prefetch_related('centro_custos__obras_centrocustos__contrato'),
            #'aditivos_list':LancamentosModel.objects.prefetch_related('centro_custos__obras_centrocustos__contrato'),
            'formulario_aditivo': ContratoAdtivoFormulario(initial={'data_encerramento':object.data_encerramento}),
            'formulario_editar':ContratoFormulario(instance=object)
        }
        return render(request, 'contratos/detalhes_novo.html', contexto)
@login_required(login_url='login')
@precisa_ser_gestor
def ClienteEditarView(request, uuid):
    object = get_object_or_404(ClientesModel, uuid=uuid)
    if request.method=='POST':
        formulario = ContratoFormulario(request.POST, instance=object)
        if formulario.is_valid():
            formulario.save(commit=False)

            messages.add_message(request, messages.SUCCESS, "O contrato {} foi atualizado com sucesso!".format(object.nome))
            return redirect('contratos', object.uuid)
        else:
            return redirect('contratos')
    else:
        return redirect('contratos')
@login_required(login_url='login')
@precisa_ser_gestor
def ContratoDesabilitarView(request, uuid):
    object = get_object_or_404(ContratosModel, uuid=uuid)
    object.status=False
    object.save()
    messages.add_message(request, messages.SUCCESS, "O contrato {} foi desabilitado com sucesso!".format(object.nome))
    return redirect('contratos')

@login_required(login_url='login')
@precisa_ser_gestor
def ContratoAditivarView(request, uuid):
    object = get_object_or_404(ContratosModel, uuid=uuid)
    formulario=ContratoAdtivoFormulario(request.POST)
    usuario=User.objects.get(pk=request.user.pk)

    if request.method=='POST':
        if formulario.is_valid():
            AditivosModel.objects.create(
                usuario=usuario,
                contrato=object,
                tipo=request.POST.get('tipo'),
                acrescimo_valor=request.POST.get('acrescimo_valor'),
                novo_prazo=request.POST.get('novo_prazo'),

            ).save()
            messages.add_message(request, messages.SUCCESS,
                             "O contrato {} foi aditivado com sucesso!".format(object.titulo))
            return redirect('contratos_detalhes', object.uuid)
        messages.add_message(request, messages.WARNING,
                             "Houve um erro no processamento do aditivo!")
        for i in formulario.non_field_errors():
            messages.add_message(request, messages.INFO, i)
        return redirect('contratos_detalhes', object.uuid)
