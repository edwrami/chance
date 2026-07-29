from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('health/', views.health_check, name='health_check'),

    # Autenticación
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('cambiar-contrasena/', views.CambiarContrasenaView.as_view(), name='cambiar_contrasena'),
    path('panel/', views.DashboardView.as_view(), name='panel'),
    
    # Admin General
    path('panel/empresarios/', views.EmpresariosListView.as_view(), name='empresarios_list'),
    path('panel/empresarios/crear/', views.EmpresarioCreateView.as_view(), name='empresario_create'),
    path('panel/empresarios/<int:pk>/', views.EmpresarioDetailView.as_view(), name='empresario_detail'),
    path('panel/empresarios/<int:pk>/editar/', views.EmpresarioUpdateView.as_view(), name='empresario_update'),
    path('panel/empresarios/<int:pk>/toggle/', views.EmpresarioToggleActivoView.as_view(), name='empresario_toggle'),
    path('panel/comisiones/', views.ComisionGlobalListView.as_view(), name='comisiones_global'),
    path('panel/comisiones/crear/', views.ComisionGlobalCreateView.as_view(), name='comision_global_create'),
    
    # Empresario - Chanceros
    path('empresario/chanceros/', views.ChancerosListView.as_view(), name='chanceros_list'),
    path('empresario/chanceros/crear/', views.ChanceroCreateView.as_view(), name='chancero_create'),
    path('empresario/chanceros/<int:pk>/', views.ChanceroDetailView.as_view(), name='chancero_detail'),
    path('empresario/chanceros/<int:pk>/toggle/', views.ChanceroToggleActivoView.as_view(), name='chancero_toggle'),
    path('empresario/chanceros/<int:pk>/update/', views.ChanceroUpdateView.as_view(), name='chancero_update'),
    path('empresario/chanceros/<int:pk>/delete/', views.ChanceroDeleteView.as_view(), name='chancero_delete'),
    path('empresario/chanceros/<int:pk>/comision/', views.ComisionVendedorUpdateView.as_view(), name='comision_update'),
    
    # Empresario - Loterías
    path('empresario/loterias/', views.LoteriasListView.as_view(), name='loterias_list'),
    path('empresario/loterias/crear/', views.LoteriaCreateView.as_view(), name='loteria_create'),
    path('empresario/loterias/<int:pk>/', views.LoteriaDetailView.as_view(), name='loteria_detail'),
    path('empresario/loterias/<int:pk>/toggle/', views.LoteriaToggleActivoView.as_view(), name='loteria_toggle'),
    
    # Empresario - Planes de Premio
    path('empresario/planes/', views.PlanesPremioListView.as_view(), name='planes_list'),
    path('api/planes-premio/', views.PlanesPremioAPIView.as_view(), name='planes_premio_api'),
    path('api/validar-apuesta/', views.ValidarApuestaAPIView.as_view(), name='validar_apuesta_api'),
    path('api/calcular-premio/', views.CalcularPremioAPIView.as_view(), name='calcular_premio_api'),
    path('api/realizar-apuesta/', views.RealizarApuestaAPIView.as_view(), name='realizar_apuesta_api'),
    path('api/loterias-por-fecha/', views.LoteriasPorFechaView.as_view(), name='loterias_por_fecha_api'),
    path('api/topes-loterias/', views.TopesLoteriasAPIView.as_view(), name='topes_loterias_api'),
    path('empresario/planes/update/', views.PlanPremioUpdateView.as_view(), name='plan_update'),
    
    # Empresario - Topes
    path('empresario/topes/', views.TopesListView.as_view(), name='topes_list'),
    path('empresario/topes/crear/', views.TopeCreateView.as_view(), name='tope_create'),
    
    # Empresario - Ventas y Reportes
    path('empresario/ventas/', views.VentasListView.as_view(), name='ventas_list'),
    path('empresario/ventas/exportar/', views.ExportarVentasExcelView.as_view(), name='exportar_ventas'),
    path('empresario/acumulados/exportar/', views.ExportarAcumuladosExcelView.as_view(), name='exportar_acumulados'),
    path('empresario/consultar-numero/', views.ConsultarNumeroView.as_view(), name='consultar_numero'),
    path('empresario/apuestas/<int:pk>/pagar-premio/', views.PagarPremioView.as_view(), name='pagar_premio'),
    path('empresario/acumulados/', views.AcumuladosView.as_view(), name='acumulados'),
    path('empresario/reportes-chancero/', views.ReportesChanceroView.as_view(), name='reportes_chancero'),
    path('empresario/ganancias/', views.GananciasView.as_view(), name='ganancias'),
    path('empresario/liquidaciones-chancero/', views.LiquidacionesChanceroView.as_view(), name='liquidaciones_chancero'),
    path('empresario/exportar-datos/', views.ExportarDatosEmpresarioView.as_view(), name='exportar_datos_empresario'),
    
    # Empresario - Liquidaciones
    path('empresario/liquidaciones/', views.LiquidacionesListView.as_view(), name='liquidaciones_list'),
    path('empresario/liquidaciones/solicitar/', views.LiquidacionSolicitarView.as_view(), name='liquidaciones_solicitar'),
    path('empresario/liquidaciones/crear/', views.LiquidacionCreateView.as_view(), name='liquidacion_create'),
    path('empresario/liquidaciones/<int:pk>/pagar/', views.LiquidacionPagarView.as_view(), name='liquidacion_pagar'),
    
    # Empresario - Configuración
    path('empresario/config/', views.EmpresarioConfigView.as_view(), name='empresario_config'),
    path('empresario/config/twilio/', views.TwilioConfiguracionView.as_view(), name='twilio_config'),
    path('empresario/config/retencion/', views.ConfiguracionRetencionView.as_view(), name='configuracion_retencion'),
    path('empresario/limpiar-datos/', views.LimpiarDatosView.as_view(), name='limpiar_datos'),
    
    # Empresario - Manual
    path('empresario/manual/', TemplateView.as_view(template_name='empresario/manual_empresario.html'), name='manual_empresario'),
    
    # Chancero - Apuestas
    path('chancero/apuestas/nueva/', views.ApuestaCreateView.as_view(), name='apuesta_create'),
    path('chancero/apuestas/', views.MisApuestasListView.as_view(), name='mis_apuestas'),
    path('chancero/verificar/', views.VerificarDisponibilidadView.as_view(), name='verificar_disponibilidad'),
    path('chancero/mensaje/enviar/', views.EnviarMensajeView.as_view(), name='enviar_mensaje'),
    path('chancero/mensaje/enviar-texto/', views.EnviarMensajeTextoView.as_view(), name='enviar_mensaje_texto'),
    path('chancero/liquidaciones/', views.MiLiquidacionView.as_view(), name='mis_liquidaciones'),
    path('chancero/consultar-premio/', views.ConsultarPremioChanceroView.as_view(), name='consultar_premio_chancero'),
    path('chancero/reportes-personales/', views.ReportesPersonalesChanceroView.as_view(), name='reportes_personales_chancero'),
    path('chancero/exportar-datos/', views.ExportarDatosChanceroView.as_view(), name='exportar_datos_chancero'),
    
    # Chancero - Agenda de Clientes
    path('chancero/agenda/', views.AgendaClientesView.as_view(), name='agenda_clientes'),
    path('chancero/clientes/crear/', views.ClienteCreateView.as_view(), name='cliente_create'),
    path('chancero/clientes/<int:pk>/editar/', views.ClienteUpdateView.as_view(), name='cliente_update'),
    path('chancero/clientes/<int:pk>/eliminar/', views.ClienteDeleteView.as_view(), name='cliente_delete'),
    path('chancero/clientes/autocomplete/', views.ClientesAutocompleteView.as_view(), name='clientes_autocomplete'),
    path('chancero/clientes/<int:pk>/historial/', views.HistorialClienteView.as_view(), name='historial_cliente'),
    
    # Chancero - Estadísticas
    path('chancero/estadisticas/', views.EstadisticasPersonalesView.as_view(), name='estadisticas_personales'),
    path('chancero/ganancias-dia/', views.GananciasDiaView.as_view(), name='ganancias_dia'),
    path('chancero/informacion/', views.InformacionChanceroView.as_view(), name='informacion_chancero'),
    path('chancero/manual/', TemplateView.as_view(template_name='chancero/manual_chancero.html'), name='manual_chancero'),
    
    # Chancero - Tickets y QR
    path('chancero/ticket/<int:apuesta_id>/', views.GenerarTicketView.as_view(), name='generar_ticket'),
    path('chancero/qr/<int:apuesta_id>/', views.GenerarQRView.as_view(), name='generar_qr'),
]