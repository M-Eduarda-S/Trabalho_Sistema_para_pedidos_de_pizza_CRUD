from cliente_CRUD import criarCliente, listarClientes, atualizarCliente, deletarCliente
from pedido_CRUD import criarPedido, listarPedidos, atualizarPedido, deletarPedido
from pizza_CRUD import criarPizza, listarPizzas, atualizarPizza, deletarPizza

def menuCliente():
    while True:
        print("\nCRUD CLIENTE")
        print("1 - Cadastrar cliente")
        print("2 - Listar clientes")
        print("3 - Atualizar cliente")
        print("4 - Deletar cliente")
        print("0 - Sair")
        
        opcao = input("Escolha: ")

        match opcao:
            case "1":
                nome = input("Nome: ")
                email = input("Email: ")
                cpf = input("CPF: ")
                numero = input("Número da casa: ")
                rua = input("Rua: ")
                cep = input("CEP: ")
                logradouro = input("Logradouro: ")
                complemento = input("Complemento: ")
                id_cidade = input("ID da Cidade: ")

                telefones = []
                while True:
                    add = input("Adicionar telefone? (s/n): ").lower()

                    if add == "n":
                        break
                    
                    numero_tel = input("Número do telefone: ")
                    print("Tipo:")
                    print("1 - Fixo")
                    print("2 - Celular")
                    print("3 - Comercial")
                    tipo_op = input("Escolha: ")

                    tipo_map = {"1": "Fixo", "2": "Celular", "3": "Comercial"}
                    tipo_tel = tipo_map.get(tipo_op, "Celular")

                    telefones.append((numero_tel, tipo_tel))

                criarCliente(nome, email, cpf, numero, rua, cep, logradouro, complemento, id_cidade, telefones)

            case "2":
                listarClientes()

            case "3":
                id_cliente = input("ID do Cliente: ")
                atualizarCliente(id_cliente)

            case "4":
                id_cliente = input("ID do Cliente: ")
                deletarCliente(id_cliente)

            case "0":
                print("Saindo do CRUD CLIENTE...")
                break

            case _:
                print("Opção inválida!")

def menuPedido():
    print()

def menuPizza():
    print()

def menuPrincipal():
    while True:
        print("\n   SISTEMA DE PEDIDOS DE PIZZA COM CRUD\n")
        print("1 - Clientes")
        print("2 - Pedidos")
        print("3 - Pizzas")
        print("4 - Créditos")
        print("0 - Sair")

        opcao = input("\nEscolha a opção: ")

        match opcao:
            case "1":
                menuCliente()

            case "2":
                menuPedido()

            case "3":
                menuPizza()

            case "4":
                print("\n-> Créditos:")
                print("\nDesenvolvedores: Maria Eduarda Santos e Yasmin Tarnovski Faccin.")
                print("\nDisciplina: Banco de Dados I")
                print("\Professor: Maurício Pasetto de Freitas\n\n")

            case "0":
                print("Saindo do sistema...")
                break

            case _:
                print("Opção inválida!")

# Para ir ao menu escolher a entidade e seu CRUD
if __name__ == "__main__":
    menuPrincipal()