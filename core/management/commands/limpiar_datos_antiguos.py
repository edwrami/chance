from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from core.models import Apuesta, AcumuladoNumero, Liquidacion, ResultadoLoteria


class Command(BaseCommand):
    help = 'Limpia datos antiguos de la base de datos según la configuración de retención'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dias',
            type=int,
            help='Días de retención (sobrescribe la configuración del empresario)',
        )
        parser.add_argument(
            '--empresario-id',
            type=int,
            help='ID del empresario específico para limpiar (si no se especifica, limpia todos)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simula la limpieza sin eliminar datos',
        )

    def handle(self, *args, **options):
        dias = options.get('dias')
        empresario_id = options.get('empresario_id')
        dry_run = options.get('dry_run', False)

        if dry_run:
            self.stdout.write(self.style.WARNING('MODO SIMULACIÓN - No se eliminarán datos'))

        # Calcular fecha límite
        if dias:
            fecha_limite = timezone.now() - timedelta(days=dias)
            self.stdout.write(f'Usando días de retención: {dias}')
        else:
            # Usar configuración de cada empresario
            from core.models import Usuario
            empresarios = Usuario.objects.filter(rol='empresario')
            if empresario_id:
                empresarios = empresarios.filter(id=empresario_id)
            
            if not empresarios.exists():
                self.stdout.write(self.style.ERROR('No se encontraron empresarios'))
                return

            # Usar el mínimo de días de retención entre los empresarios
            min_dias = min(emp.dias_retencion_datos for emp in empresarios)
            fecha_limite = timezone.now() - timedelta(days=min_dias)
            self.stdout.write(f'Usando días de retención mínimos: {min_dias}')

        self.stdout.write(f'Fecha límite: {fecha_limite.strftime("%Y-%m-%d")}')

        # Filtrar por empresario si se especificó
        apuestas_query = Apuesta.objects.filter(fecha_hora__lt=fecha_limite)
        if empresario_id:
            apuestas_query = apuestas_query.filter(empresario_id=empresario_id)

        # Contar registros a eliminar
        total_apuestas = apuestas_query.count()
        total_acumulados = AcumuladoNumero.objects.filter(
            fecha_ultima_apuesta__lt=fecha_limite
        ).count()
        total_liquidaciones = Liquidacion.objects.filter(
            fecha_inicio__lt=fecha_limite
        ).count()
        total_resultados = ResultadoLoteria.objects.filter(
            fecha__lt=fecha_limite
        ).count()

        self.stdout.write(f'Apuestas a eliminar: {total_apuestas}')
        self.stdout.write(f'Acumulados a eliminar: {total_acumulados}')
        self.stdout.write(f'Liquidaciones a eliminar: {total_liquidaciones}')
        self.stdout.write(f'Resultados a eliminar: {total_resultados}')
        self.stdout.write(f'Total registros: {total_apuestas + total_acumulados + total_liquidaciones + total_resultados}')

        if dry_run:
            self.stdout.write(self.style.SUCCESS('Simulación completada. No se eliminaron datos.'))
            return

        # Confirmar eliminación
        respuesta = input('¿Está seguro de eliminar estos datos? (s/n): ')
        if respuesta.lower() != 's':
            self.stdout.write(self.style.WARNING('Operación cancelada'))
            return

        # Eliminar datos
        apuestas_eliminadas = apuestas_query.delete()[0]
        acumulados_eliminados = AcumuladoNumero.objects.filter(
            fecha_ultima_apuesta__lt=fecha_limite
        ).delete()[0]
        liquidaciones_eliminadas = Liquidacion.objects.filter(
            fecha_inicio__lt=fecha_limite
        ).delete()[0]
        resultados_eliminados = ResultadoLoteria.objects.filter(
            fecha__lt=fecha_limite
        ).delete()[0]

        self.stdout.write(self.style.SUCCESS(f'Apuestas eliminadas: {apuestas_eliminadas}'))
        self.stdout.write(self.style.SUCCESS(f'Acumulados eliminados: {acumulados_eliminados}'))
        self.stdout.write(self.style.SUCCESS(f'Liquidaciones eliminadas: {liquidaciones_eliminadas}'))
        self.stdout.write(self.style.SUCCESS(f'Resultados eliminados: {resultados_eliminados}'))
        self.stdout.write(self.style.SUCCESS('Limpieza completada exitosamente'))
