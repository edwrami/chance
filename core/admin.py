from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import *

# ========== FORMULARIOS PERSONALIZADOS PARA USUARIO ==========

class UsuarioCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ('documento', 'nombres', 'apellidos', 'direccion', 'telefono',
                  'telefono_familiar', 'email', 'rol', 'activo', 'empresario',
                  'fecha_afiliacion', 'fecha_vencimiento')

    def clean_username(self):
        return None


class UsuarioChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Usuario
        fields = '__all__'


# ========== ADMIN PERSONALIZADO PARA USUARIO ==========

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    form = UsuarioChangeForm
    add_form = UsuarioCreationForm

    list_display = ('documento', 'nombres', 'apellidos', 'rol', 'activo', 'empresario')
    list_filter = ('rol', 'activo')
    search_fields = ('documento', 'nombres', 'apellidos', 'email')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {'fields': ('documento', 'password')}),
        ('Informacion personal', {
            'fields': ('nombres', 'apellidos', 'direccion', 'telefono',
                      'telefono_familiar', 'email', 'observaciones')
        }),
        ('Roles y permisos', {
            'fields': ('rol', 'activo', 'requiere_activacion', 'empresario',
                      'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Fechas de afiliacion (solo empresarios)', {
            'fields': ('fecha_afiliacion', 'fecha_vencimiento'),
            'classes': ('collapse',)
        }),
        ('Configuracion', {
            'fields': ('configuracion',),
            'classes': ('collapse',)
        }),
        ('Fechas importantes', {
            'fields': ('last_login', 'date_joined', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('documento', 'nombres', 'apellidos', 'direccion', 'telefono',
                      'telefono_familiar', 'email', 'rol', 'empresario',
                      'fecha_afiliacion', 'fecha_vencimiento', 'password1', 'password2'),
        }),
    )

    readonly_fields = ('created_at', 'updated_at', 'last_login', 'date_joined')


# ========== ADMIN PARA LOTERIA ==========
# CORREGIDO: Eliminado filter_horizontal porque dias_habilitados es JSONField

@admin.register(Loteria)
class LoteriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'empresario', 'activa', 'hora_apertura', 'hora_cierre')
    list_filter = ('activa', 'empresario')
    search_fields = ('nombre', 'empresario__documento')


# ========== ADMIN PARA PLAN PREMIO ==========

@admin.register(PlanPremio)
class PlanPremioAdmin(admin.ModelAdmin):
    list_display = ('empresario', 'cifras', 'es_combinado', 'premio_por_peso')
    list_filter = ('empresario', 'es_combinado')
    search_fields = ('empresario__nombres',)


# ========== ADMIN PARA TOPE POR LOTERIA ==========

@admin.register(TopeNumero)
class TopeNumeroAdmin(admin.ModelAdmin):
    list_display = ('loteria', 'tope_maximo', 'acumulado_actual')
    list_filter = ('empresario', 'loteria')
    search_fields = ('loteria__nombre',)
    readonly_fields = ('acumulado_actual',)


# ========== ADMIN PARA APUESTA ==========

@admin.register(Apuesta)
class ApuestaAdmin(admin.ModelAdmin):
    list_display = ('chancero', 'loteria', 'numero', 'monto_apostado', 'premio_potencial', 'estado', 'fecha_hora')
    list_filter = ('estado', 'loteria', 'empresario')
    search_fields = ('chancero__documento', 'numero')
    readonly_fields = ('fecha_hora', 'premio_potencial')


# ========== ADMIN PARA COMISION VENDEDOR ==========

@admin.register(ComisionVendedor)
class ComisionVendedorAdmin(admin.ModelAdmin):
    list_display = ('chancero', 'porcentaje')
    list_filter = ('empresario',)
    search_fields = ('chancero__documento', 'chancero__nombres')


# ========== ADMIN PARA LIQUIDACION ==========

@admin.register(Liquidacion)
class LiquidacionAdmin(admin.ModelAdmin):
    list_display = ('chancero', 'fecha_inicio', 'fecha_fin', 'comision_valor', 'estado')
    list_filter = ('estado', 'empresario')
    search_fields = ('chancero__documento',)
    readonly_fields = ('fecha_solicitud',)


# ========== ADMIN PARA MENSAJE ==========

@admin.register(Mensaje)
class MensajeAdmin(admin.ModelAdmin):
    list_display = ('chancero', 'tipo', 'telefono_destino', 'fecha_hora_envio')
    list_filter = ('tipo', 'empresario')
    search_fields = ('telefono_destino', 'chancero__documento')
    readonly_fields = ('fecha_hora_envio',)


# ========== ADMIN PARA COMISION GLOBAL ==========

@admin.register(ComisionGlobal)
class ComisionGlobalAdmin(admin.ModelAdmin):
    list_display = ('empresario', 'porcentaje', 'activo')
    list_filter = ('activo',)
    search_fields = ('empresario__documento', 'empresario__nombres')


# ========== ADMIN PARA FACTURA COMISION ==========

@admin.register(FacturaComision)
class FacturaComisionAdmin(admin.ModelAdmin):
    list_display = ('empresario', 'fecha_inicio', 'fecha_fin', 'valor_comision', 'estado')
    list_filter = ('estado', 'empresario')
    search_fields = ('empresario__documento',)
    readonly_fields = ('fecha_generacion',)
