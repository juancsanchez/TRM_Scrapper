import datetime
import logging
from lxml import html
import ssl
import requests, json
from string import Template

# Importar el URL_POST desde el archivo de configuración
from config import URL_POST

import azure.functions as func

# Declara constantes del entorno
URL_TRM = 'https://www.superfinanciera.gov.co/CargaDriver/index.jsp'

def get_trm(website):
    price = []
    page = requests.get(website, verify=False)
    tree = html.fromstring(page.content)
    price = tree.xpath('//tr[2]/td[3]/text()')
    #Cambiar de acuerdo a lo que se desea buscar dentro del HTML
    #(-)price = tree.xpath('//span[@class="big strong"]/text()') #Cambiar de acuerdo a lo que se desea buscar dentro del HTML
    trmString = ''.join(price) #Convierte la lista en string
    trmPreFloat = trmString.replace(',','') #Reemplazar la coma para poder convertir el string en float
    trm = float(trmPreFloat)
    return trm

def enviar_post(payload):
    url = URL_POST
    requests.post(url, json=payload) # Enviar POST a la URL designada con Header JSON

def principal():
    # Get price from function
    price = get_trm(URL_TRM)
    payload = {'TRM': price}
    enviar_post(payload)

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)

    principal()