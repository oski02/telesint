# Teleint buscador creado para aquellos que se dedican a la recopilación de Información para la Obtención de Inteligencia


## Descripción
Este script de Python utiliza la biblioteca Telethon para interactuar con la API de Telegram. Permite al usuario unirse a canales y buscar mensajes específicos dentro de esos canales. Además, traduce los mensajes encontrados al español y guarda los resultados en archivos con marcas de tiempo.

## Características
- **Unión a canales**: El script intenta unirse a una lista de canales proporcionada por el usuario.
- **Búsqueda de mensajes**: Busca una cadena de texto específica dentro de los mensajes de los canales.
- **Traducción de mensajes**: Utiliza Google Translate para traducir los mensajes encontrados al español.
- **Registro con colores**: Muestra mensajes de éxito en **verde** y mensajes de error en **rojo**.
- **Guardado de resultados**: Guarda los mensajes encontrados en archivos dentro de la carpeta 'out', añadiendo la fecha y hora al nombre del archivo.

## Uso
1. **Configuración**: Edita el archivo `config.json` para incluir tu `api_id`, `api_hash` y `session_name`.
2. **Ejecución**: Corre el script en tu terminal o línea de comandos.
3. **Búsqueda**: Introduce el texto que deseas buscar cuando se te solicite.

## Código de Colores
El script utiliza códigos de escape ANSI para mostrar los mensajes de registro con colores en la terminal. Estos son los códigos utilizados:
- **Verde**: `\033[92m`
- **Rojo**: `\033[91m`
- **Naranja**: `\033[38;5;208m`

## Contribuciones
Las contribuciones son bienvenidas. Si tienes alguna sugerencia o mejora, no dudes en crear un 'pull request' o abrir un 'issue'.

## Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.

