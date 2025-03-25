from config import select_data, requisicao, tratar_arquivo, ler_arquivo, salvar_arquivo, modelar_df
from utils import processamento_dir, colspecs, nomes_colunas, tipos_colunas, save_folder, dicionario_traducao

def main():
    # 1 - Selecionar Datas
    datas_selecionadas = select_data()
    if len(datas_selecionadas) > 0:
        print("Datas selecionadas:", ', '.join([data.strftime("%d/%m/%Y") for data in datas_selecionadas]))
    else:
        print("Data selecionada:", datas_selecionadas[0].strftime("%d/%m/%Y"))
    for data in datas_selecionadas:
        # 2 - Realizar a requisição
        file = requisicao(data)
        # 3 - Tratar o arquivo
        premio = tratar_arquivo(data, file, processamento_dir)
        # 4 - Ler o arquivo
        df = ler_arquivo(premio, colspecs, nomes_colunas, tipos_colunas)
        # 5 - Modelar o DF
        df = modelar_df(df, dicionario_traducao)
        # 6 - Salvar o arquivo
        salvar_arquivo(save_folder("Premio", data), df)
if __name__ == "__main__":
    main()
#