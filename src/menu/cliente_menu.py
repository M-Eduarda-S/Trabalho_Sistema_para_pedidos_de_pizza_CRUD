from CRUD.cliente_CRUD import criarCliente, listarClientes, atualizarCliente, deletarCliente

def menuCliente():
    while True:
        print("\nCRUD CLIENTE")
        print("1 - Cadastrar cliente")
        print("2 - Listar clientes")
        print("3 - Atualizar cliente")
        print("4 - Deletar cliente")
        print("0 - Sair")

        opcao = input("\nEscolha: ")

        match opcao:
            case "1":
                nome = input("Nome: ")
                email = input("Email: ")
                cpf = input("CPF: ")

                criarCliente(nome, email, cpf)

            case "2":
                listarClientes()

            case "3":
                id_cliente = input("\nID do Pedido: ").strip()
                if id_cliente.isdigit():
                    atualizarCliente(int(id_cliente))
                else:
                    print("ID inválido! Use apenas números.")

            case "4":
                id_cliente = input("\nID do Pedido: ").strip()
                if id_cliente.isdigit():
                    deletarCliente(int(id_cliente))
                else:
                    print("ID inválido! Use apenas números.")

            case "0":
                print("\nSaindo do CRUD CLIENTE...")
                break

            case _:
                print("\nOpção inválida!")
