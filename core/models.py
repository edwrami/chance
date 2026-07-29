from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .managers import UsuarioManager

class Usuario(AbstractUser):
    # Eliminamos username
    username = None
    documento = models.CharField(max_length=20, unique=True)
    
    # Datos personales obligatorios
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    direccion = models.TextField()
    telefono = models.CharField(max_length=20)
    telefono_familiar = models.CharField(max_length=20)
    observaciones = models.TextField(blank=True)
    
    # Email opcional
    email = models.EmailField(blank=True, null=True)
    
    # Configuración de retención de datos (solo empresario)
    dias_retencion_datos = models.PositiveSmallIntegerField(default=90, help_text="Días a mantener datos antes de depuración automática")
    
    # Relación con empresario (solo para chanceros)
    empresario = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to={'rol': 'empresario'},
        related_name='chanceros'
    )
    
    # Roles
    ROLES = (
        ('admin_general', 'Administrador General'),
        ('empresario', 'Empresario'),
        ('chancero', 'Chancero'),
    )
    rol = models.CharField(max_length=20, choices=ROLES, default='chancero')
    
    # Control de activación
    activo = models.BooleanField(default=False)
    requiere_activacion = models.BooleanField(default=True)
    
    # Fechas para empresarios
    fecha_afiliacion = models.DateField(null=True, blank=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    
    # Configuración del empresario (nombre comercial, logo, etc)
    configuracion = models.JSONField(default=dict, blank=True)
    
    # Comisión del Administrador General (porcentaje sobre ventas brutas, aplicable a empresarios)
    comision_admin_porcentaje = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0, 
        help_text="Porcentaje de comisión que cobra el Admin sobre las ventas brutas del empresario"
    )
    
    # Límite de chanceros por empresario (fijado por admin general)
    limite_chanceros = models.PositiveSmallIntegerField(default=10, null=True, blank=True)
    
    # Autorización de tipos de apuestas (configurado por empresario)
    autorizar_2c_directo = models.BooleanField(default=True)
    autorizar_2c_combinado = models.BooleanField(default=True)
    autorizar_3c_directo = models.BooleanField(default=True)
    autorizar_3c_combinado = models.BooleanField(default=True)
    autorizar_4c_directo = models.BooleanField(default=True)
    autorizar_4c_combinado = models.BooleanField(default=True)
    autorizar_5c_directo = models.BooleanField(default=True)
    autorizar_5c_combinado = models.BooleanField(default=True)
    autorizar_6c_directo = models.BooleanField(default=True)
    autorizar_6c_combinado = models.BooleanField(default=True)
    
    # Fechas de control
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Usar el manager personalizado
    objects = UsuarioManager()
    
    USERNAME_FIELD = 'documento'
    REQUIRED_FIELDS = ['nombres', 'apellidos', 'direccion', 'telefono', 'telefono_familiar']
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return f"{self.nombres} {self.apellidos} - {self.documento}"


class TwilioCredentials(models.Model):
    empresario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to={'rol': 'empresario'},
        related_name='twilio_credentials'
    )
    account_sid = models.CharField(max_length=64, help_text='Twilio Account SID')
    api_key_sid = models.CharField(max_length=64, help_text='Twilio API Key SID (empieza con SK)')
    api_key_secret = models.CharField(max_length=64, help_text='Twilio API Key Secret')
    sms_number = models.CharField(max_length=20, help_text='Formato E.164, ej. +12345678901')
    whatsapp_number = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        help_text='Número de sandbox de WhatsApp, ej. whatsapp:+14155238886'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Credenciales Twilio de {self.empresario.nombres} {self.empresario.apellidos}"


class Loteria(models.Model):
    empresario = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        limit_choices_to={'rol': 'empresario'},
        related_name='loterias'
    )
    nombre = models.CharField(max_length=100)
    
    # Días de la semana
    DIAS_SEMANA = (
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sábado', 'Sábado'),
        ('Domingo', 'Domingo'),
    )
    dias_habilitados = models.JSONField(default=list)
    
    hora_apertura = models.TimeField()
    hora_cierre = models.TimeField()
    tope_premio = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    activa = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Lotería'
        verbose_name_plural = 'Loterías'
        unique_together = ['empresario', 'nombre']
    
    def __str__(self):
        return f"{self.nombre}"


class PlanPremio(models.Model):
    empresario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to={'rol': 'empresario'},
        related_name='planes_premio'
    )
    cifras = models.PositiveSmallIntegerField()  # 2,3,4,5,6
    es_combinado = models.BooleanField(default=False)  # Si es combinado (mismas cifras en desorden)
    premio_por_peso = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Monto por cada peso apostado
    
    class Meta:
        verbose_name = 'Plan de Premio'
        verbose_name_plural = 'Planes de Premio'
        unique_together = ['empresario', 'cifras', 'es_combinado']
    
    def __str__(self):
        tipo = "Combinado" if self.es_combinado else "Directo"
        return f"{self.empresario.nombres} - {self.cifras} cifras ({tipo}): ${self.premio_por_peso} por peso"


class TopeNumero(models.Model):
    empresario = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        limit_choices_to={'rol': 'empresario'},
        related_name='topes'
    )
    loteria = models.ForeignKey(
        Loteria, 
        on_delete=models.CASCADE,
        related_name='topes'
    )
    # Eliminamos el campo 'numero' porque ahora el tope es por lotería
    tope_maximo = models.DecimalField(max_digits=12, decimal_places=2)
    acumulado_actual = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    class Meta:
        verbose_name = 'Tope por Lotería'
        verbose_name_plural = 'Topes por Lotería'
        unique_together = ['empresario', 'loteria']
    
    def __str__(self):
        return f"{self.loteria.nombre} - Tope ${self.tope_maximo}"


class Apuesta(models.Model):
    empresario = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        limit_choices_to={'rol': 'empresario'},
        related_name='apuestas_empresa'
    )
    chancero = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        limit_choices_to={'rol': 'chancero'},
        related_name='apuestas_chancero'
    )
    loteria = models.ForeignKey(
        Loteria, 
        on_delete=models.CASCADE,
        related_name='apuestas'
    )
    fecha_hora = models.DateTimeField(auto_now_add=True)
    numero = models.CharField(max_length=6)
    cifras = models.PositiveSmallIntegerField()
    monto_apostado = models.DecimalField(max_digits=12, decimal_places=2)
    premio_potencial = models.DecimalField(max_digits=12, decimal_places=2)
    
    ESTADOS = (
        ('activa', 'Activa'),
        ('pagada', 'Pagada'),
        ('anulada', 'Anulada'),
    )
    estado = models.CharField(max_length=10, choices=ESTADOS, default='activa')
    
    # Referencia a la liquidación que cubre esta apuesta
    liquidacion = models.ForeignKey(
        'Liquidacion',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='apuestas_liquidadas'
    )
    
    # Indica si la liquidación está pagada (autoriza pago de premios)
    liquidacion_pagada = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Apuesta'
        verbose_name_plural = 'Apuestas'
        ordering = ['-fecha_hora']
    
    def __str__(self):
        return f"{self.chancero.documento} - {self.loteria.nombre} - {self.numero}"


class AcumuladoNumero(models.Model):
    """Modelo para tracking del acumulado apostado a cada número por lotería"""
    empresario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to={'rol': 'empresario'},
        related_name='acumulados'
    )
    loteria = models.ForeignKey(
        Loteria,
        on_delete=models.CASCADE,
        related_name='acumulados'
    )
    numero = models.CharField(max_length=6)
    cifras = models.PositiveSmallIntegerField()
    monto_acumulado = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    fecha_ultima_apuesta = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Acumulado de Número'
        verbose_name_plural = 'Acumulados de Números'
        unique_together = ['empresario', 'loteria', 'numero', 'cifras']
        ordering = ['-monto_acumulado']
    
    def __str__(self):
        return f"{self.loteria.nombre} - {self.numero} (${self.monto_acumulado})"


class ComisionVendedor(models.Model):
    empresario = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        limit_choices_to={'rol': 'empresario'},
        related_name='comisiones'
    )
    chancero = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        limit_choices_to={'rol': 'chancero'},
        related_name='comision'
    )
    porcentaje = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Comisión de Vendedor'
        verbose_name_plural = 'Comisiones de Vendedores'
        unique_together = ['empresario', 'chancero']
    
    def __str__(self):
        return f"{self.chancero.documento} - {self.porcentaje}%"


class Liquidacion(models.Model):
    empresario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to={'rol': 'empresario'},
        related_name='liquidaciones_empresario'
    )
    chancero = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to={'rol': 'chancero'},
        related_name='liquidaciones_chancero'
    )
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    total_ventas = models.DecimalField(max_digits=12, decimal_places=2)
    comision_porcentaje = models.DecimalField(max_digits=5, decimal_places=2)
    comision_valor = models.DecimalField(max_digits=12, decimal_places=2)
    valor_empresario = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    ESTADOS = (
        ('solicitada', 'Solicitada'),
        ('pagada', 'Pagada'),
        ('cancelada', 'Cancelada'),
    )
    estado = models.CharField(max_length=10, choices=ESTADOS, default='solicitada')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_pago = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Liquidación'
        verbose_name_plural = 'Liquidaciones'

    def __str__(self):
        return f"{self.chancero.documento} - ${self.comision_valor}"


class Mensaje(models.Model):
    empresario = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        limit_choices_to={'rol': 'empresario'},
        related_name='mensajes_empresa'
    )
    chancero = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        limit_choices_to={'rol': 'chancero'},
        related_name='mensajes_chancero'
    )
    apuesta = models.ForeignKey(
        Apuesta, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='mensajes'
    )
    telefono_destino = models.CharField(max_length=20)
    contenido = models.TextField()
    
    TIPOS = (
        ('whatsapp', 'WhatsApp'),
        ('sms', 'SMS'),
    )
    tipo = models.CharField(max_length=10, choices=TIPOS)
    fecha_hora_envio = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Mensaje'
        verbose_name_plural = 'Mensajes'
    
    def __str__(self):
        return f"{self.tipo} a {self.telefono_destino}"


class PagoPremio(models.Model):
    """Registro de cada pago de premio realizado"""
    apuesta = models.ForeignKey(
        Apuesta,
        on_delete=models.CASCADE,
        related_name='pagos_premio'
    )
    monto_pagado = models.DecimalField(max_digits=12, decimal_places=2)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    pagado_por = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to={'rol__in': ['empresario', 'admin_general']},
        related_name='pagos_realizados'
    )
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Pago de Premio'
        verbose_name_plural = 'Pagos de Premios'
        ordering = ['-fecha_pago']

    def __str__(self):
        return f"Pago ${self.monto_pagado} - {self.apuesta.numero} ({self.apuesta.chancero.nombres})"


class ComisionGlobal(models.Model):
    """Comisión que el admin general cobra a cada empresario"""
    empresario = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        limit_choices_to={'rol': 'empresario'},
        related_name='comisiones_globales'
    )
    porcentaje = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Comisión Global'
        verbose_name_plural = 'Comisiones Globales'
    
    def __str__(self):
        return f"{self.empresario.documento} - {self.porcentaje}%"


class FacturaComision(models.Model):
    """Facturación de comisiones al admin general"""
    empresario = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        limit_choices_to={'rol': 'empresario'},
        related_name='facturas'
    )
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    total_ventas = models.DecimalField(max_digits=12, decimal_places=2)
    porcentaje_comision = models.DecimalField(max_digits=5, decimal_places=2)
    valor_comision = models.DecimalField(max_digits=12, decimal_places=2)
    
    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('pagada', 'Pagada'),
        ('vencida', 'Vencida'),
    )
    estado = models.CharField(max_length=10, choices=ESTADOS, default='pendiente')
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    fecha_pago = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Factura de Comisión'
        verbose_name_plural = 'Facturas de Comisiones'
    
    def __str__(self):
        return f"Factura {self.id} - {self.empresario.documento} - ${self.valor_comision}"


class ResultadoLoteria(models.Model):
    """Resultados ganadores de loterías"""
    loteria = models.ForeignKey(
        Loteria,
        on_delete=models.CASCADE,
        related_name='resultados'
    )
    fecha = models.DateField()
    numero_ganador = models.CharField(max_length=6)
    cifras = models.PositiveSmallIntegerField()
    creado_por = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to={'rol__in': ['admin_general', 'empresario']},
        related_name='resultados_creados'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Resultado de Lotería'
        verbose_name_plural = 'Resultados de Loterías'
        unique_together = ['loteria', 'fecha', 'numero_ganador']
    
    def __str__(self):
        return f"{self.loteria.nombre} - {self.fecha} - {self.numero_ganador}"


class Cliente(models.Model):
    """Modelo para agenda de clientes del chancero"""
    chancero = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to={'rol': 'chancero'},
        related_name='clientes'
    )
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, unique=True)
    direccion = models.TextField(blank=True)
    notas = models.TextField(blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nombre']
        indexes = [
            models.Index(fields=['chancero', 'telefono']),
            models.Index(fields=['activo']),
        ]
    
    def __str__(self):
        return f"{self.nombre} - {self.telefono}"


class HistorialCliente(models.Model):
    """Modelo para tracking de apuestas por cliente"""
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='historial'
    )
    apuesta = models.ForeignKey(
        Apuesta,
        on_delete=models.CASCADE,
        related_name='historial_clientes'
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Historial de Cliente'
        verbose_name_plural = 'Historiales de Clientes'
        ordering = ['-fecha_registro']
        indexes = [
            models.Index(fields=['cliente', 'fecha_registro']),
            models.Index(fields=['apuesta']),
        ]
    
    def __str__(self):
        return f"{self.cliente.nombre} - {self.apuesta.numero}"