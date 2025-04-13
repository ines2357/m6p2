import csv
import collections


def somar_pontuacoes_por_transportadora_origem():
    """
    Lê o arquivo 'transportadoras.csv' e calcula a soma
    das pontuações por transportadora e origem do percurso.
    Também armazena os scores individuais de cada transportadora.
    """

    pontuacoes_por_transportadora_origem = collections.defaultdict(int)
    scores_transportadoras = collections.defaultdict(list)

    # Ler o ficheiro CSV com delimitador ","
    with open('transportadoras.csv', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',')  # Define "," como delimitador
        next(reader)  # Ignorar cabeçalho

        for row in reader:
            origem_percurso = row[0]
            transportadora = row[1]
            chave = (transportadora, origem_percurso)

            try:
                # Converter os valores numéricos corretamente
                score_combustivel = int(row[3])  # Coluna 'score_combustivel'
                score_emissoes = int(row[4])     # Coluna 'score_emissoes'
                # Somar os scores relevantes
                pontuacao_total = score_combustivel + score_emissoes

                # Fazer a soma total
                pontuacoes_por_transportadora_origem[chave] += pontuacao_total

                # Adicionar os valores individuais à lista
                scores_transportadoras[chave].extend(
                    [score_combustivel, score_emissoes]
                )

            except ValueError:
                print(f"Erro ao converter valores na linha: {row}")

    return pontuacoes_por_transportadora_origem, scores_transportadoras
