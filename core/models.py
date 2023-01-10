from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib import admin

import PIL
from uuid import uuid4
# Create your models here.
class PerfilModel(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_usuario')
    engenheiro = models.BooleanField(default=True, verbose_name='É engenheiro')
    gestor = models.BooleanField(default=False, verbose_name="É gestor")
    avatar = models.ImageField(upload_to="avatar_usuario", blank=True, null=True, verbose_name="Avatar")
    def __str__(self):
        return str("{} {}".format(self.usuario.first_name, self.usuario.last_name))
    def funcao(self):
        if self.engenheiro and self.gestor == True:
            return str("Engenheiro e gestor")
        return str("Engenheiro")
    class Meta:
        verbose_name_plural="Perfis de usuários"
        verbose_name="Perfil de usuário"

def criar_usuario(sender, instance, created, **kwargs):

    if created:
        usuario=User.objects.get(pk=instance.pk)
        PerfilModel.objects.create(
            usuario=usuario,
            gestor=False,
            engenheiro=False,
            avatar='avatar_usuario/sem_avatar.png'
        ).save()
        n = 0


post_save.connect(criar_usuario, sender=User, dispatch_uid="my_unique_identifier")
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'engenheiro', 'gestor']
admin.site.register(PerfilModel)