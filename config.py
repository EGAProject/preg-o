from datetime import datetime
import pandas as pd
import questionary
import requests
import time
import os

from utils import processamento_dir, descompactar_arquivo, rename_extension, execute_file, rename_file, parse_date

def select_data():
    while True:
        datas_str = questionary.text("Por favor, insira as datas no formato dd/mm/aaaa (separadas por vírgula):").ask()
        datas_list = [data.strip() for data in datas_str.split(",")]
        datas_validas = []
        datas_invalidas = []
        for data in datas_list:
            try:
                data_formatada = datetime.strptime(data, "%d/%m/%Y")
                datas_validas.append(data_formatada)
            except ValueError:
                datas_invalidas.append(data)
        if datas_invalidas:
            print(f"As seguintes datas estão no formato incorreto: {', '.join(datas_invalidas)}. Tente novamente.")
        else:
            print("Todas as datas foram validadas com sucesso!")
            return datas_validas
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# 1
def requisicao(data):
    data = data.strftime('%y%m%d')
    response = requests.get(f"https://www.b3.com.br/pesquisapregao/download?filelist=RE{data}.ex_")
    if response.status_code == 200:
        file = f"RE{data}.zip"
        with open(os.path.join(processamento_dir, file), 'wb') as f:
            f.write(response.content)
        return file
    else:
        print(f"Erro ao fazer requisição. Status Code: {response.status_code}")
        quit()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# 2  
def tratar_arquivo(data, file, processamento_dir):
    data = data.strftime('%y%m%d')

    zip_file = os.path.join(processamento_dir, file)
    if zip_file:
        descompactar_arquivo(zip_file)
    time.sleep(0.5)
    ex_file = os.path.join(processamento_dir, f"RE{data}.ex_")
    if ex_file:
        rename_extension(ex_file)
    time.sleep(2)
    exe_file = os.path.join(processamento_dir, f"RE{data}.exe")
    if exe_file:
        execute_file(exe_file)
    time.sleep(2)
    premio_file = os.path.join(processamento_dir, "Premio.txt")
    if premio_file:
        premio =  os.path.join(processamento_dir, f"Premio_{data}.txt")
        rename_file(premio_file, premio)
    return premio
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# 3
def ler_arquivo(premio, colspecs, nomes_colunas, tipos_colunas):
    df = pd.read_fwf(premio,colspecs=colspecs, names=nomes_colunas, dtype=tipos_colunas,
                    parse_dates = ["Data de Referência", "Data de Vencimento do Contrato"],
                    date_format='%Y%m%d')
    os.remove(premio)
    return df
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# 
def modelar_df(df, dicionario_traducao): 
    for coluna, traducoes in dicionario_traducao.items():
        if coluna in df.columns:
            df[coluna] = df[coluna].replace(traducoes)
    df['Preço de Exercício (Opções)'] = df.apply(
        lambda row: f"{(row['Preço de Exercício (Opções)'] / 100):.{int(row['Número de Casas Decimais'])}f}", axis=1)
    df['Preço de Referência da Opção'] = df.apply(
        lambda row: f"{(row['Preço de Referência da Opção'] / 100):.{int(row['Número de Casas Decimais'])}f}", axis=1)
    return df
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# 4
def salvar_arquivo(arquivo, df):
    df.to_excel(arquivo, index=False)
    print("Arquivo excel gerado com sucesso!")

