from CRUD.pizza_CRUD import listarPizzas, adicionarPizza, atualizarPizza, deletarPizza

def menuPizza():
    while True:
        print("\nCRUD PIZZA")
        print("1. Listar Pizzas")
        print("2. Adicionar Pizza")
        print("3. Atualizar Pizza")
        print("4. Deletar Pizza")
        print("0. Sair")

        opcao = input("\nSelecione uma opção: ")

        match opcao:
            case "1":
                listarPizzas()
                
            case "2":
                tamanho = input("Tamanho da pizza: ").upper()
                valor = float(input("Valor da pizza: R$"))
                adicionarPizza(tamanho, valor)

            case "3":
                id_pizza = input("\nID do Pedido: ").strip()
                if id_pizza.isdigit():
                    atualizarPizza(int(id_pizza))
                else:
                    print("ID inválido! Use apenas números.")

            case "4":
                id_pizza = input("\nID do Pedido: ").strip()
                if id_pizza.isdigit():
                    deletarPizza(int(id_pizza))
                else:
                    print("ID inválido! Use apenas números.")

            case "0":
                print("Saindo do menu de pizzas...")
                break

            case _:
                print("\nOpção inválida!")