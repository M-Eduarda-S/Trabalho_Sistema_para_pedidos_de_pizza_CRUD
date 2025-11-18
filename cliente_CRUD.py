from conexao import conectar
from mysql.connector import Error

# Lista as cidades para poder ligar ao endereço do cliente
def listaCidades(cursor):
    print("\n--- LISTA DE CIDADES ---")
    
    cursor.execute("""
        SELECT Cidade.id, Cidade.nome, Estado.sigla 
        FROM Cidade 
        JOIN Estado ON Cidade.id_estado = Estado.id
    """)

    cidades = cursor.fetchall()
    for cidade in cidades:
        print(f"{cidade[0]} - {cidade[1]} ({cidade[2]})")


# Adicionar telefone para o cliente
def adicionarTelefone(cursor, conexao, id_pessoa):
    numero = input("Número: ")
    
    print("\nSelecione o tipo de telefone:")
    print("1 - Fixo")
    print("2 - Celular")
    print("3 - Comercial")

    while True:
        opcao = input("Escolha (1/2/3): ")
        if opcao == "1":
            tipo = "Fixo"
            break
        elif opcao == "2":
            tipo = "Celular"
            break
        elif opcao == "3":
            tipo = "Comercial"
            break
        else:
            print("Opção inválida. Tente novamente.")

    # o cursor envia comandos SQL para o MySQL, assim da para conversar com o BD
    cursor.execute("""
        INSERT INTO Telefone_pessoa (id_pessoa, numero, tipo)
        VALUES (%s, %s, %s)
    """, (id_pessoa, numero, tipo))

    conexao.commit()
    print("Telefone registrado!")


# Adiconar o endereço para o cliente
def adicionarEndereco(cursor, conexao, id_pessoa):
    listaCidades(cursor)

    id_cidade = int(input("Escolha o ID da cidade: "))
    numero = int(input("Número da residência: "))
    cep = input("CEP: ")
    rua = input("Rua: ")

    logradouro = input("Logradouro (deixe vazio se não querer preencher): ")
    if logradouro == "":
        logradouro = None

    complemento = input("Complemento (deixe vazio se não querer preencher): ")
    if complemento == "":
        complemento = None

    cursor.execute("""
        INSERT INTO Endereco_pessoa (id_pessoa, id_cidade, numero, cep, rua, logradouro, complemento)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (id_pessoa, id_cidade, numero, cep, rua, logradouro, complemento))

    conexao.commit()
    print("Endereço cadastrado!")


# CREATE
def criarCliente(nome, email, cpf, enderecos, telefones):
    conexao = conectar()
    if conexao is None:
        return
    
    try:
        cursor = conexao.cursor()

        # Inserir Pessoa
        sql_pessoa = "INSERT INTO Pessoa (nome, email) VALUES (%s, %s)"
        cursor.execute(sql_pessoa, (nome, email))
        id_pessoa = cursor.lastrowid

        # Inserir Cliente
        sql_cliente = "INSERT INTO Cliente (id_pessoa, cpf) VALUES (%s, %s)"
        cursor.execute(sql_cliente, (id_pessoa, cpf))

        # Pode criar vários endereços
        sql_endereco = """
            INSERT INTO Endereco_pessoa 
            (id_pessoa, id_cidade, numero, cep, rua, logradouro, complemento)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        for (id_cidade, numero, cep, rua, logradouro, complemento) in enderecos:
            cursor.execute(sql_endereco, (
                id_pessoa, id_cidade, numero, cep, rua, logradouro, complemento
            ))

        # Pode criar vários telefones
        sql_telefone = """
            INSERT INTO Telefone_pessoa (id_pessoa, numero, tipo)
            VALUES (%s, %s, %s)
        """

        for tel_num, tel_tipo in telefones:
            cursor.execute(sql_telefone, (id_pessoa, tel_num, tel_tipo))

        conexao.commit()
        print("Cliente cadastrado com sucesso!")

    except Error as e:
        print("Erro ao cadastrar cliente:", e)

    finally:
        cursor.close()
        conexao.close()


# READ
def listarClientes():
    conexao = conectar()
    if conexao is None:
        return
    
    try:
        cursor = conexao.cursor()
        sql = """
            SELECT Cliente.id, Pessoa.nome, Cliente.cpf 
            FROM Cliente
            INNER JOIN Pessoa ON Pessoa.id = Cliente.id_pessoa
        """
        cursor.execute(sql)
        for row in cursor.fetchall(): # pega todos os resultados da última consulta SELECT
            print(row)

    except Exception as e:
        print("Erro ao listar clientes:", e)

    finally:
        cursor.close()
        conexao.close()


# UPDATE
def atualizarCliente(id_cliente):
    conexao = conectar()
    if conexao is None:
        return
    
    try:
        cursor = conexao.cursor()

        # Buscar o ID da pessoa
        cursor.execute("SELECT id_pessoa FROM Cliente WHERE id = %s", (id_cliente,))
        dados = cursor.fetchone() # pega um resultado da última consulta SELECT

        if not dados:
            print("Cliente não encontrado!")
            return

        id_pessoa = dados[0]

        nome = input("Novo nome (envie vazio para manter a informação): ")
        email = input("Novo email (envie vazio para manter a informação): ")

        if nome != "":
            cursor.execute("UPDATE Pessoa SET nome=%s WHERE id=%s", (nome, id_pessoa))

        if email != "":
            cursor.execute("UPDATE Pessoa SET email=%s WHERE id=%s", (email, id_pessoa))

        cpf = input("Novo CPF (envie vazio para manter a informação): ")

        if cpf != "":
            cursor.execute("UPDATE Cliente SET cpf=%s WHERE id=%s", (cpf, id_cliente))

        opc = input("\nDeseja atualizar os telefones do cliente? *deleta todos os telefones ligados a esse cliente (s/n): ").lower()

        if opc == "s":
            # Deleta todos os telefones atuais
            cursor.execute("DELETE FROM Telefone_pessoa WHERE id_pessoa=%s", (id_pessoa,))

            adicionarTelefone(cursor, conexao, id_pessoa)

            # Loop de mais telefones
            while True:
                mais = input("Cadastrar outro telefone para esse cliente? (s/n): ").lower()
                if mais != "s":
                    break
                adicionarTelefone(cursor, conexao, id_pessoa)

        opc = input("\nDeseja atualizar o endereço? *deleta todos os endereços ligados a esse cliente(s/n): ").lower()

        if opc == "s":
            # Apagar endereço antigo
            cursor.execute("DELETE FROM Endereco_pessoa WHERE id_pessoa=%s", (id_pessoa,))

            adicionarEndereco(cursor, conexao, id_pessoa)

            # Loop de mais endereços
            while True:
                mais = input("Cadastrar outro endereço para esse cliente? (s/n): ").lower()
                if mais != "s":
                    break
                adicionarEndereco(cursor, conexao, id_pessoa)


        conexao.commit()
        print("\nCliente atualizado com sucesso!")

    except Error as e:
        print("Erro ao atualizar cliente:", e)

    finally:
        cursor.close()
        conexao.close()


# DELETE
def deletarCliente(id_cliente):
    conexao = conectar()
    if conexao is None:
        return
    
    try:
        cursor = conexao.cursor()

        # acha id_pessoa
        cursor.execute("SELECT id_pessoa FROM Cliente WHERE id=%s", (id_cliente,))
        result = cursor.fetchone()

        if not result:
            print("Cliente não encontrado.")
            return

        id_pessoa = result[0]

        # deletar a pessoa (e tudo dela)
        cursor.execute("DELETE FROM Pessoa WHERE id=%s", (id_pessoa,))
        conexao.commit()

        print("Cliente removido com sucesso!")

    except Exception as e:
        print("Erro ao remover cliente:", e)

    finally:
        cursor.close()
        conexao.close()