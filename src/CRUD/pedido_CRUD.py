from conexao import conectar
from mysql.connector import Error
from datetime import datetime # coletar a data atual

# funcao auxiliar para adicionar pizzas ao pedido
def listarTamanhosPizza(cursor):
    print("\n--- Tamanhos disponíveis ---")
    cursor.execute("SELECT id, tamanho, valor_pizza FROM Pizza")
    tamanhos = cursor.fetchall()
    for t in tamanhos:
        print(f"ID: {t[0]} - Tamanho: {t[1]} (R$ {t[2]:.2f})")

# funcao auxiliar para adicionar pizzas ao pedido
def listarSabores(cursor):
    print("\n--- Sabores disponpíveis ---")
    cursor.execute("SELECT id, nome FROM Sabor")
    sabores = cursor.fetchall()
    for s in sabores:
        print(f"ID: {s[0]} - {s[1]}")

# função auxiliar para adicionar pizzas ao pedido
def adicionarPizzaAoPedido(cursor, id_pedido):
    listarTamanhosPizza(cursor)
    id_tamanho = int(input("Escolha o ID do tamanho da pizza: "))

    listarSabores(cursor)
    id_sabor = int(input("Escolha o ID do sabor da pizza: "))

    quantidade = int(input("Quantidade dessa pizza: "))

    sql = """
        INSERT INTO Pedido_Pizza (id_pedido, id_tamanho, id_sabor, quantidade)
        VALUES (%s, %s, %s, %s)
    """

    cursor.execute(sql, (id_pedido, id_tamanho, id_sabor, quantidade))
    print("Pizza adicionada ao pedido com sucesso!")

# Create
def criarPedido( id_cliente, endereco_entrega, valor_pagamento):

    conexao = None
    cursor = None
    
    try:
        conexao = conectar()
        if conexao is None:
            return
        
        cursor = conexao.cursor()
        status = "Aberto"

        # Data e horário atuais
        data_atual = datetime.now().date()
        hora_atual = datetime.now().time()

        sql = """
            INSERT INTO Pedido (id_cliente, valor_pagamento, status, endereco_entrega, data_pedido, horario_pedido)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (id_cliente, valor_pagamento, status, endereco_entrega, data_atual, hora_atual))

        id_pedido = cursor.lastrowid

        print("\nPedido criado com sucesso!")
        print(f"ID do pedido: {id_pedido}")

        if input("Deseja adicionar pizzas ao pedido agora? (s/n): ").lower() == "s":
            adicionarPizzaAoPedido(cursor, id_pedido)
            while input("\nAdicionar outra pizza ao pedido? (s/n): ").lower() == "s":
                adicionarPizzaAoPedido(cursor, id_pedido)

        conexao.commit()
        print("\nPedido finalizado com sucesso!")



    except Error as e:
        print("Erro ao criar pedido:", e)

    finally:
        cursor.close()
        conexao.close()

# Read
def listarPedidos():
    
    conexao = None
    cursor = None

    try:
        conexao = conectar()
        if conexao is None:
            return

        sql = """
            SELECT Pedido.id, Pessoa.nome, Pedido.status, Pedido.valor_pagamento, Pedido.data_pedido
            FROM Pedido
            INNER JOIN Cliente ON Pedido.id_cliente = Cliente.id
            INNER JOIN Pessoa ON Cliente.id_pessoa = Pessoa.id
        """

        cursor.execute(sql)
        pedidos = cursor.fetchall()

        print("\n--- Lista de pedidos ---")
        for p in pedidos:
            id_pedido = p[0]
            print(f"ID: {p[0]} | Cliente: {p[1]} | Status: {p[2]} | Valor: R${p[3]} | Data: {p[4]}")


            #sql para buscar os itens do pedido
            sql_itens = """
                SELECT P.tamanho, GROUP_CONCAT(S.nome SEPARATOR ', ') as sabores
                FROM Pedido_Pizza PP
                JOIN Pizza P ON PP.id_pizza = P.id
                JOIN Pizza_Sabor PS ON PP.id = PS.id_pedido_pizza
                JOIN Sabor S ON PS.id_sabor = S.id
                WHERE PP.id_pedido = %s
                GROUP BY PP.id
            """

            cursor.execute(sql_itens, (id_pedido,))
            itens = cursor.fetchall()

            if not itens:
                print("   (Nenhuma pizza adicionada)")
            else:
                
                contagem_pizzas = {}

                # Agrupa as pizzas iguais e conta a quantidade
                for tamanho, sabores in itens:
                    chave = (tamanho, sabores)
                    if chave in contagem_pizzas:
                        contagem_pizzas[chave] += 1
                    else:
                        contagem_pizzas[chave] = 1
                
                # Exibe as pizzas agrupadas pela quantidade
                for (tamanho, sabores), qtd in contagem_pizzas.items():
                    print(f"   -> {qtd}x Pizza {tamanho} - Sabores: {sabores}")

    except Error as e:
        print("Erro ao listar pedidos:", e)

    finally:
        cursor.close()
        conexao.close()

# Update
def atualizarPedido(novo_status, id_pedido):
    
    conexao = None
    cursor = None

    try:
        conexao = conectar()
        if conexao is None:
            return
        cursor = conexao.cursor()

        #localiza o status antes de realziar a atualização
        cursor.execute("SELECT status FROM Pedido WHERE id=%s", (id_pedido,))
        resultado = cursor.fetchone()
        status_antigo = resultado[0]

        if status_antigo == novo_status:
            print("O pedido já está com esse status.")
            return
        
        if status_antigo == "Entregue" or status_antigo == "Cancelado":
            print("Não é possível atualizar um pedido que já foi entregue ou cancelado.")
            return

        cursor.execute("SELECT id FROM Pedido WHERE id=%s", (id_pedido,))
        if cursor.fetchone() is None:
            print("Pedido não encontrado!")
            return

        cursor.execute("UPDATE Pedido SET status=%s WHERE id=%s", (novo_status, id_pedido))
        conexao.commit()

        print("\nStatus atualizado com sucesso!")

    except Error as e:
        print("Erro ao atualizar pedido:", e)

    finally:
        cursor.close()
        conexao.close()

# Delete
def deletarPedido(id_pedido):
    conexao = None
    cursor = None

    try:
        conexao = conectar()
        if conexao is None:
            return
        cursor = conexao.cursor()


        cursor.execute("SELECT id FROM Pedido WHERE id=%s", (id_pedido))
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