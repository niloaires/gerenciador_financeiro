from django.test import TestCase
from centroscustos.models import *
from previsoes.models import *
from lancamentos.models import *
import datetime

# Create your tests here.
def testemes(pk):
    l=LancamentosModel.objects.filter(centro_custos_id=pk).filter(data_pagamento__month=datetime.datetime.now().month)
    return l