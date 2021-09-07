# Importando Bibliotecas
import requests
import pandas as pd
import json

'''
Funções á ser realizadas:

- [X] funções Consumo APIs
- [X] Funções separando primeiros Conteúdos
- [X] Função Limpa Dados
- [X] Função olhar elementos individualmente
- [ ] Estudos SQLite3
- [ ] Desenhar Banco de dados Biblioteca
- [ ] Criar Banco
- [ ] Conectar & Testar Banco
- [ ] Função Enviar Biblioteca
- [ ] Função Excluir livro Blibioteca
- [ ] Função Editar livro Biblioteca
- [ ] Pesquisar Templates Html
- [ ] Estudar Api Google & seus filtros*
- [ ] Opções para organizar biblioteca internamente (Genero, nome, status)


Extras:

- [ ] Mostrar semelhantes ao adicionar livro biblioteca
- [ ] API amazon book


link api : https://www.googleapis.com/books/v1/volumes?q={valor_procurado}
'''

def consumir_api(url, busca):
    url = str(url)
    busca = str(busca)
    resposta = requests.get(url+busca).json()
    return resposta


def head(resposta, qtd_resposta=5):
    limpo = resposta['items'][:qtd_resposta]
    return limpo

def limpa_requisicao_livro(livro): # good
    dict_livro = {
        'titulo' : livro['title'],
        'autores' : '; '.join(livro['authors']),
        'descricao' : livro['description'],
        'num_paginas' : livro['pageCount'],
        'faixa_etaria' : livro['maturityRating'],
        'idioma' : livro['language'],
        'link' : livro['infoLink'],
    }

    ## Tratando iSBN

    if 'industryIdentifiers' in livro:
        for isbns in livro['industryIdentifiers']:
            if isbns['type'] == 'ISBN_13':
                dict_livro['isbn'] = {'tipo_isbn': isbns['type'], 'valor': isbns['identifier']}
            elif isbns['type'] == 'ISBN_10':
                dict_livro['isbn'] = {'tipo_isbn': isbns['type'], 'valor': isbns['identifier']}
            else:
                {'tipo_isbn':None}
    else:
        {'tipo_isbn':None}

    ## Tratando iSBN ↑


    ## Tratando Thumb

    if 'imageLinks' in livro:
        if 'smallThumbnail' in livro['imageLinks']:
            dict_livro['imagem'] = livro['imageLinks']['smallThumbnail']
        else:
            dict_livro['imagem'] = 'https://raw.githubusercontent.com/kilerhg/TodoBook/main/imagens/livro_sem_capa.png'
    else:
        dict_livro['imagem'] = 'https://raw.githubusercontent.com/kilerhg/TodoBook/main/imagens/livro_sem_capa.png'

    ## Tratando Thumb ↑

    return dict_livro

# ' MAIN '

# url = 'https://www.googleapis.com/books/v1/volumes?q='
# busca = 'mentes'

# dados = ConsumirAPI(url,busca)
# # a = [str(dados)[55:-1]]
# print(Head(dados))
# # 55


def mostrar_por_indice(dicionario, indice=0, mostrar=False):  
    """
    → Função que recebe um dicionario e um indice e mostra apenas um elemento do livro
    :param dicionario: Recebe um dicionário com os dados limpos do livro
    :param indice: Parametro opcional, recebe um valor de 0 a 6
    :param show: Paramêtro opcional, Recebe True or False
    :return: Retorna o valor do indice escolhido
    """
    if not mostrar:
        if indice == 0:
            return dicionario['titulo']
        elif indice == 1:
            return dicionario['autores']
        elif indice == 2:
            return dicionario['descricao']
        elif indice == 3:
            return dicionario['num_paginas']
        elif indice == 4:
            return dicionario['faixa_etaria']
        elif indice == 5:
            return dicionario['idioma']
        elif indice == 6:
            return dicionario['link']
        else:
            return 'Índice inválido'
            
    elif mostrar:
        if indice == 0:
            return 'Título: ' + dicionario['titulo']
        elif indice == 1:
            return 'Autor: ' + dicionario['autores']
        elif indice == 2:
            return 'Descrição: ' + dicionario['descricao']
        elif indice == 3:
            return 'Número de páginas: ' + dicionario['num_paginas']
        elif indice == 4:
            return 'Faixa Etária: ' + dicionario['faixa_etaria']
        elif indice == 5:
            return 'Idioma: ' + dicionario['idioma']
        elif indice == 6:
            return 'Link: ' + dicionario['link']
        else:
            return 'Índice inválido'

