from django.db import models
from fornecedores.models import *
class FornecedoresManager(models.Manager):
    def listar(self):
        return self.filter(status=True).order_by('-data_registro')