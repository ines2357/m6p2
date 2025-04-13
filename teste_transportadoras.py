import csv
import collections


def somar_pontuacoes_por_produto_localizacao():
    # Dicionários para armazenar a soma total
    # das pontuações por produto e localização
    pontuacoes_por_produto_localizacao = collections.defaultdict(int)
    scores_fornecedores = collections.defaultdict(list)

    # Ler o ficheiro CSV
    with open('fornecedores.csv', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Ignorar cabeçalho

        for row in reader:
            localizacao = row[0]
            produto = row[1]
            chave = (produto, localizacao)
            pontuacoes = list(map(int, row[2:]))
            pontuacao_total = sum(pontuacoes)  # Somar todas as pontuações

            # Acumular a soma total das pontuações por produto e localização
            pontuacoes_por_produto_localizacao[chave] += pontuacao_total

            # Acumular as pontuações individuais dos fornecedores
            scores_fornecedores[chave].extend(pontuacoes)

    return pontuacoes_por_produto_localizacao, scores_fornecedores


# Testar a função
if __name__ == "__main__":
    (
        pontuacoes_por_produto_localizacao, scores_fornecedores
    ) = somar_pontuacoes_por_produto_localizacao()

    print("Soma das pontuações por produto e localização:")
    for chave, valor in pontuacoes_por_produto_localizacao.items():
        print(f"{chave}: {valor}")

    print("\nPontuações individuais dos fornecedores:")
    for chave, valores in scores_fornecedores.items():
        print(f"{chave}: {valores}")
