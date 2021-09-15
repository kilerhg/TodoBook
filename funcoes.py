# Importando Bibliotecas
import requests
import pandas as pd
import json

'''
Funções á ser realizadas:

- [X] funções Consumo APIs
- [X] Funções separando primeiros Conteúdos
- [X] Função Limpa Dados
- [ ] Função olhar elementos individualmente
- [ ] Estudos SQLite3
- [ ] Desenhar Banco de dados Biblioteca
- [ ] Criar Banco
- [ ] Conectar & Testar Banco
- [ ] Função Enviar Biblioteca
- [ ] Função Excluir livro Blibioteca
- [ ] Função Editar livro Biblioteca
- [ ] Pesquisar Templates Html
- [ ] Estudar Api Google & seus filtros
- [ ] Opções para organizar biblioteca internamente (Genero, nome, status)


Extras:

- [ ] Mostrar semelhantes ao adicionar livro biblioteca
- [ ] API amazon book


link api : https://www.googleapis.com/books/v1/volumes?q={valor_procurado}
'''

def consumir_api(url, busca=''):
    url = str(url)
    busca = str(busca)
    resposta = requests.get(url+busca).json()
    return resposta


def head(resposta, qtd_resposta=10):
    limpo = resposta['items'][:qtd_resposta]
    return limpo

def limpa_requisicao_livro(livro, book_id): # good
    dict_livro = {
        'titulo' : livro['title'],
        'autores' : '; '.join(livro['authors']),
        'descricao' : livro['description'],
        'num_paginas' : livro['pageCount'],
        'faixa_etaria' : livro['maturityRating'],
        'idioma' : livro['language'],
        'link' : livro['infoLink'],
        'book_id' : book_id
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

def search_book(busca: str):
    ' MAIN '
    url = 'https://www.googleapis.com/books/v1/volumes?q='

    dados = consumir_api(url,busca)
    dados_limpo = head(dados)

    lista_livros = []
    for livro_sujo in dados_limpo:
        book_id = livro_sujo['id']
        livro_limpo = livro_sujo['volumeInfo']
        try:
            livro_tratado = limpa_requisicao_livro(livro=livro_limpo, book_id=book_id)
        except:
            livro_tratado = None
        if livro_tratado:
            lista_livros.append(livro_tratado)
    return lista_livros

def get_books_by_id(list_books_id : list):
    base_url = 'https://www.googleapis.com/books/v1/volumes/'
    list_book_library = []
    for book in list_books_id:
        link_book = base_url+book
        dados = consumir_api(link_book)
        dados_limpos = limpa_requisicao_livro(livro=dados['volumeInfo'], book_id=dados['id'])
        # dados_limpos['']
        list_book_library.append(dados_limpos)
    return list_book_library