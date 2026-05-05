import csv
import os

PASTA = 'arquivos'

def inicializar_diretorio():
    if not os.path.exists(PASTA):
        os.makedirs(PASTA)

def salvarArquivo(dadosCSV):
    inicializar_diretorio()
    CAMINHO_ARQUIVO = os.path.join(PASTA, 'Planilha_Loja.csv')
    CAMPOS = ['Fornecedor','Data de Vencimento','Tipo De Doc', 'Nº do Doc', 'Valor', 'Status', 'Código de Barras']
    arquivo_existe = os.path.exists(CAMINHO_ARQUIVO)


    with open(CAMINHO_ARQUIVO, 'a', newline='', encoding='utf-8') as f:
        escritor = csv.writer(f)
        if not arquivo_existe:
            escritor.writerow(CAMPOS)
        escritor.writerows([dadosCSV])
    
def lerTudo():
    CAMINHO_ARQUIVO = os.path.join(PASTA, 'Planilha_Loja.csv')
    if not os.path.exists(CAMINHO_ARQUIVO):
        return []
    
    with open(CAMINHO_ARQUIVO, 'r', encoding='utf-8') as f:
        leitor = csv.reader(f)
        return list(leitor) # Retorna uma lista de listas

def sobrescreverArquivo(lista_completa):
    inicializar_diretorio()
    CAMINHO_ARQUIVO = os.path.join(PASTA, 'Planilha_Loja.csv')
    with open(CAMINHO_ARQUIVO, 'w', newline='', encoding='utf-8') as f:
        escritor = csv.writer(f)
        escritor.writerows(lista_completa)