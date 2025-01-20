import pandas as pd

def corrigir_csv(nome_arquivo_entrada, nome_arquivo_saida):
    """Lê um CSV, seleciona colunas, converte para inteiro e salva um novo CSV."""
    try:
        df = pd.read_csv(nome_arquivo_entrada)
        colunas_selecionadas = ['Concurso', '1ª Dezena', '2ª Dezena', '3ª Dezena', '4ª Dezena', '5ª Dezena', '6ª Dezena']
        df = df[colunas_selecionadas]  # Seleciona apenas as colunas desejadas

        df['Concurso'] = pd.to_numeric(df['Concurso'], errors='coerce').astype('Int64') #Converte Concurso para Int64

        for coluna in colunas_selecionadas[1:]: #Começa do índice 1 para pular a coluna Concurso
            df[coluna] = pd.to_numeric(df[coluna], errors='coerce').astype('Int64')

        df.to_csv(nome_arquivo_saida, index=False, encoding='utf-8')
        print(f"Arquivo '{nome_arquivo_saida}' criado/corrigido com sucesso!")
        return True
    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo_entrada}' não encontrado.")
        return False
    except Exception as e:
        print(f"Erro ao processar o CSV: {e}")
        return False

# Exemplo de uso:
nome_arquivo_entrada = 'New_Jogos_Megasena.csv'
nome_arquivo_saida = 'megasena_final.csv'

if corrigir_csv(nome_arquivo_entrada, nome_arquivo_saida):
    print("Processo de correção do CSV concluído.")
else:
    print("Processo de correção do CSV falhou.")