import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import scipy.stats as stats
import megasena3
import megasena4


def processar_dados_mega_sena(nome_arquivo_csv='megasena_final.csv'):
    """Processa os dados da Mega Sena a partir do CSV."""
    dados_loteria_sem_na = None  # Inicializa dados_loteria_sem_na como None
    colunas_numeros = None #Inicializa colunas_numeros como None
    try:
        dados_loteria = pd.read_csv(nome_arquivo_csv, encoding='utf-8')
        if dados_loteria.empty:
            dados_loteria = pd.read_csv(nome_arquivo_csv, encoding='latin1', delimiter=';')
        if dados_loteria.empty:
            dados_loteria = pd.read_csv(nome_arquivo_csv, encoding='cp1252', delimiter='\t')
        if dados_loteria.empty:
            dados_loteria = pd.read_csv(nome_arquivo_csv, encoding='utf-8', header=None, names=['concurso','data','dezena_1','dezena_2','dezena_3','dezena_4','dezena_5','dezena_6','ganhadores_sena','cidade','rateio_sena','ganhadores_quina','rateio_quina','ganhadores_quadra','rateio_quadra','acumulado','arrecadacao','estimativa','acumulado_especial','observacao'])

        colunas_numeros = ['1ª Dezena', '2ª Dezena', '3ª Dezena', '4ª Dezena', '5ª Dezena', '6ª Dezena']

        # Converte para inteiro e remove linhas com NaN
        for coluna in colunas_numeros:
            dados_loteria[coluna] = pd.to_numeric(dados_loteria[coluna], errors='coerce').astype('Int64')
        dados_loteria_sem_na = dados_loteria.dropna(subset=colunas_numeros)

    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo_csv}' não encontrado.")
        return dados_loteria_sem_na, colunas_numeros #Retorna None, None
    except pd.errors.ParserError as e:
        print(f"Erro ao ler o arquivo CSV '{nome_arquivo_csv}': {e}")
        return dados_loteria_sem_na, colunas_numeros #Retorna None, None
    except Exception as e:
        print(f"Ocorreu um erro INESPERADO ao ler o arquivo CSV: {e}")
        return dados_loteria_sem_na, colunas_numeros #Retorna None, None

    return dados_loteria_sem_na, colunas_numeros #Retorno normal da função.


def analisar_mega_sena(nome_arquivo_csv):
    """Analisa os dados da Mega Sena e exibe as fórmulas e cálculos."""

    print("\n\nFonte de dados: https://github.com/programadriano/mongodb-megasena/blob/master/megasena.csv \n\n")
    
    nome_arquivo_csv = 'megasena_final.csv'
    try:
        dados_loteria = pd.read_csv(nome_arquivo_csv, encoding='utf-8')
        if dados_loteria.empty:
            dados_loteria = pd.read_csv(nome_arquivo_csv, encoding='latin1', delimiter=';')
        if dados_loteria.empty:
            dados_loteria = pd.read_csv(nome_arquivo_csv, encoding='cp1252', delimiter='\t')
        if dados_loteria.empty:
            dados_loteria = pd.read_csv(nome_arquivo_csv, encoding='utf-8', header=None, names=['concurso','data','dezena_1','dezena_2','dezena_3','dezena_4','dezena_5','dezena_6','ganhadores_sena','cidade','rateio_sena','ganhadores_quina','rateio_quina','ganhadores_quadra','rateio_quadra','acumulado','arrecadacao','estimativa','acumulado_especial','observacao'])

    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo_csv}' não encontrado.")
        return
    except pd.errors.ParserError as e:
        print(f"Erro ao ler o arquivo CSV '{nome_arquivo_csv}': {e}")
        return
    except Exception as e:
        print(f"Ocorreu um erro INESPERADO ao ler o arquivo CSV: {e}")
        return

    colunas_numeros = ['1ª Dezena', '2ª Dezena', '3ª Dezena', '4ª Dezena', '5ª Dezena', '6ª Dezena']

    # Converte para inteiro e remove linhas com NaN
    for coluna in colunas_numeros:
        dados_loteria[coluna] = pd.to_numeric(dados_loteria[coluna], errors='coerce').astype('Int64')
    dados_loteria_sem_na = dados_loteria.dropna(subset=colunas_numeros)

    # Embaralha as dezenas
    for index, row in dados_loteria_sem_na.iterrows():
        numeros_sorteados = row[colunas_numeros].dropna().tolist()
        np.random.shuffle(numeros_sorteados)
        dados_loteria_sem_na.loc[index, colunas_numeros[:len(numeros_sorteados)]] = numeros_sorteados

    # Melt para os gráficos
    todos_numeros = dados_loteria_sem_na[colunas_numeros].melt(value_name='Numero')['Numero']

    # Cálculos das estatísticas
    media_todos_numeros = todos_numeros.mean()
    medias_por_dezena = dados_loteria_sem_na[colunas_numeros].mean()
    medianas = dados_loteria_sem_na[colunas_numeros].median().astype(int)
    variancias = dados_loteria_sem_na[colunas_numeros].var()
    desvios_padrao = dados_loteria_sem_na[colunas_numeros].std()

    # Obtém os primeiros 5 números da primeira dezena para o exemplo
    primeiros_5_da_dezena1 = dados_loteria_sem_na['1ª Dezena'].head(5).tolist()

    # Imprime os resultados com explicações e exemplos reais (FORMATANDO A SAÍDA)
    print(f"\nMédia de TODOS os números sorteados: {media_todos_numeros:.2f}")
    print(f"\nCálculo da Média (exemplo com os primeiros 5 números da 1ª dezena: {primeiros_5_da_dezena1}):")
    soma = sum(primeiros_5_da_dezena1)
    quantidade = len(primeiros_5_da_dezena1)
    media_exemplo = soma / quantidade
    print(f"Soma dos números: {soma}")
    print(f"Quantidade de números: {quantidade}")
    print(f"Média: {soma} / {quantidade} = {media_exemplo:.2f}\n")

    print("Média dos números sorteados POR DEZENA:\n")
    print(medias_por_dezena.apply(lambda x: f"{x:.2f}").to_string())
    print("\nA média por dezena é calculada da mesma forma que a média geral, mas considerando apenas os números de cada dezena.\n")

    print("\nMediana dos números sorteados:\n")
    print(medianas.to_string())
    print(f"\nCálculo da Mediana (exemplo com os primeiros 5 números da 1ª dezena: {primeiros_5_da_dezena1}):")
    numeros_ordenados = sorted(primeiros_5_da_dezena1)
    print(f"Números ordenados: {numeros_ordenados}")
    if quantidade % 2 == 0:
        mediana_exemplo = (numeros_ordenados[quantidade // 2 - 1] + numeros_ordenados[quantidade // 2]) / 2
        print(f"Como há {quantidade} números (par), a mediana é a média dos dois do meio: ({numeros_ordenados[quantidade // 2 - 1]} + {numeros_ordenados[quantidade // 2]}) / 2 = {mediana_exemplo:.2f}\n")
    else:
        mediana_exemplo = numeros_ordenados[quantidade // 2]
        print(f"Como há {quantidade} números (ímpar), a mediana é o número do meio: {mediana_exemplo}\n")

    print("\nVariância dos números sorteados:\n")
    print(variancias.apply(lambda x: f"{x:.2f}").to_string())
    print(f"\nCálculo da Variância (exemplo com os primeiros 5 números da 1ª dezena: {primeiros_5_da_dezena1}):")
    print("1. Média (μ):", media_exemplo)
    print("2. (x - μ)² para cada número:")
    for x in primeiros_5_da_dezena1:
        print(f"   ({x} - {media_exemplo})² = {(x - media_exemplo)**2:.2f}")
    soma_dos_quadrados = sum([(x - media_exemplo)**2 for x in primeiros_5_da_dezena1])
    variancia_exemplo = soma_dos_quadrados / (quantidade - 1)
    print(f"3. Soma dos quadrados: {soma_dos_quadrados:.2f}")
    print(f"4. Variância (amostral): {soma_dos_quadrados} / ({quantidade} - 1) = {variancia_exemplo:.2f}\n")

    print("\nDesvio Padrão dos números sorteados:\n")
    print(desvios_padrao.apply(lambda x: f"{x:.2f}").to_string())
    print("\nCálculo do Desvio Padrão:")
    print(f"Raiz quadrada da Variância: √{variancia_exemplo:.2f} ≈ {np.sqrt(variancia_exemplo):.2f}\n")

    print("\nModa dos números sorteados (por dezena):\n")
    for coluna in colunas_numeros:
        moda_dezena = dados_loteria_sem_na[coluna].mode()
        if len(moda_dezena) > 1:
            print(f"Moda da {coluna}: {', '.join(map(str, moda_dezena.tolist()))}")
        else:
            print(f"Moda da {coluna}: {moda_dezena.iloc[0]}")
    print("\nA moda é o número que aparece com maior frequência em um conjunto de dados. Pode haver mais de uma moda (multimodal).\n")   

    # Gráficos
    num_bins = int(np.ceil(np.log2(todos_numeros.size) + 1))
    plt.figure(figsize=(16, 8))
    sns.histplot(todos_numeros, bins=num_bins, stat='count', discrete=True)
    plt.title('Histograma: Distribuição da Frequência dos Números Sorteados (Ordenado por Número)')
    plt.xlabel('Número Sorteado')
    plt.ylabel('Frequência')
    plt.xticks(np.arange(1, 61), rotation=90)
    plt.tight_layout()
    plt.savefig("histograma_megasena.png")
    plt.close()

    plt.figure(figsize=(16, 8))
    frequencias = todos_numeros.value_counts().sort_values(ascending=False)
    frequencias.plot(kind='bar')
    plt.title('Gráfico de Frequência: Números Sorteados (Ordenado por Frequência)')
    plt.xlabel('Número Sorteado')
    plt.ylabel('Frequência')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig("frequencia_megasena.png")
    plt.close()

    # Comparação entre Probabilidade Clássica e Experimental (cálculo das diferenças e gráfico)
    frequencia_esperada = len(todos_numeros) / 60
    diferencas = abs(frequencias - frequencia_esperada)
    
    # REMOVE ESTA LINHA DO megasena2.py:
    # print("\nDiferenças Absolutas entre Frequência Observada e Esperada:\n")
    # print(diferencas.to_string())

    megasena3.analisar_frequencia()

    # Análise com Distribuição Binomial (Exemplo com 10 Jogos)
    print("\nAnálise com Distribuição Binomial (Exemplo com 10 Jogos):\n")
    print("Esta análise utiliza a distribuição binomial para calcular a probabilidade de acertar *pelo menos um* dos 6 números apostados em um número fixo de jogos.")
    print("Consideramos o exemplo de uma pessoa que joga na Mega Sena 10 vezes seguidas, escolhendo 6 números aleatórios em cada jogo.\n")

    n_jogos = 10  # Número de tentativas (jogos)
    prob_acerto_um_numero = 6 / 60  # Probabilidade de acertar um número em um único jogo

    # Calcula as probabilidades para 0 a 10 jogos com pelo menos um acerto
    probabilidades = [stats.binom.pmf(k, n_jogos, prob_acerto_um_numero) for k in range(n_jogos + 1)]

    # Calcula a probabilidade de acertar PELO MENOS UM número em PELO MENOS UM dos 10 jogos
    prob_acertar_pelo_menos_um = 1 - stats.binom.pmf(0, n_jogos, prob_acerto_um_numero)

    # Cálculo detalhado da probabilidade de NÃO acertar nenhum número em 10 jogos
    prob_nao_acertar_em_um_jogo = 1 - prob_acerto_um_numero  # Probabilidade de NÃO acertar em um jogo = 1 - 0.1 = 0.9
    prob_nao_acertar_em_10_jogos = prob_nao_acertar_em_um_jogo ** n_jogos  # Probabilidade de NÃO acertar em 10 jogos = (0.9)^10 ≈ 0.3487

    # Calcula a probabilidade de acertar PELO MENOS UM número em PELO MENOS UM dos 10 jogos
    prob_acertar_pelo_menos_um = 1 - prob_nao_acertar_em_10_jogos

    print("Cálculo Detalhado da probabilidade de acertar PELO MENOS UM número em um único jogo:\n")
   
    print("Há 60 números na Mega Sena e alguém escolhe 6. A probabilidade de NÃO acertar NENHUM dos 6 números em um sorteio é calculada da seguinte forma:")
    
    print("Se 54 números que NÃO foram escolhidos (60 - 6 = 54), a probabilidade de o primeiro número sorteado NÃO ser um dos seus é 54/60.")
    print("Como os sorteios são sem reposição, a probabilidade do segundo número sorteado NÃO ser um dos números sorteados é de 53/59, e assim por diante.")
    print("Portanto, a probabilidade de NÃO acertar NENHUM dos 6 números escolhidos é: (54/60) * (53/59) * (52/58) * (51/57) * (50/56) * (49/55) ≈ 0.407\n") # Cálculo mais preciso para melhor entendimento.

    print("De forma mais direta: 54/60 = 0.9. Ou seja, há 90% de chance de se errar todos os números.")
    print("Portanto, a probabilidade de acertar PELO MENOS UM número é: 1 - 0.9 = 0.1, ou seja, 10%. Logo:\n")

    print(f"1. Probabilidade de NÃO acertar um número em um único jogo: 1 - {prob_acerto_um_numero:.2f} = {prob_nao_acertar_em_um_jogo:.4f}")
    print(f"2. Probabilidade de NÃO acertar um número em NENHUM dos 10 jogos: ({prob_nao_acertar_em_um_jogo:.4f})^{n_jogos} = {prob_nao_acertar_em_10_jogos:.4f}")
    print(f"3. Probabilidade de acertar PELO MENOS UM número em PELO MENOS UM dos 10 jogos: 1 - {prob_nao_acertar_em_10_jogos:.4f} = {prob_acertar_pelo_menos_um:.4f}\n")

    print(f"Probabilidade de acertar pelo menos um número em pelo menos um dos 10 jogos: {prob_acertar_pelo_menos_um:.4f} ({prob_acertar_pelo_menos_um*100:.2f}%)\n")

    # Nova seção: Teoria da Probabilidade na Mega Sena (Probabilidades de Acerto)
    print("\nTeoria da Probabilidade na Mega Sena (Probabilidades de Acerto):\n")

    print("O espaço amostral (número total de combinações possíveis) na Mega Sena é calculado por combinação simples:")
    print("C(60, 6) = 60! / (6! * (60-6)!) = 50.063.860\n")
    print("Este número (50.063.860) será o denominador em todos os cálculos de probabilidade abaixo, pois representa o número total de resultados possíveis.\n")

    print("Probabilidades de Acerto em um Único Jogo:\n")

    # Cálculos detalhados das probabilidades
    total_combinacoes = 50063860 #Armazena o total de combinações para melhor entendimento.

    print("- Sena (6 números):\n")
    print("  Para acertar a Sena, é preciso acertar os 6 números sorteados. Existe apenas 1 combinação que acerta os 6 números.")
    
    prob_sena = 1 / total_combinacoes
    
    print(f"  Probabilidade: 1 / {total_combinacoes} ≈ {prob_sena:.8f} (aproximadamente {prob_sena*100:.6f}%)\n")

    print("- Quina (5 números):\n")
    print("  Para acertar a Quina, é preciso acertar 5 dos 6 números sorteados e errar 1.")
    print("  Existem C(6, 5) = 6 maneiras de escolher 5 números corretos dentre os 6 sorteados.")
    print("  Existem C(54, 1) = 54 maneiras de escolher 1 número incorreto dentre os 54 restantes (60 - 6 = 54).")
    print("  Portanto, existem 6 * 54 = 324 combinações que resultam em uma Quina.")
    
    prob_quina = (6 * 54) / total_combinacoes
    
    print(f"  Probabilidade: (6 * 54) / {total_combinacoes} = 324 / {total_combinacoes} ≈ {prob_quina:.8f} (aproximadamente {prob_quina*100:.5f}%)\n")

    print("- Quadra (4 números):\n")
    print("  Para acertar a Quadra, é preciso acertar 4 dos 6 números sorteados e errar 2.")
    print("  Existem C(6, 4) = (6!)/(4!*2!) = 15 maneiras de escolher 4 números corretos dentre os 6 sorteados.")
    print("  Existem C(54, 2) = (54!)/(52!*2!) = 1431 maneiras de escolher 2 números incorretos dentre os 54 restantes.")
    print("  Portanto, existem 15 * 1431 = 21465 combinações que resultam em uma Quadra.")
    
    prob_quadra = (15 * 1431) / total_combinacoes
    
    print(f"  Probabilidade: (15 * 1431) / {total_combinacoes} = 21465 / {total_combinacoes} ≈ {prob_quadra:.8f} (aproximadamente {prob_quadra*100:.4f}%)\n")

    print("Cada sorteio da Mega Sena é um evento independente dos anteriores. O resultado de um sorteio não influencia os resultados dos sorteios seguintes.\n")


    # Cria o gráfico da distribuição binomial com explicações
    plt.figure(figsize=(10, 6))
    plt.bar(range(n_jogos + 1), probabilidades)

    # Melhora os rótulos do gráfico e adiciona título explicativo
    plt.xlabel("Número de Jogos com Pelo Menos Um Acerto (de 10)", fontsize=12)  # Rótulo mais completo
    plt.ylabel("Probabilidade", fontsize=12)
    plt.title(f"Distribuição Binomial: Probabilidade de Acertar Pelo Menos Um Número em {n_jogos} Jogos\n(Probabilidade de Acerto em um Jogo: {prob_acerto_um_numero:.2f})", fontsize=14, fontweight='bold')
    plt.xticks(range(n_jogos + 1), fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(axis='y', linestyle='--')

    # Adiciona anotações no gráfico para melhor entendimento
    plt.annotate("Probabilidade de não acertar\nem nenhum dos 10 jogos", xy=(0, probabilidades[0]), xytext=(-1, probabilidades[0]+0.02), arrowprops=dict(facecolor='black', shrink=0.05), fontsize=10)
    plt.annotate("Probabilidade de acertar\nem todos os 10 jogos", xy=(10, probabilidades[10]), xytext=(7, probabilidades[10]+0.02), arrowprops=dict(facecolor='black', shrink=0.05), fontsize=10)

    plt.tight_layout() #Melhora o layout do grafico para evitar cortes
    plt.savefig("distribuicao_binomial_megasena.png")
    plt.close()

    # Nova seção: Distribuições Discretas e a Análise de Frequência
    print("\nDistribuições Discretas e a Análise de Frequência na Mega Sena:\n")

    print("Como os números sorteados na Mega Sena são inteiros e distintos, podemos usar distribuições discretas para modelar aspectos do jogo.\n")

    print("- Distribuição Uniforme Discreta (Idealizada):\n")
    print("  Em um cenário ideal, onde todos os números têm exatamente a mesma probabilidade de serem sorteados, teríamos uma distribuição uniforme discreta.") 
    print("  Isso significa que a probabilidade de qualquer número específico ser sorteado é 1/60.\n")

    print("  A 'frequência esperada' (número total de dezenas sorteadas / 60) representa o que esperaríamos sob essa distribuição ideal.")
    print("  A análise de frequência compara as frequências *observadas* (quantas vezes cada número realmente foi sorteado) com essa frequência *esperada*.\n")

    print("  Desvios entre a frequência observada e esperada são naturais devido à aleatoriedade dos sorteios.")    
    print("  Pequenas variações são normais e não indicam necessariamente um viés no sorteio.")
    print("  Desvios muito grandes, no entanto, poderiam levantar suspeitas e justificar uma investigação mais aprofundada.\n")

    print("- Distribuição Hipergeométrica (Probabilidade de Acerto):\n")
    print("  A distribuição hipergeométrica é a mais adequada para calcular as probabilidades de acertar a Sena, Quina ou Quadra, pois ela modela o sorteio sem reposição (uma vez que um número é sorteado, ele não volta para o sorteio).")
    print("  As fórmulas usadas anteriormente para calcular as probabilidades de Sena, Quina e Quadra são derivadas da distribuição hipergeométrica.\n")

    print("Em resumo, a análise de frequência busca verificar se os sorteios se comportam de acordo com o que seria esperado em um sorteio justo e aleatório, modelado pela distribuição uniforme discreta.")
    print("As probabilidades de acerto (Sena, Quina, Quadra) são calculadas usando a distribuição hipergeométrica, que considera o sorteio sem reposição.\n")

    print("\nConclusões:")
    print("\n1. Distribuição Aparente: O histograma mostra a distribuição de frequência dos números sorteados. Visualmente, parece haver uma distribuição relativamente uniforme, como esperado em um sorteio aleatório, mas podemos observar pequenas variações.")
    print("\n2. Dispersão dos Números: A variância e o desvio padrão quantificam a dispersão dos números em cada dezena. Valores maiores indicam maior variação.")
    print("\n3. Números Recorrentes: O gráfico de frequência ordenada destaca os números que apareceram com mais frequência. No entanto, é importante lembrar que, em um sorteio justo, essas diferenças devem ser pequenas devido ao acaso.")
    print("\n4. Independência dos sorteios: Cada sorteio da Mega Sena é independente dos anteriores. A análise estatística descritiva dos números sorteados ao longo do tempo nos dá uma visão geral da distribuição dos números, mas não permite prever os próximos sorteios.\n")
    print("\nExplicação das médias POR DEZENA:")
    print("As médias por dezena, após o embaralhamento, devem apresentar valores próximos à média geral, confirmando a aleatoriedade dos sorteios.\n")

    # Explicação sobre a Distribuição Normal
    print("\nExplicação sobre a Distribuição Normal:\n")
    print("A distribuição normal é uma distribuição contínua, enquanto os números da Mega Sena são discretos (inteiros de 1 a 60).")
    print("Além disso, a distribuição normal é simétrica, enquanto a distribuição dos números da Mega Sena, idealmente, deve ser uniforme (cada número com a mesma probabilidade).")
    print("Portanto, a distribuição normal não é um modelo adequado para representar a distribuição dos números sorteados na Mega Sena.\n")

    # Explicação sobre a Distribuição Binomial
    print("\nExplicação sobre a Distribuição Binomial:\n")
    print("A distribuição binomial é útil para calcular a probabilidade de um número de sucessos em um número fixo de tentativas.")
    print("Por exemplo, poderíamos usar a binomial para calcular a probabilidade de acertar um número específico na Mega Sena em X jogos.")
    print("No entanto, nosso objetivo aqui é analisar a frequência com que os números são sorteados ao longo dos concursos, e não a probabilidade de acerto em um número fixo de tentativas.")
    print("Portanto, a distribuição binomial não é diretamente aplicável para analisar a distribuição de frequência dos números sorteados.\n")

    # Explicação sobre o Teorema de Bayes
    print("\nExplicação sobre o Teorema de Bayes:\n")
    print("O Teorema de Bayes é usado para calcular probabilidades condicionais, ou seja, a probabilidade de um evento ocorrer dado que outro evento já ocorreu.")
    print("Na Mega Sena, os sorteios são independentes: o resultado de um sorteio não influencia o resultado dos sorteios seguintes.")
    print("Portanto, a probabilidade de um número ser sorteado em um concurso não depende se ele foi sorteado ou não em concursos anteriores.")
    print("Consequentemente, a aplicação direta do Teorema de Bayes para prever números na Mega Sena é redundante, pois a probabilidade condicional é igual à probabilidade incondicional (P(A|B) = P(A)).\n")

    # Explicação sobre a Distribuição Exponencial
    print("\nExplicação sobre a Distribuição Exponencial:\n")
    print("A distribuição exponencial modela o tempo entre eventos em um processo de Poisson, onde os eventos ocorrem de forma contínua e independente a uma taxa constante.")
    print("Na Mega Sena, os sorteios ocorrem em intervalos discretos (não contínuos) e o que analisamos é a frequência dos números sorteados, não o tempo entre os sorteios.")
    print("Além disso, a distribuição exponencial é adequada para modelar tempos de espera ou durações, o que não se aplica diretamente à análise da frequência dos números da Mega Sena.")
    print("Portanto, a distribuição exponencial não é um modelo apropriado para este tipo de análise.\n")

    # *** CHAMADA PARA megasena4.py (CORRIGIDA) ***
    dados_loteria_sem_na, colunas_numeros = processar_dados_mega_sena() #Apenas a chamada, sem a definição da função aqui dentro.
    if dados_loteria_sem_na is not None:    
        megasena4.analisar_variaveis_mega_sena(dados_loteria_sem_na, colunas_numeros)
    

    # FIM DA FUNÇÃO analisar_mega_sena

if __name__ == "__main__":
    nome_csv = 'megasena_final.csv'
    analisar_mega_sena(nome_csv)