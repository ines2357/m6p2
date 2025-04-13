import datetime
import requests
import os

# Define a URL da API corretamente, priorizando a variável de ambiente
API_URL = os.getenv("API_URL", "http://localhost:5000/api/produtos")


def obter_produtos_disponiveis():
    try:
        # Fazendo a requisição GET à API que retorna a lista de produtos
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()  # Gera um erro para status 4xx e 5xx

        produtos = response.json()  # Obtemos os produtos no formato JSON
        return produtos
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Erro ao tentar conectar com a API: {str(e)}")


def registrar_escolha(produto_nome):
    with open("historico_de_escolhas.txt", "a") as arquivo:
        arquivo.write(f"{datetime.datetime.now()}: {produto_nome}\n")


def escolher_produto(produto_nome):
    # Obtendo os produtos disponíveis a partir da API
    produtos_disponiveis = obter_produtos_disponiveis()

    # Normalizando o nome do produto recebido
    produto_nome_normalizado = produto_nome.strip().title()

    # Verificando se o produto está na lista de produtos disponíveis
    if produto_nome_normalizado not in produtos_disponiveis:
        raise ValueError(f"Produto '{produto_nome}' não é válido.")

    # Registrar a escolha do produto
    registrar_escolha(produto_nome_normalizado)

    return produto_nome_normalizado
