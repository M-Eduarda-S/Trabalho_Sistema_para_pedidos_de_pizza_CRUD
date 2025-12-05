from CRUD.pedido_CRUD import visualizarPedidos, adicionarPedido, deletarPedido, atualizarPedido, listarPedidos

def menuPedido():
    while True:
        print("\n" + "="*40)
        print("CRUD PEDIDO")
        print("="*40)
        print("1. Visualizar Pedidos")
        print("2. Adicionar Pedido")
        print("3. Atualizar Pedido")
        print("4. Deletar Pedido")
        print("0. Sair")
        print("="*40)

        opcao = input("\nSelecione uma opção: ").strip()

        match opcao:
            case "1":
                visualizarPedidos()

            case "2":
                print("\n--- Adicionar Novo Pedido ---")
                adicionarPedido()

            case "3":
                print("\n--- Atualizar Pedido ---")
                atualizarPedido()

            case "4":
                print("\n--- Deletar Pedido ---")
                deletarPedido()

            case "0":
                print("Saindo do menu de pedidos...")
                break

            case _:
                print("\nOpção inválida! Tente novamente.")