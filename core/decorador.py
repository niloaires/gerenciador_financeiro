from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from core.models import PerfilModel as Perfil
from django.contrib import messages
def precisa_ser_gestor(function):
    def wrap(request, *args, **kwargs):
        perfil = Perfil.objects.get(usuario_id=request.user.id)
        if perfil.gestor==True:
            return function(request, *args, **kwargs)
        else:
            messages.add_message(request, messages.ERROR, 'Você não tem permissão para acessar este módulo!')
            return redirect('login')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def precisa_ser_engenheiro(function):
    def wrap(request, *args, **kwargs):
        perfil = Perfil.objects.get(usuario_id=request.user.id)
        if perfil.engenheiro==True:
            return function(request, *args, **kwargs)
        else:
            messages.add_message(request, messages.ERROR, 'Você não tem permissão para acessar este módulo!')
            return redirect('login')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap