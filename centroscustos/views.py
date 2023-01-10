from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum, Case, When, Value, DecimalField
from django.forms import DecimalField
import datetime
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
from django.contrib import messages
from centroscustos.models import CentroCustosModel, PlanosContaModel, CentroCustosHistoricoModel
from centroscustos.formularios import CentroCustosFormulario, PlanoContasFormulario
from django.contrib.auth.decorators import login_required
from core.decorador import precisa_ser_gestor
from previsoes.models import PrevisoesModel
from relatorios.formularios import FormPesquisaGeral
# Create your views here.
@login_required(login_url='login')
@precisa_ser_gestor
def PlanoContasCriarView(request):
    formulario = PlanoContasFormulario(request.POST)
    if request.method=='POST':
        if formulario.is_valid():
            cc = formulario.save(commit=False)
            cc.usuario = request.user
            cc.save()
            historico = CentroCustosHistoricoModel.objects.create(
                descricao=str("O centro de custos {} foi criado".format(cc.titulo))
            ).save()


            messages.add_message(request, messages.SUCCESS, 'O plano {} foi adicionado com sucesso'.format(cc.titulo))
            return redirect('plano_contas')
@login_required(login_url='login')
@precisa_ser_gestor
def PlanoContasView(request):
    object_list=PlanosContaModel.objects.filter(status=True).values('titulo', 'uuid',
                   'descricao').annotate(acumulado=Sum('centros_plano__lancamentos_centrocusto__valor_final')).order_by('titulo')
    acumulado=object_list.aggregate(total=Sum('centros_plano__lancamentos_centrocusto__valor_final'))
    contexto={
        'object_list':object_list,
        'total':acumulado['total'],
        'formulario': PlanoContasFormulario,
        'historico': CentroCustosHistoricoModel.objects.all().order_by('-data_registro')
    }
    return render(request, 'centroscustos/lista_planos.html', contexto)
@login_required(login_url='login')
@precisa_ser_gestor
def PlanoContasDetalhesView(request, uuid):
    object = get_object_or_404(PlanosContaModel, uuid=uuid)
    contexto={
        'object':object,
        'formulario':PlanoContasFormulario(instance=object),
        'object_list': PrevisoesModel.objects.filter(status=True, centro_custos__plano_contas=object),
        'formulario_pesquisa':FormPesquisaGeral
    }
    return render(request, 'centroscustos/detalhes_novo_planos.html', contexto)
@login_required(login_url='login')
@precisa_ser_gestor
def PlanoContasEditarView(request, uuid):
    object = get_object_or_404(PlanosContaModel, uuid=uuid)
    if request.method=='POST':
        formulario = PlanoContasFormulario(request.POST, instance=object)
        if formulario.is_valid():
            formulario.save()


            messages.add_message(request, messages.SUCCESS, "O plano de contas {} foi atualizado com sucesso!".format(object.titulo))
            return redirect('planocontas_detalhes', object.uuid)
@login_required(login_url='login')
@precisa_ser_gestor
def PlanoContasDesabilitarView(request, uuid):
    object = get_object_or_404(CentroCustosModel, uuid=uuid)
    object.status=False
    object.save()
    historico = CentroCustosHistoricoModel.objects.create(
        icone='delete',
        descricao=str("O centro de custos {} foi desabilitado".format(object.titulo))
    ).save()
    messages.add_message(request, messages.SUCCESS, "O centro de custos {} foi desabilitado com sucesso!".format(object.titulo))
    return redirect('centrocustos')
@login_required(login_url='login')
@precisa_ser_gestor
def CentroCustosCriarView(request):
    formulario = CentroCustosFormulario(request.POST)
    if request.method=='POST':
        if formulario.is_valid():
            cc = formulario.save(commit=False)
            cc.usuario = request.user
            cc.save()
            historico = CentroCustosHistoricoModel.objects.create(
                descricao=str("O centro de custos {} foi criado".format(cc.titulo))
            ).save()


            messages.add_message(request, messages.SUCCESS, 'O centro de custos {} foi adicionado com sucesso'.format(cc.titulo))
            return redirect('centrocustos')
@login_required(login_url='login')
@precisa_ser_gestor
def CentrosCustosView(request):
    object_list=CentroCustosModel.objects.filter(status=True)
    acumulado=object_list.aggregate(total=Sum('lancamentos_centrocusto__valor_final'))
    #CentroCustosModel.objects.filter(=)
    contexto={
        'object_list':object_list,
        'total':acumulado['total'],
        'formulario': CentroCustosFormulario,
        'historico': CentroCustosHistoricoModel.objects.all().order_by('-data_registro')
    }
    return render(request, 'centroscustos/lista.html', contexto)
@login_required(login_url='login')
@precisa_ser_gestor
def CentroCustosDetalhesView(request, uuid):
    object = get_object_or_404(CentroCustosModel, uuid=uuid)
    contexto={
        'object':object,
        'formulario':CentroCustosFormulario(instance=object),
        'object_list':object.previsoes_centrocusto.all(),
        'formulario_pesquisa':FormPesquisaGeral
    }
    return render(request, 'centroscustos/detalhes_novo.html', contexto)
@login_required(login_url='login')
@precisa_ser_gestor
def CentroCustosEditarView(request, uuid):
    object = get_object_or_404(CentroCustosModel, uuid=uuid)
    if request.method=='POST':
        formulario = CentroCustosFormulario(request.POST, instance=object)
        if formulario.is_valid():
            formulario.save()
            historico = CentroCustosHistoricoModel.objects.create(
                descricao=str("O Centro de custos {} foi editada".format(object.titulo))
            ).save()

            messages.add_message(request, messages.SUCCESS, "O centro de custos {} foi atualizado com sucesso!".format(object.titulo))
            return redirect('centrocustos_detalhes', object.uuid)
@login_required(login_url='login')
@precisa_ser_gestor
def CentroCustosDesabilitarView(request, uuid):
    object = get_object_or_404(CentroCustosModel, uuid=uuid)
    object.status=False
    object.save()
    historico = CentroCustosHistoricoModel.objects.create(
        icone='delete',
        descricao=str("O centro de custos {} foi desabilitado".format(object.titulo))
    ).save()
    messages.add_message(request, messages.SUCCESS, "O centro de custos {} foi desabilitado com sucesso!".format(object.titulo))
    return redirect('centrocustos')