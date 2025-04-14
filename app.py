from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from collections import OrderedDict
import fornecedores
import consumidor
import transportadoras
import os


app = Flask(__name__)
# Permite CORS para todas as rotas, você pode ajustar se necessário
CORS(app, resources={r"/*": {"origins": "*"}})
port = int(os.environ.get("PORT", 5000))


@app.route('/api/produtos', methods=['GET'])
def get_produtos():
    try:
        (
            _, _, produtos
        ) = fornecedores.somar_pontuacoes_por_produto_localizacao()

        return jsonify(produtos)
    except Exception:
        return jsonify({"error": "Erro ao obter lista de produtos."}), 500

# Rota GET para a página inicial


@app.route('/')
def index():
    # Obtendo a lista de produtos disponíveis
    (
        _, _, produtos_disponiveis
    ) = fornecedores.somar_pontuacoes_por_produto_localizacao()
    return render_template('index.html', produtos=produtos_disponiveis)


# Rota POST para processar o produto escolhido
# e retornar os impactos ambientais (API)
@app.route('/api/escolher_produto', methods=['POST'])
def api_escolher_produto():
    try:
        data = request.get_json()
        produto_nome = data.get('produto_nome')

        if not produto_nome:
            return jsonify({"error": "Nome do produto não fornecido"}), 400

        try:
            produto_nome = consumidor.escolher_produto(produto_nome)
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

        # Continua com os cálculos como antes...
        (
            pontuacoes_por_produto_localizacao, scores_fornecedores, produtos
        ) = fornecedores.somar_pontuacoes_por_produto_localizacao()
        (
            pontuacoes_por_transportadora_origem, scores_transportadoras
        ) = transportadoras.somar_pontuacoes_por_transportadora_origem()

        impactos_fornecedores = [
            (localizacao, pontuacao)
            for ((produto, localizacao), pontuacao)
            in pontuacoes_por_produto_localizacao.items()
            if produto == produto_nome
        ]

        impactos_transportadoras = [
            (origem_percurso, pontuacao)
            for ((transportadora, origem_percurso), pontuacao)
            in pontuacoes_por_transportadora_origem.items()
        ]

        impactos_totais = []
        for (localizacao, impacto_fornecedor) in impactos_fornecedores:
            impacto_transporte = next(
                (impacto for (origem_percurso, impacto)
                 in impactos_transportadoras
                 if origem_percurso == localizacao),
                0
            )
            impacto_total = impacto_fornecedor + impacto_transporte
            impactos_totais.append({
                "localizacao": localizacao,
                "impacto_total": impacto_total
            })

        menor_impacto = min(impactos_totais, key=lambda x: x["impacto_total"])
        localizacao_menor_impacto = menor_impacto["localizacao"]
        impacto_total = menor_impacto["impacto_total"]

        resposta = OrderedDict([
            ('produto', produto_nome),
            ('impactos_totais', impactos_totais),
            ('menor_impacto', {
                'localizacao': localizacao_menor_impacto,
                'impacto_total': impacto_total
            })
        ])

        return jsonify(resposta)

    except Exception as e:
        print(f"[ERRO INTERNO] {e}")  # Log no terminal para facilitar debug
        return jsonify({"error": "Erro ao calcular impactos ambientais."}), 500


# Rota POST para processar o produto escolhido
# e renderizar a página de resultados (HTML)
@app.route('/escolher_produto', methods=['POST'])
def render_escolher_produto():
    # Produto escolhido pelo usuário
    produto_nome = request.form['produto_nome']
    # Supondo que você tem uma função para processar a escolha
    produto_nome = consumidor.escolher_produto(produto_nome)

    # Calcula os impactos ambientais
    (
        pontuacoes_por_produto_localizacao, scores_fornecedores, produtos
    ) = fornecedores.somar_pontuacoes_por_produto_localizacao()
    (
        pontuacoes_por_transportadora_origem, scores_transportadoras
    ) = transportadoras.somar_pontuacoes_por_transportadora_origem()

    # Calculando os impactos ambientais por fornecedor
    impactos_fornecedores = [
        (localizacao, pontuacao)
        for (produto, localizacao), pontuacao
        in pontuacoes_por_produto_localizacao.items()
        if produto == produto_nome
    ]

    impactos_transportadoras = [
        (origem_percurso, pontuacao)
        for (transportadora, origem_percurso), pontuacao
        in pontuacoes_por_transportadora_origem.items()
    ]

    impactos_totais = []
    for (localizacao, impacto_fornecedor) in impactos_fornecedores:
        impacto_transporte = next(
            (impacto for (origem_percurso, impacto)
             in impactos_transportadoras if origem_percurso == localizacao),
            0
        )
        impacto_total = impacto_fornecedor + impacto_transporte
        impactos_totais.append((localizacao, impacto_total))

    # Encontrar o local com menor impacto
    menor_impacto = min(impactos_totais, key=lambda x: x[1])
    localizacao_menor_impacto, impacto_total = menor_impacto

    # Renderizar a página de resultado com os dados
    return render_template(
        'resultado.html',
        produto=produto_nome,
        impactos=impactos_totais,
        menor_impacto=(
            localizacao_menor_impacto,
            impacto_total
        )
    )


@app.route('/api/resumo_impactos', methods=['GET'])
def api_resumo_impactos():
    try:
        (
            pontuacoes_por_produto_localizacao, scores_fornecedores, produtos
        ) = fornecedores.somar_pontuacoes_por_produto_localizacao()
        (
            pontuacoes_por_transportadora_origem, scores_transportadoras
        ) = transportadoras.somar_pontuacoes_por_transportadora_origem()

        dados_resumo = []

        # Definir a ordem específica conforme o seu exemplo
        for (produto, localizacao), pontuacao in scores_fornecedores.items():
            score_agua = pontuacao[0] if len(pontuacao) > 0 else 0
            score_eletricidade = pontuacao[1] if len(pontuacao) > 1 else 0
            score_combustiveis = pontuacao[2] if len(pontuacao) > 2 else 0
            score_desperdicio = pontuacao[3] if len(pontuacao) > 3 else 0
            score_contaminacao = pontuacao[4] if len(pontuacao) > 4 else 0
            score_emissoes = pontuacao[5] if len(pontuacao) > 5 else 0

            transportadora_data = next(
                (data for (transportadora, origem),
                 data in scores_transportadoras.items()
                 if origem == localizacao),
                None
            )

            if transportadora_data:
                score_combustivel = transportadora_data[0] if len(
                    transportadora_data) > 0 else 0
                score_emissoes_transporte = transportadora_data[1] if len(
                    transportadora_data) > 1 else 0
            else:
                score_combustivel = 0
                score_emissoes_transporte = 0

            # Adicionar os dados no OrderedDict com a ordem correta
            dados_resumo.append(OrderedDict([
                ('produto', produto),
                ('localizacao', localizacao),
                ('score_agua', score_agua),
                ('score_eletricidade', score_eletricidade),
                ('score_combustiveis_fornecedor', score_combustiveis),
                ('score_desperdicio', score_desperdicio),
                ('score_contaminacao', score_contaminacao),
                ('score_emissoes', score_emissoes),
                ('score_combustiveis_transportadora', score_combustivel),
                ('score_emissoes_transportadora', score_emissoes_transporte)
            ]))

        # Retornar os dados com a ordem garantida
        return jsonify(dados_resumo)
    except Exception:
        return jsonify(
            {"error": "Erro ao calcular resumo dos impactos ambientais."}
        ), 500


@app.route('/resumo_impactos')
def resumo_impactos():
    (
        pontuacoes_por_produto_localizacao, scores_fornecedores, produtos
    ) = fornecedores.somar_pontuacoes_por_produto_localizacao()
    (
        pontuacoes_por_transportadora_origem, scores_transportadoras
    ) = transportadoras.somar_pontuacoes_por_transportadora_origem()

    dados_resumo = []

    for (produto, localizacao), pontuacao in scores_fornecedores.items():

        score_agua = pontuacao[0] if len(pontuacao) > 0 else 0
        score_eletricidade = pontuacao[1] if len(pontuacao) > 1 else 0
        score_combustiveis = pontuacao[2] if len(pontuacao) > 2 else 0
        score_desperdicio = pontuacao[3] if len(pontuacao) > 3 else 0
        score_contaminacao = pontuacao[4] if len(pontuacao) > 4 else 0
        score_emissoes = pontuacao[5] if len(pontuacao) > 5 else 0

        transportadora_data = next(
            (data for (transportadora, origem),
             data in scores_transportadoras.items() if origem == localizacao),
            None
        )

        if transportadora_data:

            score_combustivel = transportadora_data[0] if len(
                transportadora_data) > 0 else 0
            score_emissoes_transporte = transportadora_data[1] if len(
                transportadora_data) > 1 else 0
        else:
            score_combustivel = 0
            score_emissoes_transporte = 0

        dados_resumo.append({
            'produto': produto,
            'localizacao': localizacao,
            'score_agua': score_agua,
            'score_eletricidade': score_eletricidade,
            'score_combustiveis_fornecedor': score_combustiveis,
            'score_desperdicio': score_desperdicio,
            'score_contaminacao': score_contaminacao,
            'score_emissoes': score_emissoes,
            'score_combustiveis_transportadora': score_combustivel,
            'score_emissoes_transportadora': score_emissoes_transporte
        })

    return render_template('resumo_impactos.html', dados_resumo=dados_resumo)


@app.route('/api/historico', methods=['GET'])
def api_historico():
    try:
        caminho_arquivo = './historico_de_escolhas.txt'
        with open(caminho_arquivo, "r") as arquivo:
            escolhas = arquivo.readlines()
        return jsonify({'escolhas': escolhas})
    except FileNotFoundError:
        return jsonify({'escolhas': []}), 200
    except Exception:
        return jsonify(
            {"error": "Erro ao acessar o histórico de escolhas."}
        ), 500


@app.route('/historico')
def historico():

    caminho_arquivo = './historico_de_escolhas.txt'

    try:
        with open(caminho_arquivo, "r") as arquivo:
            escolhas = arquivo.readlines()
    except FileNotFoundError:
        escolhas = []

    return render_template('historico.html', escolhas=escolhas)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=port)
