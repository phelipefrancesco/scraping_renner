import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
import re
import time

def get_html(url):
    
    response = requests.get(url)
    
    if response.ok:
        
        return response.text
    else:
        print(f'code: {response.status_code} for {url}')
        

def get_UFs(html):
    
    soup = BeautifulSoup(html, 'lxml')
    
    pattern = r'\w{2}'
    
    lista_com_UF_desformatada = soup.find_all('option', attrs={"value": re.compile(pattern)})[1:]
    
    lista_com_UFs = []
    
    for index, UF_estado in enumerate(lista_com_UF_desformatada):
        
        UF = lista_com_UF_desformatada[index]['value']
        
        lista_com_UFs.append(UF)
        
    return lista_com_UFs 
        

def get_number_of_stores(html): #encontrando o numero de lojas no estado.
    
    BSobj = BeautifulSoup(html, 'lxml')
    
    pattern = re.compile(r'\d+')
    
    tag = BSobj.find_all('p')[0].text #encontra a primeira tag <p>, que é a que contém o número de lojas.
    
    numero = re.findall(pattern, tag)
    
    return numero[0]


def get_store_establishment(local):
    
    estabelecimento = local.find_all('p')[0].text
        
    return estabelecimento


def get_store_address(local):
    
    endereco = local.find_all('p')[1].text
        
    return endereco


def get_store_address_number(local):
        
    number = local.find_all('p')[2].text
        
    return number

def write_json(data):

    with open('lojas_renner.json', 'w') as jsonfile:

        json.dump(data,jsonfile,indent = 2)
   
url = 'https://www.lojasrenner.com.br/nossas-lojas'

response = get_html(url)

lista_com_UFs = get_UFs(response)

lista_lojas = []

for UF in lista_com_UFs:
    
    url2 = f'https://www.lojasrenner.com.br/store/renner/br/cartridges/OurStores/fragments/ourStoresList.jsp?state={UF}'
    
    time.sleep(0.1)
    r = get_html(url2)
    
    soup_object = BeautifulSoup(r, 'lxml')

    locais = soup_object.find_all('div', class_ = 'seacrh_result')
    
    for local in locais:

        loja = {
            'UF':UF,
            'estabelecimento': get_store_establishment(local), 
            'endereco': get_store_address(local), 
            'numero': get_store_address_number(local)
        }

        lista_lojas.append(loja)

write_json(lista_lojas)

    #print(json.dumps(lista_lojas, indent=2))

        # total_lojas = get_number_of_stores(r)
        # estabelecimento_loja = get_store_establishment(r)
        # endereco_loja = get_store_address(r)
        # numero_loja = get_store_address_number(r)

        # print(UF)
        # print(total_lojas)
        # print(estabelecimento_loja)
        # print(endereco_loja)
        # print(numero_loja)
