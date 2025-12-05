from conexao import conectar
from mysql.connector import Error
from datetime import datetime  # coletar a data atual
from CRUD.cliente_CRUD import listarClientes


# Função auxiliar para listar tamanhos de pizza disponíveis
def listarTamanhosPizza(cursor):
    print("\n--- Tamanhos disponíveis ---")
    cursor.execute("SELECT id, tamanho, valor_pizza FROM Pizza")
    tamanhos = cursor.fetchall()
    if not tamanhos:
        print("Nenhuma pizza cadastrada!")
        return None
    for t in tamanhos:
        print(f"ID: {t[0]} - Tamanho: {t[1]} (R$ {t[2]:.2f})")
    return tamanhos


# Função auxiliar para listar sabores disponíveis
def listarSabores(cursor):
    print("\n--- Sabores disponpíveis ---")
    cursor.execute("SELECT id, nome FROM Sabor")
    sabores = cursor.fetchall()
    if not sabores:
        print("Nenhum sabor cadastrado!")
        return None
    for s in sabores:
        print(f"ID: {s[0]} - {s[1]}")
    return sabores


# Função auxiliar para adicionar pizza ao pedido
def adicionarPizzaAoPedido(cursor, id_pedido):
    print ("\n--- Adicionar Pizza ao Pedido ---\n")
    tamanhos = listarTamanhosPizza(cursor)
    if not tamanhos:
        return
    
    try:
        id_pizza = int(input("\nEscolha o ID do tamanho da pizza: "))
        
       
        cursor.execute("SELECT id FROM Pizza WHERE id = %s", (id_pizza,))
        if not cursor.fetchone():
            print("Pizza não encontrada!")
            return
        
        sabores = listarSabores(cursor)
        if not sabores:
            return
        
        id_sabor = int(input("\nEscolha o ID do sabor da pizza: "))
        
        # Valida se o ID do sabor existe
        cursor.execute("SELECT id FROM Sabor WHERE id = %s", (id_sabor,))
        if not cursor.fetchone():
            print("Sabor não encontrado!")
            return
        
        # Insere o registro na tabela Pedido_Pizza
        sql_pedido_pizza = """
            INSERT INTO Pedido_Pizza (id_pedido, id_pizza)
            VALUES (%s, %s)
        """
        cursor.execute(sql_pedido_pizza, (id_pedido, id_pizza))
        id_pedido_pizza = cursor.lastrowid
        
        # Insere o sabor na tabela Pizza_Sabor
        sql_sabor = """
            INSERT INTO Pizza_Sabor (id_pedido_pizza, id_sabor)
            VALUES (%s, %s)
        """
        cursor.execute(sql_sabor, (id_pedido_pizza, id_sabor))
        
        print("Pizza adicionada ao pedido com sucesso!")
        
    except ValueError:
        print("Entrada inválida! Insira um número válido.")
    except Error as e:
        print(f"Erro ao adicionar pizza: {e}")


# CREATE
def adicionarPedido():
    """Cria um novo pedido com pizzas"""
    conexao = None
    cursor = None
    
    try:
        conexao = conectar()
        if conexao is None:
            return
        
        cursor = conexao.cursor()
        
        # Lista os clientes disponíveis
        listarClientes()
        
        # Solicita o ID do cliente
        try:
            id_cliente = int(input("\nID do cliente que está fazendo o pedido: "))
        except ValueError:
            print("ID inválido!")
            return
        
        # Valida se o cliente existe
        cursor.execute("SELECT id FROM Cliente WHERE id = %s", (id_cliente,))
        if not cursor.fetchone():
            print("Cliente não encontrado!")
            return
        
        endereco_entrega = input("Endereço de entrega: ").strip()
        if not endereco_entrega:
            print("Endereço não pode estar vazio!")
            return
        
        try:
            valor_pagamento = float(input("Valor do pagamento: R$ "))
            if valor_pagamento <= 0:
                print("Valor deve ser maior que zero!")
                return
        except ValueError:
            print("Valor inválido!")
            return
        
        status = "Aberto"
        data_atual = datetime.now().date()
        hora_atual = datetime.now().time()
        
        sql = """
            INSERT INTO Pedido (id_cliente, valor_pagamento, status, endereco_entrega, data_pedido, horario_pedido)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(sql, (id_cliente, valor_pagamento, status, endereco_entrega, data_atual, hora_atual))
        id_pedido = cursor.lastrowid
        
        print(f"\nPedido criado com sucesso! ID do pedido: {id_pedido}")
        
        # Adiciona pizzas ao pedido
        if input("Deseja adicionar pizzas ao pedido agora? (s/n): ").lower() == "s":
            adicionarPizzaAoPedido(cursor, id_pedido)
            while input("\nAdicionar outra pizza ao pedido? (s/n): ").lower() == "s":
                adicionarPizzaAoPedido(cursor, id_pedido)
        
        conexao.commit()
        print("\nPedido finalizado com sucesso!")
        
    except Error as e:
        print(f"Erro ao criar pedido: {e}")
        if conexao:
            conexao.rollback()
    
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()


# READ
def visualizarPedidos():
    print("\n--- Visualizar Pedidos  ---")
    conexao = None
    cursor = None

    try:
        conexao = conectar()
        if conexao is None:
            return

        cursor = conexao.cursor()
        
        sql = """
            SELECT Pedido.id, Pessoa.nome, Pedido.status, Pedido.valor_pagamento, Pedido.data_pedido, Pedido.horario_pedido
            FROM Pedido
            INNER JOIN Cliente ON Pedido.id_cliente = Cliente.id
            INNER JOIN Pessoa ON Cliente.id_pessoa = Pessoa.id
            ORDER BY Pedido.data_pedido DESC, Pedido.horario_pedido DESC
        """

        cursor.execute(sql)
        pedidos = cursor.fetchall()

        if not pedidos:
            print("\nNenhum pedido cadastrado!")
            return

        print("\n--- LISTA DE PEDIDOS ---")
        for p in pedidos:
            id_pedido = p[0]
            nome_cliente = p[1]
            status = p[2]
            valor = p[3]
            data = p[4]
            hora = p[5]
            
            print(f"\nID: {id_pedido} | Cliente: {nome_cliente}")
            print(f"Status: {status} | Valor: R$ {valor:.2f}")
            print(f"Data: {data} | Hora: {hora}")
            
            # Busca as pizzas do pedido
            sql_itens = """
                SELECT P.tamanho, P.valor_pizza, GROUP_CONCAT(S.nome SEPARATOR ', ') as sabores
                FROM Pedido_Pizza PP
                JOIN Pizza P ON PP.id_pizza = P.id
                JOIN Pizza_Sabor PS ON PP.id = PS.id_pedido_pizza
                JOIN Sabor S ON PS.id_sabor = S.id
                WHERE PP.id_pedido = %s
                GROUP BY PP.id
            """

            cursor.execute(sql_itens, (id_pedido,))
            itens = cursor.fetchall()

            if itens:
                print("Pizzas do pedido:")
                for tamanho, valor_pizza, sabores in itens:
                    print(f"  -> Pizza {tamanho} (R$ {valor_pizza:.2f}) - Sabor: {sabores}")
            else:
                print("  (Nenhuma pizza adicionada)")

    except Error as e:
        print(f"Erro ao listar pedidos: {e}")

    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()


def listarPedidos():
    print("\n--- Listar Pedidos ---")
    conexao = None
    cursor = None

    try:
        conexao = conectar()
        if conexao is None:
            return

        cursor = conexao.cursor()
        
        sql = """
            SELECT Pedido.id, Pessoa.nome, Pedido.status, Pedido.valor_pagamento, Pedido.data_pedido
            FROM Pedido
            INNER JOIN Cliente ON Pedido.id_cliente = Cliente.id
            INNER JOIN Pessoa ON Cliente.id_pessoa = Pessoa.id
            ORDER BY Pedido.data_pedido DESC
        """

        cursor.execute(sql)
        pedidos = cursor.fetchall()

        if not pedidos:
            print("\nNenhum pedido cadastrado!")
            return

        print("\n--- LISTA DE PEDIDOS ---")
        for p in pedidos:
            print(f"ID: {p[0]} | Cliente: {p[1]} | Status: {p[2]} | Valor: R$ {p[3]:.2f} | Data: {p[4]}")

    except Error as e:
        print(f"Erro ao listar pedidos: {e}")

    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()


# UPDATE
def atualizarPedido():
    print("\n--- Atualizar Pedido ---")
    conexao = None
    cursor = None

    try:
        conexao = conectar()
        if conexao is None:
            return
        
        cursor = conexao.cursor()
        
        listarPedidos()
        
        try:
            id_pedido = int(input("\nID do pedido que deseja atualizar: "))
        except ValueError:
            print("ID inválido!")
            return

        # Verifica se o pedido existe
        cursor.execute("SELECT status FROM Pedido WHERE id = %s", (id_pedido,))
        resultado = cursor.fetchone()
        
        if resultado is None:
            print("Pedido não encontrado!")
            return
        
        status_atual = resultado[0]
        
        # Valida se o pedido pode ser atualizado
        if status_atual == "Entregue":
            print("Não é possível atualizar um pedido que já foi entregue!")
            return
        
        if status_atual == "Cancelado":
            print("Não é possível atualizar um pedido que foi cancelado!")
            return

        print("\nSelecione o novo status:")
        print("1 - Aberto")
        print("2 - Em preparo")
        print("3 - Saiu para entrega")
        print("4 - Entregue")
        print("5 - Cancelado")

        try:
            opcao = input("\nEscolha a opção: ")
        except:
            print("Opção inválida!")
            return

        status_map = {
            "1": "Aberto",
            "2": "Em preparo",
            "3": "Saiu para entrega",
            "4": "Entregue",
            "5": "Cancelado"
        }

        novo_status = status_map.get(opcao)
        
        if novo_status is None:
            print("Opção inválida!")
            return
        
        if novo_status == status_atual:
            print(f"O pedido já possui o status '{novo_status}'!")
            return

        cursor.execute("UPDATE Pedido SET status = %s WHERE id = %s", (novo_status, id_pedido))
        conexao.commit()

        print(f"\nStatus do pedido {id_pedido} atualizado para '{novo_status}' com sucesso!")

    except Error as e:
        print(f"Erro ao atualizar pedido: {e}")
        if conexao:
            conexao.rollback()

    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()


# DELETE
def deletarPedido():
    print("\n--- Deletar Pedido ---")
    conexao = None
    cursor = None

    try:
        conexao = conectar()
        if conexao is None:
            return
        
        cursor = conexao.cursor()
        
        listarPedidos()
        
        try:
            id_pedido = int(input("\nID do pedido para deletar: "))
        except ValueError:
            print("ID inválido!")
            return

        # Verifica se o pedido existe
        cursor.execute("SELECT id, status FROM Pedido WHERE id = %s", (id_pedido,))
        resultado = cursor.fetchone()
        
        if resultado is None:
            print("Pedido não encontrado!")
            return
        
        status = resultado[1]
        
        # Aviso sobre pedidos entregues
        if status == "Entregue":
            print("\nAVISO: Este pedido já foi entregue!")
        
        confirmacao = input(f"\nTem certeza que deseja deletar o pedido {id_pedido}? (s/n): ").lower()
        
        if confirmacao != "s":
            print("Operação cancelada!")
            return

        cursor.execute("DELETE FROM Pedido WHERE id = %s", (id_pedido,))
        conexao.commit()

        print(f"\nPedido {id_pedido} deletado com sucesso!")

    except Error as e:
        print(f"Erro ao deletar pedido: {e}")
        if conexao:
            conexao.rollback()

    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()