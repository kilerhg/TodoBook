# Importando Bibliotecas
import requests
import pandas as pd
import json

'''
Funções á ser realizadas

- [ ] Criar funções Consumo APIs
- [ ] Criar Funções separando primeiros Conteúdos
- [ ] 



link api : https://www.googleapis.com/books/v1/volumes?q={valor_procurado}
'''

def ConsumirAPI(url,busca):
    url = str(url)
    busca = str(busca)
    resposta = requests.get(url+busca).json()

    return resposta

def Head(resposta,qtd_resposta=5):
    limpo = resposta['items'][:qtd_resposta]
    return limpo

# ' MAIN '

# url = 'https://www.googleapis.com/books/v1/volumes?q='
# busca = 'mentes'

# dados = ConsumirAPI(url,busca)
# # a = [str(dados)[55:-1]]
# print(Head(dados))
# # 55