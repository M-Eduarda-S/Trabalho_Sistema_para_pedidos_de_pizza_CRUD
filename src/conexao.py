import mysql.connector
from mysql.connector import Error

# Estabelece conexão com o Banco de Dados
def conectar():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="digite_a_sua_password", 
            database="pizzaria_pedidos"
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