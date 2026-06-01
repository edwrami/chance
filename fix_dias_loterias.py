import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chancepro.settings')
django.setup()

from core.models import Loteria

# Mapeo de días en minúsculas a mayúsculas
dias_mapping = {
    'lunes': 'Lunes',
    'martes': 'Martes',
    'miercoles': 'Miércoles',
    'jueves': 'Jueves',
    'viernes': 'Viernes',
    'sabado': 'Sábado',
    'domingo': 'Domingo'
}

# Obtener todas las loterías
loterias = Loteria.objects.all()

print(f"Total de loterías: {loterias.count()}")

for loteria in loterias:
    dias_habilitados = loteria.dias_habilitados
    print(f"\nLotería: {loteria.nombre}")
    print(f"Días actuales: {dias_habilitados}")
    
    # Corregir días
    nuevos_dias = []
    for dia in dias_habilitados:
        dia_corregido = dias_mapping.get(dia.lower(), dia)
        nuevos_dias.append(dia_corregido)
    
    if nuevos_dias != dias_habilitados:
        loteria.dias_habilitados = nuevos_dias
        loteria.save()
        print(f"Días corregidos: {nuevos_dias}")
    else:
        print("Días ya están correctos")

print("\n✅ Corrección completada")
