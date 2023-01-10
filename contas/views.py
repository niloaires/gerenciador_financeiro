from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from contas.models import ContasModel, ContasHistoricoModel
from lancamentos.models import LancamentosModel
from contas.formularios import ContaFormulario, MovimentacoesFormulario
from django.contrib.auth.decorators import login_required
from core.decorador import precisa_ser_gestor
# Create your views here.
@login_required(login_url='login')
@precisa_ser_gestor
def ContasView(request):
    contexto={
        'object_list':ContasModel.objects.filter(status=True).order_by('titulo'),
        'formulario': ContaFormulario,
        'historico': ContasHistoricoModel.objects.all().order_by('-data_registro')
    }
    return render(request, 'contas/lista.html', contexto)
@login_required(login_url='login')
@precisa_ser_gestor
def ContasCriarView(request):
    formulario = ContaFormulario(request.POST)
    if request.method=='POST':
        if formulario.is_valid():
            conta = formulario.save(commit=False)
            conta.usuario = request.user
            conta.save()
            historico = ContasHistoricoModel.objects.create(
                descricao=str("A conta {} foi criada".format(conta.titulo))
            ).save()


            messages.add_message(request, messages.SUCCESS, 'A conta {} foi adicionada com sucesso'.format(conta.titulo))
            return redirect('contas')
@login_required(login_url='login')
@precisa_ser_gestor
def ContasDetalhesView(request, uuid):
    object = get_object_or_404(ContasModel, uuid=uuid)
    contexto={
        'object':object,
        'object_list': LancamentosModel.objects.filter(status=True, conta=object),
        'formulario_editar':ContaFormulario(instance=object),
        'formulario_pesquisa':MovimentacoesFormulario
    }
    return render(request, 'contas/detalhes.html', contexto)
@login_required(login_url='login')
@precisa_ser_gestor
def ContasEditarView(request, uuid):
    object = get_object_or_404(ContasModel, uuid=uuid)
    if request.method=='POST':
        formulario = ContaFormulario(request.POST, instance=object)
        if formulario.is_valid():
            formulario.save()
            historico = ContasHistoricoModel.objects.create(
                descricao=str("A conta {} foi editada".format(object.titulo))
            ).save()

            messages.add_message(request, messages.SUCCESS, "A conta {} foi atualizado com sucesso!".format(object.titulo))
            return redirect('contas_detalhes', object.uuid)
@login_required(login_url='login')
@precisa_ser_gestor
def ContasDesabilitarView(request, uuid):
    object = get_object_or_404(ContasModel, uuid=uuid)
    object.status=False
    object.save()
    historico = ContasHistoricoModel.objects.create(
        icone='delete',
        descricao=str("A conta {} foi desabilitada".format(object.titulo))
    ).save()
    messages.add_message(request, messages.SUCCESS, "A conta {} foi desabilitada com sucesso!".format(object.titulo))
    return redirect('contas')
