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




def listarPedidos():
    conexao = conectar()
    if conexao is None:
        return

    try:
        cursor = conexao.cursor()

        sql = """
            SELECT Pedido.id, Pessoa.nome, Pedido.status, Pedido.valor_pagamento, Pedido.data_pedido
            FROM Pedido
            INNER JOIN Cliente ON Pedido.id_cliente = Cliente.id
            INNER JOIN Pessoa ON Cliente.id_pessoa = Pessoa.id
        """

        cursor.execute(sql)
        pedidos = cursor.fetchall()

        print("\n--- LISTA DE PEDIDOS ---")
        for p in pedidos:
            print(f"ID: {p[0]} | Cliente: {p[1]} | Status: {p[2]} | Valor: R${p[3]} | Data: {p[4]}")

    except Error as e:
        print("Erro ao listar pedidos:", e)

    finally:
        cursor.close()
        conexao.close()


def atualizarPedido():
    conexao = conectar()
    if conexao is None:
        return

    try:
        cursor = conexao.cursor()

        id_pedido = input("\nID do pedido que deseja atualizar: ")

        cursor.execute("SELECT id FROM Pedido WHERE id=%s", (id_pedido,))
        if cursor.fetchone() is None:
            print("Pedido não encontrado!")
            return

        print("\n--- ATUALIZAR PEDIDO ---")
        print("Status disponíveis:")
        print("1 - Aberto")
        print("2 - Em preparo")
        print("3 - Saiu para entrega")
        print("4 - Entregue")
        print("5 - Cancelado")

        opc = input("\nEscolha novo status: ")

        match opc:
            case "1": novo_status = "Aberto"
            case "2": novo_status = "Em preparo"
            case "3": novo_status = "Saiu para entrega"
            case "4": novo_status = "Entregue"
            case "5": novo_status = "Cancelado"
            case _:
                print("Opção inválida.")
                return

        cursor.execute("UPDATE Pedido SET status=%s WHERE id=%s", (novo_status, id_pedido))
        conexao.commit()

        print("\nStatus atualizado com sucesso!")

    except Error as e:
        print("Erro ao atualizar pedido:", e)

    finally:
        cursor.close()
        conexao.close()

def deletarPedido():
    conexao = conectar()
    if conexao is None:
        return

    try:
        cursor = conexao.cursor()

        id_pedido = input("\nID do pedido para deletar: ")

        cursor.execute("SELECT id FROM Pedido WHERE id=%s", (id_pedido,))
        if cursor.fetchone() is None:
            print("Pedido não encontrado!")
            return

        cursor.execute("DELETE FROM Pedido WHERE id=%s", (id_pedido,))
        conexao.commit()

        print("\nPedido deletado com sucesso!")

    except Error as e:
        print("Erro ao deletar pedido:", e)

    finally:
        cursor.close()
        conexao.close()

