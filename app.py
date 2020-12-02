import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
import re
import time
import constantes


def get_html(url): # retorna a string que será analisada no construtor BeautifulSoup
    
    response = requests.get(url)
    
    if response.ok:
        
        return response.text
    else:
        print(f'code: {response.status_code} for {url}')
        

def get_UFs(html): # retorna a lista com todas as UFs, retiradas do site. 
    
    soup = BeautifulSoup(html, 'lxml')
    
    pattern = r'\w{2}'
    
    lista_com_UF_desformatada = soup.find_all('option', attrs={"value": re.compile(pattern)})[1:]
    
    lista_com_UFs = []
    
    for index in range(lista_com_UF_desformatada):
        
        UF = lista_com_UF_desformatada[index]['value']
        
        lista_com_UFs.append(UF)
        
    return lista_com_UFs  
        

def get_number_of_stores(html): #encontrando o numero de lojas no estado. Não foi usada em main()
    
    BSobj = BeautifulSoup(html, 'lxml')
    
    pattern = re.compile(r'\d+')
    
    tag = BSobj.find_all('p')[0].text #encontra a primeira tag <p>, que é a que contém o número de lojas.
    
    numero = re.findall(pattern, tag)
    
    return numero[0]


def get_store_establishment(local): #retorna o estabelecimento (shopping,loja...)
    
    estabelecimento = local.find_all('p')[0].text
        
    return estabelecimento


def get_store_address(local): # retorna o endereço (rua, avenida...) da loja.
    
    endereco = local.find_all('p')[1].text
        
    return endereco


def get_store_address_number(local): # retorna o numero do endereço da loja.
        
    number = local.find_all('p')[2].text
        
    return number

def write_json(data): # retorna um arquivo json

    with open('lojas_renner.json', 'w') as jsonfile:

        json.dump(data,jsonfile,indent = 2)

def main():
    response = get_html(constantes.url["lojas_renner_principal"])

    lista_com_UFs = get_UFs(response)

    lista_lojas = []

    for UF in lista_com_UFs:
        
        url_por_estado = f'{constantes.url["lojas_renner_por_uf"]}{UF}'
        
        r = get_html(url_por_estado)
        
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

if __name__ == "__main__":
    main()