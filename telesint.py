import json
import os
import argparse
import sys
from colorama import init, Fore, Style
from datetime import datetime
from bs4 import BeautifulSoup
from telethon import TelegramClient, errors
from telethon.tl.functions.channels import JoinChannelRequest
from tqdm import tqdm
from googletrans import Translator
import asyncio


# Inicializa colorama
init(autoreset=True)
# Banner en ASCII para Telesint con el nombre del creador en color amarillo
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
            print(Fore.GREEN + f'Acceso exitoso al canal "{canal}"' + Style.RESET_ALL)
        except (ValueError, errors.FloodWaitError) as e:
            print(Fore.RED + f'Error en el canal "{canal}": {e}' + Style.RESET_ALL)
            continue
        try:
            await client(JoinChannelRequest(canal))
            print(Fore.GREEN + f'Se unió al canal "{canal}"' + Style.RESET_ALL)
        except (errors.FloodWaitError, Exception) as e:
            print(Fore.RED + f'Error al unirse al canal "{canal}": {e}' + Style.RESET_ALL)
            continue


async def buscar_en_canales(client, canales, busqueda, formato_salida):
    translator = Translator()
    if not os.path.exists('out'):
        os.makedirs('out')
    for canal in tqdm(canales, desc='Buscando en canales', colour='blue'):
        resultados = []  # Mover la inicialización de resultados aquí
        try:
            entity = await client.get_entity(canal)
        except (ValueError, errors.FloodWaitError) as e:
            print(Fore.RED + f'Error en el canal "{canal}": {e}' + Style.RESET_ALL)
            continue
        async for message in client.iter_messages(entity):
            if message.text and busqueda in message.text:
                translated = translator.translate(message.text, dest='es')
                resultados.append({'canal': canal, 'mensaje': translated.text})
        # Mover las llamadas a las funciones de exportación aquí
        if 'json' in formato_salida:
            exportar_json(resultados, busqueda, canal)
        if 'txt' in formato_salida:
            exportar_txt(resultados, busqueda, canal)
        if 'html' in formato_salida:
            exportar_html(resultados, busqueda, canal)



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

async def main():
    #parser = argparse.ArgumentParser(description='Telesint - Herramienta de búsqueda de Inteligencia en canales de Telegram')

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

    # Busca en los canales
    await buscar_en_canales(client, args.canales, args.busqueda, args.formato.split(','))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
