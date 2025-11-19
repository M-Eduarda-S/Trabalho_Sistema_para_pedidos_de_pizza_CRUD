# Disciplina: Banco de Dados I
# Professor: Maurício Pasetto de Freitas
# Nomes: Maria Eduarda Santos e Yasmin Tarnovski Faccin.

from cliente_menu import menuCliente

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

            # case "2":
            #     menuPedido()

            # case "3":
            #     menuPizza()

            case "4":
                print("\n-> Créditos:")
                print("\nDesenvolvedores: Maria Eduarda Santos e Yasmin Tarnovski Faccin.")
                print("Disciplina: Banco de Dados I")
                print("Professor: Maurício Pasetto de Freitas.\n")

            case "0":
                print("\nSaindo do sistema...")
                break

            case _:
                print("\nOpção inválida!")

# Para ir ao menu escolher a entidade e seu CRUD
if __name__ == "__main__":
    menuPrincipal()