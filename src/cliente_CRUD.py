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
def adicionarTelefone(cursor, id_pessoa):
    numero = input("Número: ")
    
    print("\nSelecione o tipo de telefone:")
    print("1 - Fixo")
    print("2 - Celular")
    print("3 - Comercial")

    while True:
        opcao = input("Escolha (1, 2 ou 3): ")
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

    print("Telefone registrado!")


# Adiconar o endereço para o cliente
def adicionarEndereco(cursor, id_pessoa):
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

    print("Endereço cadastrado!")


# CREATE
def criarCliente(nome, email, cpf):
    conexao = None
    cursor = None

    try:
        conexao = conectar()
        if conexao is None:
            print("Erro ao conectar ao banco")
            return
        
        cursor = conexao.cursor()

        # Inserir Pessoa
        sql_pessoa = "INSERT INTO Pessoa (nome, email) VALUES (%s, %s)"
        cursor.execute(sql_pessoa, (nome, email))
        id_pessoa = cursor.lastrowid

        # Inserir Cliente
        sql_cliente = "INSERT INTO Cliente (id_pessoa, cpf) VALUES (%s, %s)"
        cursor.execute(sql_cliente, (id_pessoa, cpf))
        id_cliente = cursor.lastrowid

        if input("Deseja adicionar telefone? (s/n): ").lower() == "s":
            adicionarTelefone(cursor, id_pessoa)
            while input("\nAdicionar outro telefone? (s/n): ").lower() == "s":
                adicionarTelefone(cursor, id_pessoa)

        if input("\nDeseja adicionar endereço? (s/n): ").lower() == "s":
            adicionarEndereco(cursor, id_pessoa)
            while input("\nAdicionar outro endereço? (s/n): ").lower() == "s":
                adicionarEndereco(cursor, id_pessoa)

        conexao.commit()
        print("\nCliente criado com sucesso! ID:", id_cliente)
        return id_pessoa  # ID para cadastrar telefone e endereço

    except Error as e:
        print("Erro ao cadastrar cliente:", e)

    finally:
        if cursor: # para evitar erro se não existir
            cursor.close()
        if conexao:
            conexao.close()

# READ
def listarClientes():
    conexao = None
    cursor = None

    try:
        conexao = conectar()
        if conexao is None:
            print("Erro ao conectar ao banco")
            return
        
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
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()


# UPDATE
def atualizarCliente(id_cliente):
    conexao = None
    cursor = None

    try:
        conexao = conectar()
        if conexao is None:
            print("Erro ao conectar ao banco")
            return
        
        cursor = conexao.cursor()

        # Buscar o ID da pessoa
        cursor.execute("SELECT id_pessoa FROM Cliente WHERE id = %s", (id_cliente,))
        dados = cursor.fetchone() # pega um resultado da última consulta SELECT

        if not dados:
            print("Cliente não encontrado!")
            return

        id_pessoa = dados[0]

        nome = input("Novo nome (enter para manter o dado anterior): ")
        if nome:
            cursor.execute("UPDATE Pessoa SET nome=%s WHERE id=%s", (nome, id_pessoa))

        email = input("Novo email (enter para manter o dado anterior): ")
        if email:
            cursor.execute("UPDATE Pessoa SET email=%s WHERE id=%s", (email, id_pessoa))

        cpf = input("Novo CPF (enter para manter o dado anterior): ")
        if cpf:
            cursor.execute("UPDATE Cliente SET cpf=%s WHERE id=%s", (cpf, id_cliente))

        opcao = input("\nDeseja atualizar os telefones do cliente? (s/n): ").lower()

        if opcao == "s":
            cursor.execute("SELECT id, numero, tipo FROM Telefone_pessoa WHERE id_pessoa=%s", (id_pessoa,))
            telefones = cursor.fetchall()

            print("\nTelefones atuais desse Cliente:")
            for f in telefones:
                print(f"{f[0]} - {f[1]} ({f[2]})")

            print("\n1 - Adicionar telefone")
            print("2 - Remover telefone")
            print("3 - Editar telefone existente")
            print("Enter - cancelar")

            opcaoTelefone = input("Escolha: ")

            if opcaoTelefone == "1":
                adicionarTelefone(cursor, id_pessoa)

            elif opcaoTelefone == "2":
                id_telefone = input("ID do telefone para remover: ")
                cursor.execute("DELETE FROM Telefone_pessoa WHERE id=%s", (id_telefone,))
                conexao.commit()
                print("Telefone removido!")

            elif opcaoTelefone == "3":
                id_telefone = input("ID do telefone para editar: ")
                novo_numero = input("Novo número (enter para manter o dado anterior): ")
                print("\nNovo tipo de telefone:")
                print("1 - Fixo")
                print("2 - Celular")
                print("3 - Comercial")
                print("Enter - manter o tipo anterior")
                escolha_tipo = input("Escolha: ")

                novo_tipo = None
                if escolha_tipo == "1":
                    novo_tipo = "Fixo"
                elif escolha_tipo == "2":
                    novo_tipo = "Celular"
                elif escolha_tipo == "3":
                    novo_tipo = "Comercial"
                elif escolha_tipo == "":
                    novo_tipo = None  # Mantém o tipo anterior
                else:
                    print("Opção inválida. Vai ser mantido o tipo anterior.")

                if novo_numero:
                    cursor.execute("UPDATE Telefone_pessoa SET numero=%s WHERE id=%s", (novo_numero, id_telefone))

                if novo_tipo:
                    cursor.execute("UPDATE Telefone_pessoa SET tipo=%s WHERE id=%s", (novo_tipo, id_telefone))

                print("Telefone atualizado!")
            

        opcao = input("\nDeseja atualizar o endereço? (s/n): ").lower()

        if opcao == "s":
            cursor.execute("""SELECT id, rua, numero, cep FROM Endereco_pessoa WHERE id_pessoa=%s""", (id_pessoa,))
            enderecos = cursor.fetchall()

            print("\nEndereços atuais desse Cliente:")
            for e in enderecos:
                print(f"{e[0]} - {e[1]}, {e[2]} (CEP {e[3]})")

            print("\n1 - Adicionar endereço")
            print("2 - Remover endereço")
            print("3 - Editar endereço existente")
            print("Enter - cancelar")
            opcaoEndereco = input("Escolha: ")

            if opcaoEndereco == "1":
                adicionarEndereco(cursor, id_pessoa)

            elif opcaoEndereco == "2":
                id_endereco = input("ID do endereço para remover: ")
                cursor.execute("DELETE FROM Endereco_pessoa WHERE id=%s", (id_endereco,))
                conexao.commit()
                print("Endereço removido!")

            elif opcaoEndereco == "3":
                id_endereco = input("ID do endereço para editar: ")
                nova_rua = input("Nova rua (enter para manter o dado anterior): ")
                novo_numero = input("Novo número (enter para manter o dado anterior): ")
                novo_cep = input("Novo CEP (enter para manter o dado anterior): ")
                novo_logradouro = input("Novo logradouro (enter para manter o dado anterior): ")
                novo_complemento = input("Novo complemento (enter para manter o dado anterior): ")

                if nova_rua:
                    cursor.execute("UPDATE Endereco_pessoa SET rua=%s WHERE id=%s", (nova_rua, id_endereco))

                if novo_numero:
                    cursor.execute("UPDATE Endereco_pessoa SET numero=%s WHERE id=%s", (novo_numero, id_endereco))

                if novo_cep:
                    cursor.execute("UPDATE Endereco_pessoa SET cep=%s WHERE id=%s", (novo_cep, id_endereco))

                if novo_logradouro:
                    cursor.execute("UPDATE Endereco_pessoa SET logradouro=%s WHERE id=%s", (novo_logradouro, id_endereco))

                if novo_complemento:
                    cursor.execute("UPDATE Endereco_pessoa SET complemento=%s WHERE id=%s", (novo_complemento, id_endereco))

                print("Endereço atualizado!")


        conexao.commit()
        print("\nCliente atualizado com sucesso!")

    except Error as e:
        print("Erro ao atualizar cliente:", e)

    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()


# DELETE
def deletarCliente(id_cliente):
    conexao = None
    cursor = None

    try:
        conexao = conectar()
        if conexao is None:
            print("Erro ao conectar ao banco")
            return
        
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
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()