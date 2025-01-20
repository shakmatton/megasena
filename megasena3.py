from tabulate import tabulate
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def analisar_frequencia():
    """Analisa a frequência dos números sorteados na Mega Sena."""
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

    frequencias = todos_numeros.value_counts().sort_index()
    frequencia_esperada = len(todos_numeros) / 60
    diferencas = abs(frequencias - frequencia_esperada)

    # Exibe as diferenças formatadas
    print("\nDiferenças Absolutas entre Frequência Observada e Esperada:\n")

    tabela = []
    linha = []
    largura_coluna = 25

    for numero, diferenca in diferencas.items():
        formato = "{: <" + str(largura_coluna) + "}"
        linha.append(formato.format(f"{numero} - {diferenca:.1f}"))

        if len(linha) == 5:
            tabela.append(linha)
            linha = []

    if linha:
        tabela.append(linha)

    print(tabulate(tabela, tablefmt="plain"))

    # Nova seção: Exibe as frequências absolutas, esperadas e médias
    print("\nFrequência dos Números (Obtida e Esperada) e Média:\n")

    total_jogos = len(dados_loteria_sem_na) #Conta o total de jogos
    print(f"Total de jogos realizados: {total_jogos}\n") #Imprime o total de jogos

    tabela_frequencias = []
    for numero in range(1, 61):
        frequencia_obtida = frequencias.get(numero, 0)
        tabela_frequencias.append([numero, frequencia_obtida, frequencia_esperada, f"{frequencia_obtida / total_jogos:.2f}"]) #Arredonda a média para 2 casas decimais

    print(tabulate(tabela_frequencias, headers=["Número", "Frequência Obtida", "Frequência Esperada", "Média"], tablefmt="grid"))

    # Explicação das colunas "Frequência Esperada" e "Média"
    print("\n\nExplicação das Colunas:\n")
    print("Frequência Esperada: Representa a frequência teórica que cada número deveria ter se os sorteios fossem perfeitamente aleatórios. É calculada dividindo o número total de dezenas sorteadas (6 dezenas por jogo * número de jogos) por 60 (total de números possíveis).")
    print(f"No caso, a frequência esperada para cada número é: {len(todos_numeros)} / 60 = {frequencia_esperada:.2f}")
    print("Média: Representa a frequência média com que cada número foi sorteado por jogo. É calculada dividindo a 'Frequência Obtida' de cada número pelo 'Total de jogos realizados'.")

    # Gráfico das diferenças
    plt.figure(figsize=(16, 8))
    plt.bar(diferencas.index, diferencas)
    plt.xlabel("Número Sorteado")
    plt.ylabel("Diferença Absoluta")
    plt.title("Diferença entre Frequência Observada e Esperada")
    plt.xticks(np.arange(1, 61), rotation=90)
    plt.tight_layout()
    plt.savefig("diferencas_frequencia.png")
    plt.close()

    # Justificativa da comparação
    print("\n\nJustificativa da Comparação entre Frequência Observada e Esperada:\n")
    print("Em um sorteio justo e aleatório, espera-se que cada número tenha aproximadamente a mesma probabilidade de ser sorteado (1/60).")
    print("A comparação entre a frequência observada (a frequência com que cada número realmente foi sorteado nos dados históricos) e a frequência esperada (calculada com base na probabilidade teórica) permite verificar se os resultados dos sorteios se aproximam do esperado teoricamente.")
    print("Desvios significativos entre a frequência observada e a esperada podem indicar a necessidade de uma investigação mais aprofundada, embora pequenas variações sejam esperadas devido à natureza aleatória dos sorteios.\n")