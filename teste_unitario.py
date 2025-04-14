import unittest
from unittest.mock import patch, mock_open
from fornecedores import somar_pontuacoes_por_produto_localizacao
from transportadoras import somar_pontuacoes_por_transportadora_origem


class TestSomarPontuacoes(unittest.TestCase):

    @patch(
        'builtins.open',
        new_callable=mock_open,
        read_data=(
            'localizacao,produto,score_agua,score_eletricidade,'
            'score_combustiveis,score_desperdicio,score_contaminacao,'
            'score_emissoes\n'
            'Torres Vedras,Arroz,5,1,5,5,4,5\n'
            'Torres Vedras,Trigo,2,3,2,2,3,3\n'
            'Alcácer do Sal,Trigo,3,3,4,3,4,3\n'
            'Alcácer do Sal,Milho,4,2,1,1,1,1\n'
            'Alcácer do Sal,Cevada,1,3,2,2,2,1\n'
            'Campo Maior,Arroz,4,5,5,5,5,5\n'
            'Campo Maior,Milho,4,1,1,1,1,1\n'
            'Campo Maior,Cevada,2,3,2,2,3,1\n'
        )
    )
    def test_somar_pontuacoes_por_produto_localizacao(self, mock_file):
            (
                pontuacoes_por_produto_localizacao,
                scores_fornecedores, produtos
            ) = somar_pontuacoes_por_produto_localizacao()

            # Verificar se as somas das pontuações estão corretas dinamicamente
            for chave in pontuacoes_por_produto_localizacao:
                soma_esperada = sum(scores_fornecedores[chave])
                self.assertEqual(
                    pontuacoes_por_produto_localizacao[chave],
                    soma_esperada,
                    msg=f"Soma incorreta para {chave}"
                )

            # Verificar se o ficheiro foi aberto corretamente
            mock_file.assert_called_once_with(
                 'fornecedores.csv', newline='', encoding='utf-8'
            )


class TestSomarPontuacoesTransportadoras(unittest.TestCase):

    @patch(
        'builtins.open',
        new_callable=mock_open,
        read_data=(
            'origem_percurso,transportadora,distancia_percorrida_km,'
            'score_combustivel,score_emissoes\n'
            'Torres Vedras,A,53,1,1\n'
            'Campo Maior,B,229,5,5\n'
            'Alcácer do Sal,C,96,2,2\n'
        )
    )
    def test_somar_pontuacoes_por_transportadora_origem(self, mock_file):
        (
            pontuacoes_por_transportadora_origem,
            scores_transportadoras
        ) = somar_pontuacoes_por_transportadora_origem()

        # Verificar se as somas das pontuações estão corretas dinamicamente
        for chave in pontuacoes_por_transportadora_origem:
            soma_esperada = sum(scores_transportadoras[chave])
            self.assertEqual(
                pontuacoes_por_transportadora_origem[chave],
                soma_esperada,
                msg=f"Soma incorreta para {chave}"
            )

        # Verificar se o ficheiro foi aberto corretamente
        mock_file.assert_called_once_with(
            'transportadoras.csv', newline='', encoding='utf-8'
        )


if __name__ == '__main__':
    unittest.main()
