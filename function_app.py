import logging
import azure.functions as func
import os

app = func.FunctionApp()

import datetime
import logging
from lxml import html
import ssl
import requests, json
from string import Template

# Declara constantes del entorno
URL_TRM = 'https://www.superfinanciera.gov.co/CargaDriver/index.jsp'
URL_POST = os.environ.get("URL_POST")

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

@app.timer_trigger(schedule="0 0 8 * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def timer_trigger(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')
    principal()
    