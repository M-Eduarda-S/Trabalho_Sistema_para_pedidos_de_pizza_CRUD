from cliente_CRUD import criarCliente, adicionarTelefone, adicionarEndereco, listarClientes, atualizarCliente, deletarCliente

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
                id_cliente = input("\nID do Cliente: ")
                atualizarCliente(id_cliente)

            case "4":
                id_cliente = input("\nID do Cliente: ")
                deletarCliente(id_cliente)

            case "0":
                print("\nSaindo do CRUD CLIENTE...")
                break

            case _:
                print("\nOpção inválida!")
