from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Membro, Evento, FotoGaleria, Mensagem, Auditoria, AlertaSeguranca


@admin.register(Membro)
class MembroAdmin(BaseUserAdmin):
    list_display = ('nome', 'email', 'telefone', 'nivel', 'is_active', 'date_joined')
    list_filter = ('nivel', 'is_active')
    search_fields = ('nome', 'email', 'telefone')
    ordering = ('nome',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Dados pessoais', {'fields': ('nome', 'telefone', 'foto', 'nivel', 'senha_seguranca')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('email', 'nome', 'telefone', 'password1', 'password2', 'nivel')}),
    )


admin.site.register(Evento)
admin.site.register(FotoGaleria)
admin.site.register(Mensagem)
admin.site.register(Auditoria)
admin.site.register(AlertaSeguranca)
