import mysql.connector
from mysql.connector import Error

# Estabelece conexão com o Banco de Dados
def conectar():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Pr0gr4m4ç40+BD", 
            database="pizzaria_pedidos"
        )
        if conexao.is_connected():
            print("Conexão ao Banco de Dados realizada com sucesso!")
            return conexao
    except Error as erro:
        print("Erro ao conectar ao Banco de Dados:", erro)
        return None # para não retornar nada se der erro

#NAO MOSTRAR A PASSWORD!!!!!!!!!!!!!!!!

conexao = conectar()