import pytest
from app import app
from unittest.mock import patch


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_get_produtos(client):
    """Deve retornar a lista de produtos disponíveis"""
    response = client.get('/api/produtos')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list) or isinstance(data, dict)


def test_escolher_produto_sucesso(client):
    """Deve retornar impactos ambientais para um produto válido"""
    produto_nome = "Milho"  # <- esse precisa existir na sua base
    response = client.post('/api/escolher_produto', json={
        "produto_nome": produto_nome
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'produto' in data
    assert 'impactos_totais' in data
    assert 'menor_impacto' in data


def test_escolher_produto_falha_sem_nome(client):
    """Deve retornar erro se nenhum produto for enviado"""
    response = client.post('/api/escolher_produto', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


def test_escolher_produto_falha_inexistente(client):
    """Deve retornar erro se o produto não existir"""
    response = client.post('/api/escolher_produto', json={
        "produto_nome": "Produto Inexistente"
    })
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data


def test_resumo_impactos(client):
    """Deve retornar o resumo dos impactos ambientais"""
    response = client.get('/api/resumo_impactos')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    if data:
        exemplo = data[0]
        assert 'produto' in exemplo
        assert 'score_agua' in exemplo


def test_historico(client):
    """Deve retornar o histórico de escolhas (pode estar vazio)"""
    response = client.get('/api/historico')
    assert response.status_code == 200
    data = response.get_json()
    assert 'escolhas' in data


# Testes para forçar o erro 500 (simulação de falhas)

def test_erro_500_produtos(client):
    """Deve retornar erro 500 ao tentar obter lista de produtos"""
    """quando ocorre um erro"""
    with patch(
        "fornecedores.somar_pontuacoes_por_produto_localizacao",
        side_effect=Exception("Erro interno ao acessar fornecedores")
    ):
        response = client.get('/api/produtos')
    assert response.status_code == 500
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == "Erro ao obter lista de produtos."


def test_erro_500_escolher_produto(client):
    """Deve retornar erro 500 ao tentar calcular os impactos"""
    """ambientais e ocorre um erro"""
    with patch(
        "fornecedores.somar_pontuacoes_por_produto_localizacao",
        side_effect=Exception("Erro ao calcular impactos ambientais")
    ):
        response = client.post('/api/escolher_produto',
                               json={"produto_nome": "Produto A"})
    assert response.status_code == 500
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == "Erro ao calcular impactos ambientais."


def test_erro_500_resumo_impactos(client):
    """Deve retornar erro 500 ao tentar calcular o resumo dos"""
    """impactos ambientais e ocorre um erro"""
    with patch("fornecedores.somar_pontuacoes_por_produto_localizacao",
               side_effect=Exception("Erro ao calcular impactos ambientais")):
        response = client.get('/api/resumo_impactos')
    assert response.status_code == 500
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == "Erro ao calcular resumo dos impactos ambientais."


def test_erro_500_historico(client):
    """Deve retornar erro 500 ao tentar acessar o histórico"""
    """e ocorre um erro ao ler o arquivo"""
    with patch("builtins.open",
               side_effect=Exception("Erro ao acessar o histórico")):
        response = client.get('/api/historico')
    assert response.status_code == 500
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == "Erro ao acessar o histórico de escolhas."
