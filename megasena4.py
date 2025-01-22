import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import scipy.stats as stats  # Importar somente se usar scipy.stats
import megasena2


def analisar_variaveis_mega_sena(dados, colunas_numeros):
    """Analisa variáveis aleatórias discretas e contínuas na Mega Sena."""

    if dados is None: #Verifica se os dados foram lidos corretamente
        print("Erro ao processar os dados em megasena2.py. A análise de variáveis aleatórias será ignorada.")
        return

    print("\nVariáveis Aleatórias Discretas e Contínuas na Mega Sena:\n")

    print("Uma variável aleatória é uma variável cujo valor numérico é o resultado de um fenômeno aleatório.\n")

    print("1. Variáveis Aleatórias Discretas:\n")
    print("   Uma variável aleatória é discreta se seus valores possíveis formam um conjunto finito ou contável. Na Mega Sena, temos diversos exemplos:\n")
    print("   - O número sorteado em uma determinada dezena (ex: a 1ª dezena pode assumir valores de 1 a 60).")
    print("   - A quantidade de vezes que um número específico é sorteado ao longo de todos os concursos (a 'Frequência Obtida').")
    print("   - O número de acertos em um concurso (Sena, Quina, Quadra ou nenhum acerto).\n")

    print("   As seguintes distribuições de probabilidade discretas são relevantes para a análise da Mega Sena:\n")
    print("   - Distribuição Uniforme Discreta: Modela o cenário ideal onde cada número tem a mesma probabilidade (1/60) de ser sorteado. A análise de frequência compara os resultados reais com esse modelo.")
    print("   - Distribuição Hipergeométrica: Usada para calcular as probabilidades de acerto (Sena, Quina, Quadra), considerando o sorteio sem reposição.")
    print("   - Distribuição Binomial: Usada para calcular a probabilidade de acertar pelo menos um número em um número fixo de jogos.\n\n")

    print("   (Veja exemplos detalhados dos dados aplicados à essas distribuições no output do código do programa 'megasena2.py') .\n")

    media_por_concurso = dados[colunas_numeros].mean(axis=1)    

    print("\n2. Variável Aleatória Contínua (derivada):\n")
    print("   A média dos números sorteados em cada concurso é um exemplo de variável aleatória contínua derivada dos dados discretos. Vamos analisar a distribuição dessas médias.\n")

    # Histograma
    plt.figure(figsize=(10, 6))
    sns.histplot(media_por_concurso, kde=True)
    plt.xlabel("Média dos números sorteados por concurso", fontsize=12)
    plt.ylabel("Frequência", fontsize=12)
    plt.title("Histograma da média dos números sorteados por concurso", fontsize=14, fontweight='bold')
    plt.savefig("histograma_medias.png")
    plt.close()

    # Aplicações nos dados da variável contínua (Média)
    media_geral = media_por_concurso.mean()
    desvio_padrao = media_por_concurso.std()
    minimo = media_por_concurso.min()
    maximo = media_por_concurso.max()

    print("   Analisando a variável 'Média dos números sorteados por concurso', observamos:")
    print(f"   - Média geral das médias: {media_geral:.2f}")
    print(f"   - Desvio padrão das médias: {desvio_padrao:.2f}")
    print(f"   - Valor mínimo da média: {minimo:.2f}")
    print(f"   - Valor máximo da média: {maximo:.2f}\n")

    print("   Essas estatísticas descrevem a distribuição da variável contínua derivada, fornecendo informações sobre sua tendência central (média) e dispersão (desvio padrão).")
    print("   O histograma permite visualizar a distribuição das médias, mostrando a frequência com que diferentes valores de média ocorrem nos concursos.\n")


if __name__ == "__main__":
    dados, colunas_numeros = megasena2.processar_dados_mega_sena() # Chama a função para obter os dados
    if dados is not None: #Verifica se os dados foram lidos corretamente
        analisar_variaveis_mega_sena(dados, colunas_numeros) # Passa os dados para a função
