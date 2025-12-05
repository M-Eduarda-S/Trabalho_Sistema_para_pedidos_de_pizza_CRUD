from conexao import conectar
from mysql.connector import Error
from datetime import datetime  # coletar a data atual
from CRUD.cliente_CRUD import listarClientes


# Função auxiliar para listar tamanhos de pizza disponíveis
def listarTamanhosPizza(cursor):
    print("\n-> Tamanhos de pizzas disponíveis: ")
    cursor.execute("SELECT id, tamanho, valor_pizza FROM Pizza")
    tamanhos = cursor.fetchall()

    if not tamanhos:
        print("Nenhum tamanho de pizza cadastrado!")
        return None
    
    for t in tamanhos:
        print(f"ID: {t[0]} - Tamanho: {t[1]} (R$ {t[2]:.2f})")

    return tamanhos


# Função auxiliar para listar sabores disponíveis
def listarSabores(cursor):
    print("\n-> Sabores de pizzas disponíveis: ")
    cursor.execute("SELECT id, nome FROM Sabor")
    sabores = cursor.fetchall()

    if not sabores:
        print("Nenhum sabor de pizza cadastrado!")
        return None
    
    for s in sabores:
        print(f"ID: {s[0]} - {s[1]}")

    return sabores


# READ
def visualizarPedidos():
    print("\n-> Visualizar Pedidos: ")
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

        print("\n-> Lista de Pedido: ")
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
            
            # busca as pizzas do pedido
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
    conexao = None
    cursor = None

    try:
        conexao = conectar()
        if conexao is None:
            return

        cursor = conexao.cursor()
        
        sql = """
            SELECT Pedido.id, Pessoa.nome, Pedido.status, Pedido.valor_pagamento, Pedido.endereco_entrega, Pedido.data_pedido, Pedido.horario_pedido
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

        print("\n-> Lista de Pedidos: ")
        for p in pedidos:
            print(f"ID: {p[0]} | Cliente: {p[1]} | Status: {p[2]} | Valor: R$ {p[3]:.2f} | Endereço da entrega: {p[4]} | Data: {p[5]} | Horário: {p[6]}")

    except Error as e:
        print(f"Erro ao listar pedidos: {e}")

    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()



# Função auxiliar para adicionar pizza ao pedido
def adicionarPizzaAoPedido(cursor, id_pedido):
    print ("\n-> Adicionar Pizza ao Pedido: \n")
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
        
        quantidade_sabores = int(input("\nQuantos sabores você deseja na pizza? (1 ou 2): "))

        if quantidade_sabores not in (1, 2):
            print("Escolha inválida! Será considerado 1 sabor.")
            quantidade_sabores = 1

        lista_sabores = [] # para guardar os id de sabor escolhidos

        for i in range(quantidade_sabores):
            print(f"\nEscolha o sabor {i+1}:")
            id_sabor = int(input("ID do sabor: "))

            cursor.execute("SELECT id FROM Sabor WHERE id = %s", (id_sabor,))
            if not cursor.fetchone():
                print("Sabor da pizza não encontrado!")
                return
            
            lista_sabores.append(id_sabor)

        # insere o registro na tabela Pedido_Pizza
        cursor.execute(""" INSERT INTO Pedido_Pizza (id_pedido, id_pizza) VALUES (%s, %s) """, (id_pedido, id_pizza))
        id_pedido_pizza = cursor.lastrowid

        # insere o sabor na tabela Pizza_Sabor
        for id_sabor in lista_sabores:
            cursor.execute(""" INSERT INTO Pizza_Sabor (id_pedido_pizza, id_sabor) VALUES (%s, %s) """, (id_pedido_pizza, id_sabor))

        # pega o valor da pizza para somar no pedido
        cursor.execute("SELECT valor_pizza FROM Pizza WHERE id = %s", (id_pizza,))
        preco = cursor.fetchone()[0]

        cursor.execute("""UPDATE Pedido SET valor_pagamento = valor_pagamento + %s WHERE id = %s """, (preco, id_pedido))
        
        print("Pizza adicionada ao pedido com sucesso!")
        
        return float(preco) if preco is not None else 0.0 # retorna o valor da pizza adicionada

    except ValueError:
        print("Entrada inválida! Insira um número válido.")
        
    except Error as e:
        print(f"Erro ao adicionar pizza: {e}")


# CREATE
def adicionarPedido():
    conexao = None
    cursor = None
    
    try:
        conexao = conectar()
        if conexao is None:
            return
        
        cursor = conexao.cursor()
        
        print("-> Lista de Clientes: ")
        # Lista os clientes disponíveis
        listarClientes()
        
        # pede o ID do cliente
        id_cliente = input("\nID do cliente que está fazendo o pedido: ").strip()
        if not id_cliente.isdigit():
            print("ID inválido! Use apenas números.")
            return
        
        id_cliente = int(id_cliente)
        
        # verifica se o cliente existe
        cursor.execute("SELECT id FROM Cliente WHERE id = %s", (id_cliente,))
        if not cursor.fetchone():
            print("Cliente não encontrado!")
            return
        
        endereco_entrega = input("Endereço de entrega: ").strip()
        while not endereco_entrega:
            print("Endereço não pode estar vazio!")
            endereco_entrega = input("Endereço de entrega: ").strip()
        
        valor_pagamento = 0.0
        
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

        cursor.execute("SELECT valor_pagamento FROM Pedido WHERE id = %s", (id_pedido,))
        valor_final = cursor.fetchone()[0]

        print(f"\nPedido finalizado com sucesso! Valor total para pagamento: R${valor_final}")
        
    except Error as e:
        print(f"Erro ao criar pedido: {e}")
        if conexao:
            conexao.rollback()
    
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()


# UPDATE
def atualizarPedido(id_pedido):
    conexao = None
    cursor = None

    try:
        conexao = conectar()
        if conexao is None:
            return
        
        cursor = conexao.cursor()
        
        listarPedidos()
        
        # verifica se o pedido existe
        cursor.execute("SELECT id_cliente, endereco_entrega, valor_pagamento, status FROM Pedido WHERE id = %s", (id_pedido,))
        pedido = cursor.fetchone()
        
        if pedido is None:
            print("Pedido não encontrado!")
            return
        
        id_cliente_atual, endereco_atual, valor_atual, status_atual = pedido

        # opções para atualizar no pedido
        while True:
            print("\n-> Atualizar Pedido: ", id_pedido)
            print(f"Cliente atual: {id_cliente_atual}")
            print(f"Endereço atual: {endereco_atual}")
            print(f"Valor atual: R$ {valor_atual:.2f}")
            print(f"Status atual: {status_atual}")

            print("\nO que você quer atualizar?")
            print("1 - Status")
            print("2 - Cliente")
            print("3 - Endereço de entrega")
            print("4 - Valor do pagamento")
            print("5 - Adicionar pizzas ao pedido")
            print("0 - Sair")
            escolha = input("Escolha: ").strip()

            # atualizar o status
            if escolha == "1":
                if status_atual in ("Entregue", "Cancelado"):
                    print(f"Não é possível atualizar um pedido com status '{status_atual}'.")
                else:
                    print("\nSelecione o novo status:")
                    print("1 - Aberto")
                    print("2 - Em preparo")
                    print("3 - Saiu para entrega")
                    print("4 - Entregue")
                    print("5 - Cancelado")
                    opcao_status = input("Escolha: ").strip()

                    status_map = {
                        "1": "Aberto",
                        "2": "Em preparo",
                        "3": "Saiu para entrega",
                        "4": "Entregue",
                        "5": "Cancelado"
                    }
                    novo_status = status_map.get(opcao_status)

                    if not novo_status:
                        print("Opção inválida.")
                    elif novo_status == status_atual:
                        print("Pedido já possui esse status.")
                    else:
                        cursor.execute("UPDATE Pedido SET status = %s WHERE id = %s", (novo_status, id_pedido))
                        conexao.commit()
                        status_atual = novo_status
                        print("Status atualizado com sucesso.")

            # atualizar cliente
            elif escolha == "2":
                listarClientes()
                id_cliente = input("Novo ID do cliente (enter para manter): ").strip()

                if id_cliente == "":
                    print("ID mantido.")

                elif not id_cliente.isdigit():
                    print("ID inválido. Digite apenas números.")

                else:
                    novo_cliente = int(id_cliente)
                    cursor.execute("SELECT id FROM Cliente WHERE id = %s", (novo_cliente,))
                        
                    if not cursor.fetchone():
                        print("Cliente não encontrado.")

                    else:
                        cursor.execute("UPDATE Pedido SET id_cliente = %s WHERE id = %s", (novo_cliente, id_pedido))
                        conexao.commit()
                        id_cliente_atual = novo_cliente
                        print("Cliente do pedido atualizado.")

            # atualizar endereço de entrega
            elif escolha == "3":
                novo_endereco = input("Novo endereço de entrega (enter para manter): ").strip()

                if novo_endereco == "":
                    print("Endereço mantido.")
                else:
                    cursor.execute("UPDATE Pedido SET endereco_entrega = %s WHERE id = %s", (novo_endereco, id_pedido))
                    conexao.commit()
                    endereco_atual = novo_endereco
                    print("Endereço atualizado.")

            # atualizar valor de pagamento
            elif escolha == "4":
                novo_valor = input("Novo valor do pagamento (enter para manter): ").strip()

                if novo_valor == "":
                    print("Valor do pagamento mantido.")
                else:
                    try:
                        novo_valor_pagamento = float(novo_valor)

                        if novo_valor_pagamento <= 0:
                            print("Valor deve ser maior que zero.")

                        else:
                            cursor.execute("UPDATE Pedido SET valor_pagamento = %s WHERE id = %s", (novo_valor_pagamento, id_pedido))
                            conexao.commit()
                            valor_atual = novo_valor_pagamento
                            print("Valor atualizado.")

                    except ValueError:
                        print("Valor inválido.")

            # adicionar pizzas ao pedido
            elif escolha == "5":
                while True:
                    print("\n-> Gerenciar pizzas do pedido: ")
                    print("1 - Listar pizzas deste pedido")
                    print("2 - Adicionar pizza ao pedido")
                    print("0 - Voltar")
                    opcao_pizzas = input("Escolha: ").strip()

                    # listar pizzas
                    if opcao_pizzas == "1":
                        cursor.execute("""
                            SELECT PP.id, P.tamanho, P.valor_pizza, GROUP_CONCAT(S.nome SEPARATOR ', ') as sabores
                            FROM Pedido_Pizza PP
                            JOIN Pizza P ON PP.id_pizza = P.id
                            LEFT JOIN Pizza_Sabor PS ON PP.id = PS.id_pedido_pizza
                            LEFT JOIN Sabor S ON PS.id_sabor = S.id
                            WHERE PP.id_pedido = %s
                            GROUP BY PP.id
                        """, (id_pedido,))
                        pizzas = cursor.fetchall()

                        if not pizzas:
                            print("Nenhuma pizza adicionada a este pedido.")
                        else:
                            for r in pizzas:
                                print(f"ID_Pedido_Pizza: {r[0]} | Tamanho: {r[1]} | Valor: R$ {r[2]:.2f} | Sabores: {r[3]}")

                    # adicionar pizza ao pedido
                    elif opcao_pizzas == "2":
                        valor_adicionado = adicionarPizzaAoPedido(cursor, id_pedido)
                        conexao.commit()
                        if valor_adicionado: # só soma se retornar algo
                            valor_atual += valor_adicionado # atualiza a variável local sobre o valor

                    elif opcao_pizzas == "0":
                        break
                    else:
                        print("Opção inválida.")

            # sair do loop
            elif escolha == "0":
                print("Saindo da atualização de pedido...")
                break

            else:
                print("Opção inválida. Tente novamente.")

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
def deletarPedido(id_pedido):
    conexao = None
    cursor = None

    try:
        conexao = conectar()
        if conexao is None:
            return
        
        cursor = conexao.cursor()
        
        listarPedidos()
        
        # Verifica se o pedido existe
        cursor.execute("SELECT id, status FROM Pedido WHERE id = %s", (id_pedido,))
        pedido = cursor.fetchone()
        
        if pedido is None:
            print("Pedido não encontrado!")
            return
        
        status = pedido[1]
        
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