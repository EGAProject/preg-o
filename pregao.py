from datetime import datetime
import pandas as pd
import requests
import zipfile
import time
import os

# 1
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
data = datetime(2025, 3, 19).strftime('%y%m%d')

# 2
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# URL do arquivo
url = f"https://www.b3.com.br/pesquisapregao/download?filelist=RE{data}.ex_"

# Fazendo a requisição GET
response = requests.get(url)

# Verificando se a requisição foi bem-sucedida
if response.status_code == 200:
    # Salvando o arquivo compactado
    with open(f"RE{data}.zip", 'wb') as f:
        f.write(response.content)
    
    print(f"Arquivo salvo com sucesso em RE{data}.zip")
else:
    print(f"Erro ao fazer requisição. Status Code: {response.status_code}")

# 3
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Caminho do diretório onde o arquivo foi salvo
diretorio_atual = os.path.dirname(f"RE{data}.zip")

# Verificando se o arquivo é um .zip
if f"RE{data}.zip":
    with zipfile.ZipFile(f"RE{data}.zip", 'r') as zip_ref:
        # Extraindo todos os arquivos no mesmo diretório
        zip_ref.extractall(diretorio_atual)
    print(f"Arquivo descompactado em: {os.path.abspath(diretorio_atual)}")
else:
    print("O arquivo não é um arquivo .zip.")

os.rename(f"RE{data}.ex_", f"RE{data}.exe")

try:
    os.startfile(f"RE{data}.exe")
    print(f"Arquivo RE{data}.exe executado com sucesso.")
except FileNotFoundError:
    print(f"Arquivo não encontrado: RE{data}.exe")
except Exception as e:
    print(f"Erro inesperado: {e}")

time.sleep(2)

os.rename("Premio.txt", f"Premio_{data}.txt")

# 4
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Definindo as larguras dos campos manualmente (por exemplo, 10 caracteres para o primeiro campo, 20 para o segundo, etc.)
colspecs = [(0, 6), (6, 9), (9, 11), (11, 19),
            (19, 22), (22, 23), (23, 27), (27, 28),
            (28, 29), (29, 37), (37, 52), (52, 67), (67, 68)]

# Lista de nomes das colunas
nomes_colunas = [
    "Identificação da Transação",
    "Complemento da Transação",
    "Tipo de Registro",
    "Data de Referência",
    "Código da Mercadoria",
    "Tipo de Mercado",
    "Série (Opções)",
    "Indicador de Tipo de Opção",
    "Tipo de Opção",
    "Data de Vencimento do Contrato",
    "Preço de Exercício (Opções)",
    "Preço de Referência da Opção",
    "Número de Casas Decimais",
]

# Definindo os tipos de dados para cada coluna (caso necessário)
tipos_colunas = {
    "Identificação da Transação": int,
    "Complemento da Transação": int,
    "Tipo de Registro": int,
    "Data de Referência": str,  # Pode ser ajustado para datetime, dependendo do formato
    "Código da Mercadoria": str,
    "Tipo de Mercado": str,
    "Série (Opções)": str,
    "Indicador de Tipo de Opção": str,
    "Tipo de Opção": str,
    "Data de Vencimento do Contrato": str,  # Ajustar conforme o formato real
    "Preço de Exercício (Opções)": int,
    "Preço de Referência da Opção": int,
    "Número de Casas Decimais": int,
}

dicionario_traducao = {
    "Tipo de Mercado": {"3": "Opções Sobre Disponível", "4": "Opções Sobre Futuro "},
    "Indicador de Tipo de Opção": {"C": "Compra", "V": "Venda"},
    "Tipo de Opção": {"A": "Americana", "E": "Européia"},
}

def parse_date(date_str):
    return pd.to_datetime(date_str, format='%Y%m%d')

# Lendo o arquivo com as larguras fixas e os tipos de dados especificados
df = pd.read_fwf(f"Y:\\Usuários\\Felipe.Colombini\\Scripts\Pregão\\Processamento\\Premio_250320.txt",
                 colspecs=colspecs, names=nomes_colunas, dtype=tipos_colunas,
                 parse_dates = ["Data de Referência", "Data de Vencimento do Contrato"],
                 date_parser = parse_date)
for coluna, traducoes in dicionario_traducao.items():
    if coluna in df.columns:
        df[coluna] = df[coluna].replace(traducoes)
df['Preço de Exercício (Opções)'] = df.apply(
    lambda row: f"{(row['Preço de Exercício (Opções)'] / 100):.{int(row['Número de Casas Decimais'])}f}", axis=1)
df['Preço de Referência da Opção'] = df.apply(
    lambda row: f"{(row['Preço de Referência da Opção'] / 100):.{int(row['Número de Casas Decimais'])}f}", axis=1)

# Exibindo as primeiras linhas do DataFrame
df.to_excel(f"Y:\\Usuários\\Felipe.Colombini\\Scripts\Pregão\\Processamento\\Premio_250320.xlsx", index=False)

os.remove(f"RE{data}.zip")
os.remove(f"RE{data}.exe")
os.remove(f"Premio_{data}.txt")
