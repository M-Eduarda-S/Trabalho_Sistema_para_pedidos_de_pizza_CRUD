from conexao import conectar
from mysql.connector import Error

# Read
def listarPizzas():
    conexao = conectar()
    if conexao is None:
        return
    
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT id, tamanho, valor_pizza FROM Pizza")
        pizzas = cursor.fetchall()

        for pizza in pizzas:
            print(f"ID: {pizza[0]}, Tamanho: {pizza[1]}, Preço: R${pizza[2]:.2f}")

    except Error as e:
        print("Erro ao listar pizzas:", e)

    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()


# Create
def adicionarPizza(tamanho, valor_pizza):
    conexao = conectar()
    if conexao is None:
        return

    try:
        cursor = conexao.cursor()

        sql = "INSERT INTO Pizza (tamanho, valor_pizza) VALUES (%s, %s)"
        valores = (tamanho, valor_pizza)
        cursor.execute(sql, valores)
        conexao.commit()

        print("\nPizza adicionada com sucesso! ID da pizza:", cursor.lastrowid)

    except Error as e:
        print("Erro ao adicionar pizza:", e)

    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()


# Update
def atualizarPizza(id_pizza):
    conexao = conectar()
    if conexao is None:
        return

    try:
        cursor = conexao.cursor()

        # verifica se tem
        cursor.execute("SELECT tamanho, valor_pizza FROM Pizza WHERE id = %s", (id_pizza,))
        dados = cursor.fetchone()

        if not dados:
            print("Nenhuma pizza encontrada com esse ID.")
            return

        tamanho_atual, preco_atual = dados

        # mostra os tamanhos
        cursor.execute("SELECT DISTINCT tamanho FROM Pizza ORDER BY tamanho")
        tamanhos = cursor.fetchall()

        print("\nTamanhos de pizzas disponíveis no banco:")
        for t in tamanhos:
            print("-", t[0])

        print("\nTamanho atual da pizza:", tamanho_atual)
        novo_tamanho = input("Novo tamanho da pizza (Enter para manter): ").upper()

        if novo_tamanho == "":
            novo_tamanho = tamanho_atual

        # preço da pizza
        print(f"Preço atual da pizza: R${preco_atual:.2f}")
        preco = input("Novo preço da pizza (Enter para manter): R$")

        if preco == "":
            preco = preco_atual
        else:
            preco = float(preco)

        sql = "UPDATE Pizza SET tamanho = %s, valor_pizza = %s WHERE id = %s"
        valores = (novo_tamanho, preco, id_pizza)
        cursor.execute(sql, valores)
        conexao.commit()

        print("\nPizza atualizada com sucesso!")

    except Error as e:
        print("Erro ao atualizar pizza:", e)

    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()
        

# Delete
def deletarPizza(id_pizza):
    conexao = conectar()
    if conexao is None:
        return

    try:
        cursor = conexao.cursor()

        cursor.execute("DELETE FROM Pizza WHERE id = %s", (id_pizza,))
        conexao.commit()

        # verifica se deletou
        if cursor.rowcount == 0:
            print("Pizza não encontrada.")
            return

        print("Pizza deletada com sucesso!")

    except Error as e:
        print("Erro ao deletar pizza:", e)

    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()