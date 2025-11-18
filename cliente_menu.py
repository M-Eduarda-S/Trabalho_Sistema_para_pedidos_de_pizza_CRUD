from cliente_CRUD import criarCliente, adicionarTelefone, adicionarEndereco, listarClientes, atualizarCliente, deletarCliente
from conexao import conectar
from mysql.connector import Error

def cadastrar_cliente():
    conexao = conectar()
    if conexao is None:
        return
    
    try:
        cursor = conexao.cursor()

        print("\n--- CADASTRAR CLIENTE ---")
        nome = input("Nome: ")
        email = input("Email: ")

        cursor.execute("""
            INSERT INTO Pessoa (nome, email)
            VALUES (%s, %s)
        """, (nome, email))

        conexao.commit()
        id_pessoa = cursor.lastrowid
        print(f"Pessoa cadastrada! ID = {id_pessoa}")

        # Telefones opcionais
        opcao = input("Deseja adicionar telefone? (s/n): ").lower()

        if opcao == "s":
            adicionarTelefone(cursor, conexao, id_pessoa)

            # Loop para mais telefones
            while True:
                opcao = input("Gostaria de cadastrar outro telefone nesse mesmo cliente? (s/n): ").lower()
                if opcao != "s":
                    break
                adicionarTelefone(cursor, conexao, id_pessoa)

        # Endereços opcionais
        opcao = input("Deseja adicionar endereço? (s/n): ").lower()

        if opcao == "s":
            adicionarEndereco(cursor, conexao, id_pessoa)

            while True:
                opcao = input("Cadastrar outro endereço para esse cliente? (s/n): ").lower()
                if opcao != "s":
                    break
                adicionarEndereco(cursor, conexao, id_pessoa)

        # Criar Cliente
        cpf = input("CPF: ")

        cursor.execute("""
            INSERT INTO Cliente (id_pessoa, cpf)
            VALUES (%s, %s)
        """, (id_pessoa, cpf))

        conexao.commit()
        print("Cliente cadastrado com sucesso!\n")

    except Error as e:
        print("\nErro ao cadastrar Cliente:", e)

    finally:
        cursor.close()
        conexao.close()


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
                cadastrar_cliente()

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