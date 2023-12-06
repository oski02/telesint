import json
import os
import argparse
import sys
import asyncio
import re
from colorama import init, Fore, Style
from datetime import datetime
from bs4 import BeautifulSoup
from telethon import TelegramClient, errors
from telethon.tl.functions.channels import JoinChannelRequest
from tqdm import tqdm
from googletrans import Translator

# Inicializa colorama
init(autoreset=True)
# Banner en ASCII para Telesint
print(Fore.CYAN + '''
████████╗███████╗██╗     ███████╗███████╗██╗███╗   ██╗████████╗
╚══██╔══╝██╔════╝██║     ██╔════╝██╔════╝██║████╗  ██║╚══██╔══╝
   ██║   █████╗  ██║     █████╗  ███████╗██║██╔██╗ ██║   ██║   
   ██║   ██╔══╝  ██║     ██╔══╝  ╚════██║██║██║╚██╗██║   ██║   
   ██║   ███████╗███████╗███████╗███████║██║██║ ╚████║   ██║   
   ╚═╝   ╚══════╝╚══════╝╚══════╝╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝   
''' + Style.RESET_ALL + Fore.YELLOW + 'By: Oscar Atienza aka @oski02|@x25s\n\n\n' + Style.RESET_ALL)


async def cargar_configuracion():
    with open('config.json') as f:
        return json.load(f)

async def crear_cliente(config):
    client = TelegramClient(config['session_name'], config['api_id'], config['api_hash'])
    await client.start()
    return client

async def verificar_canales(client, canales):
    for canal in canales:
        try:
            entity = await client.get_entity(canal)
            print(Fore.WHITE + f'[*] Canales:\n' +Style.RESET_ALL)
            print(Fore.YELLOW + f'[A] ' + Style.RESET_ALL + Fore.GREEN + f'Acceso exitoso al canal "{canal}"' + Style.RESET_ALL)
        except (ValueError, errors.FloodWaitError) as e:
            print(Fore.RED + f'Error en el canal "{canal}": {e}' + Style.RESET_ALL)
            continue
        try:
            await client(JoinChannelRequest(canal))
            print(Fore.YELLOW + f'[U] ' + Style.RESET_ALL + Fore.GREEN + f'Se unió al canal "{canal}"' + Style.RESET_ALL)
            print("")
        except (errors.FloodWaitError, Exception) as e:
            print(Fore.RED + f'[-] Error al unirse al canal "{canal}": {e}' + Style.RESET_ALL)
            continue

async def buscar_en_canales(client, canales, busqueda, formato_salida):
    if not os.path.exists('out'):
        os.makedirs('out')

    translator = Translator()

    for canal in tqdm(canales, desc='[*] Buscando en canales', colour='blue'):
        resultados = []  # Mover la inicialización de resultados aquí
        try:
            entity = await client.get_entity(canal)
        except (ValueError, errors.FloodWaitError) as e:
            print(Fore.RED + f'Error en el canal "{canal}": {e}' + Style.RESET_ALL)
            continue
        print("")

        async for message in client.iter_messages(entity):
            if message.text and busqueda in message.text:
                translated = translator.translate(message.text, dest='es')
                resultados.append({'canal': canal, 'mensaje': translated.text})

        # Verifica si hay resultados antes de llamar a las funciones de exportación
        if resultados:  # Si hay resultados en la lista
            if 'json' in formato_salida:
                exportar_json(resultados, busqueda, canal)
            if 'txt' in formato_salida:
                exportar_txt(resultados, busqueda, canal)
            if 'html' in formato_salida:
                exportar_html(resultados, busqueda, canal)
        else:
            print(Fore.YELLOW + f"No se encontraron resultados para la búsqueda '{busqueda}' en el canal '{canal}'" + Style.RESET_ALL)

def exportar_json(resultados, busqueda, canal):
    fecha_hora = datetime.now().strftime('%Y%m%d_%H%M%S')
    nombre_archivo = f'resultados_{busqueda}_{canal}_{fecha_hora}.json'
    with open(os.path.join('out', nombre_archivo), 'w', encoding='utf-8') as f:
        json.dump(resultados, f, ensure_ascii=False, indent=4)
    print(Fore.YELLOW + 'Los resultados se han guardado de forma exitosa en formato JSON en la carpeta ' + Style.RESET_ALL + Fore.BLUE + 'out' + Style.RESET_ALL)

def exportar_txt(resultados, busqueda, canal):
    fecha_hora = datetime.now().strftime('%Y%m%d_%H%M%S')
    nombre_archivo = f'resultados_{busqueda}_{canal}_{fecha_hora}.txt'
    with open(os.path.join('out', nombre_archivo), 'w', encoding='utf-8') as f:
        for resultado in resultados:
            f.write(f'Encontrado en {resultado["canal"]}: {resultado["mensaje"]}\n')
    guardar_urls_en_archivo(extraer_urls_archivos_txt())
    print(Fore.YELLOW + 'Los resultados se han guardado de forma exitosa en formato texto en la carpeta ' + Style.RESET_ALL + Fore.BLUE + 'out' + Style.RESET_ALL)

def exportar_html(resultados, busqueda, canal):
    fecha_hora = datetime.now().strftime('%Y%m%d_%H%M%S')
    nombre_archivo = f'resultados_{busqueda}_{canal}_{fecha_hora}.html'
    html = BeautifulSoup('', 'html.parser')
    for resultado in resultados:
        p = html.new_tag('p')
        p.string = f'Encontrado en {resultado["canal"]}: {resultado["mensaje"]}'
        html.append(p)
    with open(os.path.join('out', nombre_archivo), 'w', encoding='utf-8') as f:
        f.write(str(html))
    print(Fore.YELLOW + 'Los resultados se han guardado de forma exitosa en formato HTML en la carpeta ' + Style.RESET_ALL + Fore.BLUE + 'out' + Style.RESET_ALL)

def extraer_urls_archivos_txt():
    urls_unicas = set()
    # Expresión regular para buscar URLs dentro del texto
    url_pattern = r'https?://[^\s)]+'
    # Recorre los archivos .txt en el directorio 'out'
    for file_name in os.listdir('out'):
        if file_name.endswith(".txt"):
            with open(os.path.join('out', file_name), 'r', encoding='utf-8') as file:
                lines = file.readlines()
                for line in lines:
                    # Encuentra todas las URLs en la línea usando la expresión regular
                    urls = re.findall(url_pattern, line)
                    urls_unicas.update(urls)
    return urls_unicas

def guardar_urls_en_archivo(urls):
    with open(os.path.join('out', 'urls.txt'), 'a', encoding='utf-8') as urls_file:
        for url in urls:
            urls_file.write(url + '\n')

async def main():
    parser = argparse.ArgumentParser(
           description='Telesint - Herramienta de búsqueda de Inteligencia en canales de Telegram',
           epilog='''Ejemplos de uso:
           python3 telesint.py -b busqueda
           python3 telesint.py -b busqueda -f html
           python3 telesint.py -b busqueda -f html,json
           python3 telesint.py -l (Lista todos los canales del fichero config.json)
           python3 telesint.py -c canal1 canal2 -b busqueda
           ''',
           formatter_class=argparse.RawDescriptionHelpFormatter
          )
    parser.add_argument('-c', '--canales', nargs='*', help='Lista de canales para buscar')
    parser.add_argument('-b', '--busqueda', required=False, help='Texto de búsqueda')
    parser.add_argument('-f', '--formato', default='json,txt,html', help='Formato de salida (json, txt, html)')
    parser.add_argument('-l', '--listar', action='store_true', help='Lista los canales del archivo config.json')
    # Si no se pasaron argumentos, muestra la ayuda y termina
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    args = parser.parse_args()
    # Comprueba si se proporcionaron argumentos
    if not any(vars(args).values()):
        parser.print_help()
        sys.exit(0)
    # Carga la configuración
    config = await cargar_configuracion()
    # Si se pasó la opción -l, lista los canales y termina
    if args.listar:
        print('Canales en config.json:')
        for canal in config['canales']:
            print(canal)
        sys.exit(0)
    # Crea el cliente de Telegram
    client = await crear_cliente(config)
    # Si no se especificaron canales, usa todos los canales de la configuración
    if args.canales is None:
        args.canales = config['canales']
    # Verifica los canales
    await verificar_canales(client, args.canales)
    # Busca en los canales utilizando el texto proporcionado como búsqueda
    await buscar_en_canales(client, args.canales, args.busqueda, args.formato.split(','))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
