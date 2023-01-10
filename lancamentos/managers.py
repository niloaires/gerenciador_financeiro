from django.db import models

class lancamentosBusca(models.QuerySet):
    def search(self, **kwargs):
        qs = self
        if kwargs.get('descricao', ''):
            qs= qs.filter(descricao_icontains=kwargs['descricao'])
        if kwargs.get('centroCustos', []):
            qs = qs.filter(centro_custos_icontains=kwargs['centroCustos'])
        if kwargs.get('classificacao', []):
            qs = qs.filter(classificacao_despesa_icontains=kwargs['classificacao'])
        return qs
