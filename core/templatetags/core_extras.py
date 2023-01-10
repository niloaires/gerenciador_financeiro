from django import template
import locale
import datetime
from core.models import PerfilModel
from orcamentos.models import OrcamentosModel
from contratos.models import ContratosModel
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
register = template.Library()
@register.filter
def removervirgula(value):
    valor=str(value)
    return valor.replace(',','.')

@register.filter
def exibir_valor_em_real(value):
    if value is '':
        return str("R$: 0,00")
    return locale.currency(value, grouping=True, symbol=True)

@register.filter
def avatar_usuario(usuario):
    qs = PerfilModel.objects.get(usuario=usuario)
    if qs is False:
        avatar = 'None'
    elif qs.avatar is None:
        avatar = 'None'
    return qs.avatar

@register.simple_tag
def contar_orcamentos_nao_aprovados():

    qs=OrcamentosModel.objects.filter(aprovado=False, status=True)
    return qs

@register.simple_tag
def contar_contratos_proximos_do_vencimento():

    qs=ContratosModel.objects.filter(status=True, data_encerramento__month=datetime.datetime.now().month)
    return qs