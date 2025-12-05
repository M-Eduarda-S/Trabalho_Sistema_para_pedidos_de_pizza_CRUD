import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Carrega variáveis do arquivo .env
load_dotenv()

# Estabelece conexão com o Banco de Dados
def conectar():
    try:
        conexao = mysql.connector.connect(
            host=os.getenv("BD_HOST"), # pega o valor de cada variável
            user=os.getenv("BD_USER"),
            password=os.getenv("BD_SENHA"), 
            database=os.getenv("BD_NOME")
        )
        if conexao.is_connected():
            # print para testes
            print("\nConexão ao Banco de Dados realizada com sucesso!\n")
            return conexao
    except Error as erro:
        print("Erro ao conectar ao Banco de Dados:", erro)
        return None # para não retornar nada se der erro

# Para testar a conexão
# conexao = conectar()