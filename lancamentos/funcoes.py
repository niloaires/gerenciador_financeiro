from lancamentos.models import *
from obras.models import ObrasModel, LancamentosObrasModel
from centroscustos.models import CentroCustosModel
from previsoes.models import PrevisoesModel
import decimal
def LancamentoObra(request, obra):
    cc = CentroCustosModel.objects.get(pk=request.POST.get('centro_custos'))
    conta = ContasModel.objects.get(pk=request.POST.get('conta'))
    obra=ObrasModel.objects.get(uuid=obra)
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
        comprovante=request.POST.get('comprovante')

    ).save()
    lancamento = LancamentosModel.objects.latest('pk')
    #Criar LancamentoObra
    LancamentosObrasModel.objects.create(
        obra=obra,
        lancamento=lancamento
    ).save()
    lancamentoObra = LancamentosObrasModel.objects.latest('pk')
    return lancamentoObra




