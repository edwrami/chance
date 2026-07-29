import os
import django
import subprocess

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chancepro.settings')
django.setup()

# Lista de todas las migraciones
migraciones = [
    '0001_initial',
    '0002_usuario_cifras_maximas_usuario_cifras_minimas_and_more',
    '0003_apuesta_liquidacion_apuesta_liquidacion_pagada',
    '0004_resultadoloteria',
    '0005_loteria_tope_premio',
    '0006_alter_planpremio_unique_together_and_more',
    '0007_remove_usuario_cifras_maximas_and_more',
    '0008_alter_planpremio_unique_together_and_more',
    '0009_acumuladonumero',
    '0010_usuario_dias_retencion_datos',
    '0011_cliente_historialcliente_and_more',
    '0012_pagopremio',
    '0013_liquidacion_valor_empresario'
]

with open('schema_completo.sql', 'w', encoding='utf-8') as f:
    f.write('-- Schema completo para ChancePro - Base de datos Supabase\n')
    f.write('-- Generado automáticamente desde Django migrations\n\n')
    
    for migracion in migraciones:
        print(f"Generando SQL para migración {migracion}...")
        result = subprocess.run(
            ['python', 'manage.py', 'sqlmigrate', 'core', migracion],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            f.write(f"-- Migración: {migracion}\n")
            f.write(result.stdout)
            f.write("\n")
        else:
            print(f"Error en migración {migracion}: {result.stderr}")

print("Schema completo generado en schema_completo.sql")
