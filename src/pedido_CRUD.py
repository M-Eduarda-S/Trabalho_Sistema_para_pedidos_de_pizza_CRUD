from conexao import conectar
from mysql.connector import Error
from cliente_CRUD import listarClientes
from datetime import datetime


# Criar um novo pedido
def criarPedido():
    conexao = conectar()
    if conexao is None:
        return
    
    try:
        cursor = conexao.cursor()

        print("\n--- CRIANDO PEDIDO ---")

        # Escolher cliente
        print("\n--- SELECIONE O CLIENTE ---")
        listarClientes()

    
        
        id_cliente = input("\nID do cliente que está fazendo o pedido: ")

        # Endereço 
        endereco_entrega = input("Endereço de entrega: ")

        # Valor  
        valor_pagamento = float(input("Valor do pagamento (digite 0 se não tiver ainda): "))
        

        # Status inicial
        status = "Aberto"

        # Data e horário atuais
        data_atual = datetime.now().date()
        hora_atual = datetime.now().time()

        sql = """
            INSERT INTO Pedido (id_cliente, valor_pagamento, status, endereco_entrega, data_pedido, horario_pedido)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (id_cliente, valor_pagamento, status, endereco_entrega, data_atual, hora_atual))
        conexao.commit()

        print("\nPedido criado com sucesso!")
        print(f"ID do pedido: {cursor.lastrowid}")

    except Error as e:
        print("Erro ao criar pedido:", e)

    finally:
        cursor.close()
        conexao.close()

