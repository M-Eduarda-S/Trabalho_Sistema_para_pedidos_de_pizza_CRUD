from CRUD.pedido_CRUD import listarPedidos, adicionarPedido, deletarPedido, atualizarPedido

def menuPedido():
    while True:
        print("\nCRUD PEDIDO")
        print("1. Listar Pedidos")
        print("2. Adicionar Pedido")
        print("3. Atualizar Pedido")
        print("4. Deletar Pedido")
        print("0. Sair")

        opcao = input("\nSelecione uma opção: ").strip()

        match opcao:
            case "1":
                listarPedidos()

            case "2":
                adicionarPedido()

            case "3":
                id_pedido = input("\nID do Pedido: ").strip()
                if id_pedido.isdigit():
                    atualizarPedido(int(id_pedido))
                else:
                    print("ID inválido! Use apenas números.")

            case "4":
                id_pedido = input("\nID do Pedido: ").strip()
                if id_pedido.isdigit():
                    deletarPedido(int(id_pedido))
                else:
                    print("ID inválido! Use apenas números.")

            case "0":
                print("Saindo do menu de pedidos...")
                break

            case _:
                print("\nOpção inválida! Tente novamente.")