# Iconos de la Aplicación PWA

Este directorio debe contener los iconos de la aplicación para que funcione como PWA.

## Tamaños de Iconos Requeridos

Necesitas crear iconos con los siguientes tamaños (en formato PNG):

- icon-72x72.png (72x72 píxeles)
- icon-96x96.png (96x96 píxeles)
- icon-128x128.png (128x128 píxeles)
- icon-144x144.png (144x144 píxeles)
- icon-152x152.png (152x152 píxeles)
- icon-192x192.png (192x192 píxeles)
- icon-384x384.png (384x384 píxeles)
- icon-512x512.png (512x512 píxeles)

## Recomendaciones

- Usa un logo simple y reconocible
- Fondo sólido (preferiblemente azul #0d6efd para coincidir con el tema)
- Asegúrate de que el icono sea legible en tamaños pequeños
- El icono debe representar claramente tu marca

## Cómo Crear los Iconos

Puedes usar herramientas online como:
- https://www.favicon-generator.org/
- https://realfavicongenerator.net/
- https://www.pwabuilder.com/imageGenerator

Sube tu logo base y estas herramientas generarán todos los tamaños necesarios automáticamente.

## Después de Agregar los Iconos

1. Ejecuta `python manage.py collectstatic` para copiar los iconos a la carpeta de archivos estáticos
2. Reinicia el servidor Django
3. Abre la aplicación en un navegador móvil
4. Verás la opción de "Agregar a pantalla de inicio" o "Instalar app"
