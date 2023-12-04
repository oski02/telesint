# Teleint buscador creado para aquellos que se dedican a la recopilación de Información para la Obtención de Inteligencia


## Descripción
Este script de Python utiliza la biblioteca Telethon para interactuar con la API de Telegram. Permite al usuario unirse a canales y buscar mensajes específicos dentro de esos canales. Además, traduce los mensajes encontrados al español y guarda los resultados en archivos con marcas de tiempo.


<span>![</span><span>Aquí la descripción de la imagen por si no carga</span><span>]</span><span>(</span><span>https://raw.githubusercontent.com/oski02/teleint/main/img/logo.jpeg</span><span>)</span>


## Características
- **Unión a canales**: El script intenta unirse a una lista de canales proporcionada por el usuario.
- **Búsqueda de mensajes**: Busca una cadena de texto específica dentro de los mensajes de los canales.
- **Traducción de mensajes**: Utiliza Google Translate para traducir los mensajes encontrados al español.
- **Registro con colores**: Muestra mensajes de éxito en **verde** y mensajes de error en **rojo**.
- **Guardado de resultados**: Guarda los mensajes encontrados en archivos dentro de la carpeta 'out', añadiendo la fecha y hora al nombre del archivo.

## Uso
1. **Instalación**: Instala las dependencias con: `pip3 install requirements.txt`
2. **Configuración**: Edita el archivo `config.json` para incluir tu `api_id`, `api_hash` y `session_name`. Añade los canales `canales`
3. **Ejecución**: Corre el script en tu terminal o línea de comandos.
4. **Búsqueda**: Introduce el texto que deseas buscar cuando se te solicite.

## Instalación
El script utiliza códigos de escape ANSI para mostrar los mensajes de registro con colores en la terminal. Estos son los códigos utilizados:

## Ejemplos de uso:
            > python3 telesint.py -b busqueda
            > python3 telesint.py -b busqueda -f html
            > python3 telesint.py -b busqueda -f html,json
            > python3 telesint.py -l (Lista todos los canales del fichero config.json)
            > python3 telesint.py -c canal1 canal2 -b busqueda
            > grep -ri "spain" out/*
            > grep -ri "ukraine" out/*
      
## Contribuciones
Las contribuciones son bienvenidas. Si tienes alguna sugerencia o mejora, no dudes en crear un 'pull request' o abrir un 'issue'.

## Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.

