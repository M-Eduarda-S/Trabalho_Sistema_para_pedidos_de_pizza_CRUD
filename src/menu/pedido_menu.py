from CRUD.pedido_CRUD import visualizarPedidos, adicionarPedido, deletarPedido, atualizarPedido, listarPedidos
from CRUD.cliente_CRUD import listarClientes

def menuPedido():
    while True:
        print("CRUD PEDIDO")
        print("1. Ver Pedidos")
        print("2. Adicionar Pedido")
        print("3. Deletar Pedido")
        print("4. Atualizar Pedido")
        print("0. Sair")

        opcao = input("\nSelecione uma opção: ")

        match opcao:
            case "1":
                visualizarPedidos()

            case "2":
                listarClientes()

                id_cliente = input("\nID do cliente que está fazendo o pedido: ")
                endereco_entrega = input("Endereço de entrega: ")
                valor_pagamento = float(input("Valor do pagamento (digite 0 se não tiver ainda): "))
                
                adicionarPedido(id_cliente, endereco_entrega, valor_pagamento)

            case "3":
                listarPedidos()
                id_pedido = input("\nID do pedido para deletar: ")
                deletarPedido(id_pedido)

            case "4":
                listarPedidos()
                id_pedido = input("\nID do pedido que deseja atualizar: ")
                StatusNovo = input("\Selecione o novo status: ")

                match StatusNovo:
                    case "1": novo_status = "Aberto"
                    case "2": novo_status = "Em preparo"
                    case "3": novo_status = "Saiu para entrega"
                    case "4": novo_status = "Entregue"
                    case "5": novo_status = "Cancelado"
                    case _:
                        print("Opção inválida.")
                        return
                    
                atualizarPedido(novo_status, id_pedido)

            case "0":
                print("Saindo do menu de pedidos...")
                break

            case _:
                print("\nOpção inválida!")