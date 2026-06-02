from PIL import Image
import os

# Abrir la imagen original
img_path = 'static/icons/chanpro.jpeg'
img = Image.open(img_path)

# Convertir a RGBA si es necesario
if img.mode != 'RGBA':
    img = img.convert('RGBA')

# Tamaños requeridos
sizes = [72, 96, 128, 144, 152, 192, 384, 512]

# Generar iconos
for size in sizes:
    # Redimensionar
    resized = img.resize((size, size), Image.Resampling.LANCZOS)
    
    # Guardar
    output_path = f'static/icons/icon-{size}x{size}.png'
    resized.save(output_path, 'PNG')
    print(f'Generado: {output_path}')

print('¡Iconos generados exitosamente!')
