from conexao import conectar
from mysql.connector import Error

#testar ainda
def listarPizzas():
    conexao = conectar()
    if conexao is None:
        return
    
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT id_pizza, nome, ingredientes, preco FROM Pizza")
        pizzas = cursor.fetchall()

        print("\n--- LISTA DE PIZZAS ---")
        for pizza in pizzas:
            print(f"ID: {pizza[0]}, Nome: {pizza[1]}, Ingredientes: {pizza[2]}, Preço: R${pizza[3]:.2f}")

    except Error as e:
        print("Erro ao listar pizzas:", e)

    finally:
        cursor.close()
        conexao.close()


def adicionarPizza(tamanho, sabor, valor_pizza):
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
        cursor.close()
        conexao.close()


def atualizarPizza():
    conexao = conectar()
    if conexao is None:
        return

    try:
        cursor = conexao.cursor()

        id_pizza = int(input("\nID da pizza a ser atualizada: "))
        nome = input("Novo nome da pizza: ")
        ingredientes = input("Novos ingredientes (separados por vírgula): ")
        preco = float(input("Novo preço da pizza: R$"))

        sql = "UPDATE Pizza SET nome = %s, ingredientes = %s, preco = %s WHERE id_pizza = %s"
        valores = (nome, ingredientes, preco, id_pizza)

        cursor.execute(sql, valores)
        conexao.commit()

        if cursor.rowcount > 0:
            print("\nPizza atualizada com sucesso!")
        else:
            print("\nNenhuma pizza encontrada com o ID fornecido.")

    except Error as e:
        print("Erro ao atualizar pizza:", e)

    finally:
        cursor.close()
        conexao.close()

def deletarPizza():
    conexao = conectar()
    if conexao is None:
        return

    try:
        cursor = conexao.cursor()

        id_pizza = int(input("\nID da pizza a ser deletada: "))

        sql = "DELETE FROM Pizza WHERE id_pizza = %s"
        valores = (id_pizza,)

        cursor.execute(sql, valores)
        conexao.commit()

        if cursor.rowcount > 0:
            print("\nPizza deletada com sucesso!")
        else:
            print("\nNenhuma pizza encontrada com o ID fornecido.")

    except Error as e:
        print("Erro ao deletar pizza:", e)

    finally:
        cursor.close()
        conexao.close()