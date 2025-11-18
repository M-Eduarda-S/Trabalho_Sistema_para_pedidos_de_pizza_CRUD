from conexao import conectar

from mysql.connector import Error

# CREATE
def criarCliente(nome, email, cpf, numero, rua, cep, logradouro, complemento, id_cidade, telefones):
    conexao = conectar()
    if conexao is None:
        return
    
    try:
        cursor = conexao.cursor()

        # Inserir em Pessoa
        sql_pessoa = "INSERT INTO Pessoa (nome, email) VALUES (%s, %s)"
        cursor.execute(sql_pessoa, (nome, email))
        id_pessoa = cursor.lastrowid

        # Inserir em Cliente
        sql_cliente = "INSERT INTO Cliente (id_pessoa, cpf) VALUES (%s, %s)"
        cursor.execute(sql_cliente, (id_pessoa, cpf))

        # Inserir em Endereco_pessoa
        sql_endereco = """
            INSERT INTO Endereco_pessoa (id_pessoa, id_cidade, numero, cep, rua, logradouro, complemento) VALUES 
            (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql_endereco, (
            id_pessoa, id_cidade, numero, cep, rua, logradouro, complemento
        ))

        # Inserir Telefone_pessoa (pode ser 1 ou vários telefones)
        sql_telefone = """
            INSERT INTO Telefone_pessoa (id_pessoa, numero, tipo) VALUES 
            (%s, %s, %s)
        """

        for tel in telefones:
            numero_tel, tipo_tel = tel
            cursor.execute(sql_telefone, (id_pessoa, numero_tel, tipo_tel))

        conexao.commit()
        print("Cliente cadastrado com sucesso!")

    except Exception as e:
        print("Erro ao cadastrar cliente:", e)

    finally:
        cursor.close()
        conexao.close()


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
        for row in cursor.fetchall():
            print(row)

    except Exception as e:
        print("Erro ao listar:", e)

    finally:
        cursor.close()
        conexao.close()


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
        print("Erro ao remover:", e)

    finally:
        cursor.close()
        conexao.close()