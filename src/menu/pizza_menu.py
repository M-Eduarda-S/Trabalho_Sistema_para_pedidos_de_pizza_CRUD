from CRUD.pizza_CRUD import adicionarPizza, listarPizzas, atualizarPizza, deletarPizza

def menuPizza():
    while True:
        print("CRUD PIZZA")
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
                tamanho = input("Tamanho da pizza (P, M, G): ")
                sabor = input("Sabor da pizza: ")
                valor = float(input("Valor da pizza: "))
              
                adicionarPizza( tamanho, sabor, valor)

            case "3":
                listarPizzas()
                print("-" * 20)
                atualizarPizza()

            case "4":
                listarPizzas()
                print("-" * 20)
                deletarPizza()

            case "0":
                print("Saindo do menu de pizzas...")
                break

            case _:
                print("\nOpção inválida!")