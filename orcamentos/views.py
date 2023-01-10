from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from django.db.models import  Sum
from django.contrib import messages
from orcamentos.models import OrcamentosModel, OrcamentosHistoricoModel, ItensOrcamentosModel
from orcamentos.formularios import *
from previsoes.models import PrevisoesModel, PrevisoesHistoricoModel
from fornecedores.models import FornecedoresModel
from django.contrib.auth.decorators import login_required
from core.decorador import precisa_ser_gestor
import datetime
# Create your views here.
@login_required(login_url='login')
def FornecedorCriar(request):
    if request.method=='POST':
        #usuario=User.objects.get(pk=request.user.pk)
        formulario=ForcecedoresForms(request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.add_message(request, messages.SUCCESS, "Fornecedor registrado com sucesso!")
            return HttpResponse('<script type="text/javascript">self.close(); window.opener.location.reload(true)</script>')
        else:
            contexto = {
                'formulario': formulario
            }

            return render(request, 'orcamentos/popups/criar_fornecedor.html', contexto)

    else:
        contexto={
            'formulario':ForcecedoresForms()
        }
        return render(request, 'orcamentos/popups/criar_fornecedor.html', contexto)
@login_required(login_url='login')
def FornecedorLista(request):
    contexto={
        'object_list':FornecedoresModel.objects.filter(status=True).order_by('nome')
    }
    return render(request, 'orcamentos/lista_fornecedores.html', contexto)
@login_required(login_url='login')
def FornecedorEditar(request, uuid):
    instance=FornecedoresModel.objects.get(uuid=uuid)
    if request.method=='POST':
        #usuario=User.objects.get(pk=request.user.pk)
        formulario=ForcecedoresForms(request.POST, instance=instance)
        if formulario.is_valid():
            formulario.save()
            messages.add_message(request, messages.SUCCESS, "Fornecedor registrado com sucesso!")
            return HttpResponse('<script type="text/javascript">self.close(); window.opener.location.reload(true)</script>')
        else:
            contexto = {
                'formulario': formulario,
                'object':instance
            }

            return render(request, 'orcamentos/popups/editar_fornecedor.html', contexto)

    else:
        contexto={
            'formulario':ForcecedoresForms(instance=instance)
        }
        return render(request, 'orcamentos/popups/editar_fornecedor.html', contexto)

@login_required(login_url='login')
def ItemOrcamentoEditar(request, pk):
    object=ItensOrcamentosModel.objects.get(pk=pk)
    formulario=ItensOrcamentosFormularioModel
    if request.method=='POST':
        formulario=formulario(request.POST, instance=object)
        if formulario.is_valid():
            formulario.save()
            messages.add_message(request, messages.SUCCESS, "Item editado com sucesso!")
            return HttpResponse(
                '<script type="text/javascript">self.close(); window.opener.location.reload(true)</script>')
        contexto={
            'formulario':formulario(instance=object),
            'object':object
        }
        return render(request, 'orcamentos/popups/editar_deletar_item.html', contexto )
    else:
        contexto={
            'formulario':formulario,
            'object':object
        }
        return render(request, 'orcamentos/popups/editar_deletar_item.html', contexto)
@login_required(login_url='login')
def ItemOrcamentoDeletar(request, pk):
    object=ItensOrcamentosModel.objects.get(pk=pk)
    object.delete()
    messages.add_message(request, messages.SUCCESS, "Item excluído com sucesso!")
    return HttpResponse(
        '<script type="text/javascript">self.close(); window.opener.location.reload(true)</script>')



@login_required(login_url='login')
def NaturezaDespesasCriar(request):
    if request.method=='POST':
        #usuario=User.objects.get(pk=request.user.pk)
        formulario=ClassificacaoDespesasForms(request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.add_message(request, messages.SUCCESS, "Fornecedor registrado com sucesso!")
            return HttpResponse('<script type="text/javascript">self.close(); window.opener.location.reload(true)</script>')
        else:
            contexto = {
                'formulario': formulario
            }

            return render(request, 'orcamentos/popups/criar_natureza_despesa.html', contexto)

    else:
        contexto={
            'formulario':ClassificacaoDespesasForms
        }
        return render(request, 'orcamentos/popups/criar_natureza_despesa.html', contexto)
@login_required(login_url='login')
def OrcamentosCriarView(request):
    novo = ItensOrcamentosModel.objects.filter(item='#4fdifjidf')
    if request.method=='POST':
        usuario=request.user
        formulario=OrcamentoFormulario(request.POST)
        formset=ItensModelFormset(request.POST)


        if formulario.is_valid() and formset.is_valid():
            orcamento=formulario.save(commit=False)
            orcamento.usuario=usuario
            orcamento.save()
            for form in formset:
                item = form.save(commit=False)
                item.orcamento=orcamento
                item.save()
            return redirect('orcamentos_detalhes', orcamento.uuid)
    else:
        form = OrcamentoFormulario
        formset = ItensModelFormset(request.POST or None, queryset=novo)
        contexto={
            "formulario": form,
            "formset": formset,

        }
        return render(request, 'orcamentos/criar.html', contexto)
@login_required(login_url='login')
def OrcamentosView(request):
    usuario=User.objects.get(pk=request.user.pk)
    contexto={
        "object_list":OrcamentosModel.objects.filter(status=True, usuario=usuario)

    }
    return render(request, 'orcamentos/lista.html', contexto)
@login_required(login_url='login')
def OrcamentosDetalhesView(request, uuid):
    object=get_object_or_404(OrcamentosModel, uuid=uuid)

    contexto={
        "object":object,
        "object_list": ItensOrcamentosModel.objects.filter(orcamento=object),
        "formulario_previsao":PrevisaoOrcamentoform
    }
    return render(request, "orcamentos/detalhes_2.html", contexto)
@login_required(login_url='login')
def OrcamentoAprovarView(request, uuid):
    usuario = request.user.first_name
    object=get_object_or_404(OrcamentosModel, uuid=uuid)
    object.usuario=request.user
    object.aprovado=True
    object.data_autorizacao=datetime.datetime.now()
    object.save()
    #Salvar no histórico
    OrcamentosHistoricoModel.objects.create(
        descricao=str("O orçamento {} foi autorizado por {} em {}".format(object, usuario, datetime.datetime.now() )),
        icone="check"
    ).save()
    #Mensagem de confirmação
    messages.add_message(request, messages.SUCCESS, "O orçamento {} foi autorizado por {} com sucesso".format(object, request.user.first_name))
    previsao=PrevisoesModel.objects.create(
        titulo=str("{}".format(object)),
        centro_custos=object.obra.centrocusto,
        modalidade="saida",
        data_previsao=request.POST.get("data_previsao"),
        valor=object.valor_orcado(),

    )
    return redirect('orcamentos_detalhes', object.uuid)

@login_required(login_url='login')
@precisa_ser_gestor
def OrcamentosViewAdm(request):
    contexto={
        'object_list':OrcamentosModel.objects.all(),
        'relatorios':OrcamentosModel.objects.filter(aprovado=True).order_by('data_autorizacao')

    }
    return render(request, 'orcamentos/lista_adm.html', contexto)

@login_required(login_url='login')
@precisa_ser_gestor
def OrcamentosDetalhesViewAdm(request, uuid):
    object = get_object_or_404(OrcamentosModel, uuid=uuid)

    contexto = {
        'object':object,
        'object_list':ItensOrcamentosModel.objects.filter(orcamento=object),
        'formulario_aprovacao':DataPrevisaoAprovarOrcamentoForm

    }
    return render(request, 'orcamentos/detalhes_adm.html', contexto)


@login_required(login_url='login')
def OrcamentoConfirmarDeletar(request, uuid):
    instance = OrcamentosModel.objects.get(uuid=uuid)

    contexto = {
        'object': instance
    }
    return render(request, 'orcamentos/popups/deletar_orcamento.html', contexto)

@login_required(login_url='login')
def OrcamentoDeletar(request, uuid):
    instance = OrcamentosModel.objects.get(uuid=uuid)
    if instance.aprovado==True:
        messages.add_message(request, messages.INFO, "Este orçamento já foi aprovado, por isso não pode mais ser excluído!")
        return HttpResponse('<script type="text/javascript">self.close(); window.opener.location.reload(true)</script>')
    else:
        itens=ItensOrcamentosModel.objects.filter(orcamento=instance)
        itens.delete()
        instance.delete()
        messages.add_message(request, messages.SUCCESS, "Orçamento excluído com sucesso")
        return redirect('orcamentos')
@login_required(login_url='login')
@precisa_ser_gestor
def OrcamentosAprovarViewAdm(request, uuid):
    usuario=User.objects.get(pk=request.user.pk)
    object = get_object_or_404(OrcamentosModel, uuid=uuid)
    itens=ItensOrcamentosModel.objects.filter(orcamento=object)
    if request.method=='POST':
        if object.aprovado == True:
            messages.add_message(request, messages.INFO,
                                 'O orçamento {} já foi aprovado em {}'.format(object, object.data_autorizacao))
            return redirect('orcamentos_detalhes_adm', object.uuid)
        else:
            if itens.count() == 0:
                messages.add_message(request, messages.INFO, 'Operação impossível, não há itens na composição do orçamento')
                return redirect('orcamentos_detalhes_adm', object.uuid)
            else:
                for i in itens:
                    PrevisoesModel.objects.create(
                        usuario=usuario,
                        ratear=False,
                        titulo=i.item,
                        fornecedor=i.fornecedor,
                        centro_custos=i.orcamento.obra.centrocusto,
                        classificacao_despesa=i.classificacao_despesa,
                        modalidade='saida',
                        valor=i.subtotal(),
                        data_previsao=request.POST.get('data_previsao'),
                        parcelas=1,
                        intervado=1,
                        status=True,
                        efetivada=False,

                    ).save()
                object.aprovado=True
                object.data_autorizacao=datetime.datetime.now()
                object.descricao=str("Ok")
                object.usuario=usuario
                object.save()
                messages.add_message(request, messages.SUCCESS, '{} itens foram convertido em previsão de pagamento'.format(itens.count()))
                messages.add_message(request, messages.SUCCESS, '{} Foi autorizado'.format(object))
                messages.add_message(request, messages.SUCCESS, '{} passou a ser responsabilidade de {} {}'.format(object, usuario.first_name, usuario.last_name))
                return redirect('previsoes')
    else:
        HttpResponseForbidden()

