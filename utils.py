from datetime import datetime
import pandas as pd
import subprocess
import zipfile
import os

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
processamento_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'processamento')

def descompactar_arquivo(file_path):
    try:
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(processamento_dir)
        print("Arquivo descompactado com sucesso!")
        os.remove(file_path)
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {file_path}")

def rename_extension(file_path, old_extension = ".ex_", new_extension = ".exe"):
    os.rename(file_path, file_path.replace(old_extension, new_extension))

def execute_file(file_path):
    try:
        subprocess.run(file_path, cwd=processamento_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print(f"Arquivo .exe executado com sucesso!")
        os.remove(file_path)
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {file_path}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

def rename_file(file_path, new_name):
    os.rename(file_path, new_name) 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def save_folder(arquivo, data):
    data = data.strftime('%y%m%d')
    return os.path.join("Y:\\Geral\\Fundos Ativos\\FIDC\\Syngenta I FIDC\\CARTEIRA\\Prêmio Precificação Hedge B3", f"{arquivo}_{data}.xlsx")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def parse_date(date_str):
    return pd.to_datetime(date_str, format='%d_%m_%Y')

colspecs = [(0, 6), (6, 9), (9, 11), (11, 19),
            (19, 22), (22, 23), (23, 27), (27, 28),
            (28, 29), (29, 37), (37, 52), (52, 67), (67, 68)]

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
