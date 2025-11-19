# 🧾 Sistema de Pedidos de Pizza — CRUD em Python

Projeto desenvolvido para a disciplina **Banco de Dados I**, consistindo em um sistema CRUD feito em **Python** que manipula três tabelas principais e relacionadas utilizando um banco de dados **MySQL** para armazenamento e gerenciamento das informações.<br><br>

**Professor que passou o projeto**: Maurício Pasetto de Freitas.<br>
**Desenvolvedoras do projeto**: Maria Eduarda Santos e Yasmin Tarnovski Faccin.<br>

## Como executar o projeto
### Instalar dependências
Se esta for a sua primeira vez executando o projeto, instale o conector Python–MySQL:

```bash
pip install mysql-connector-python
```
<br>Se estiver utilizando um ambiente virtual (opcional), ative-o:
```
.venv\Scripts\activate
```
### Rodar o projeto
Para rodar o projeto, digite no terminal:
```
python main.py
```

### Acessar o MySQL local
Para acessar o banco de dados MySQL via **terminal**:
```
mysql -h localhost -u root -p
```

<br>Se estiver usando um console que aceita comandos SQL diretos:
```
\sql
\connect root@localhost
```
Você também pode acessar o banco normalmente pelo MySQL Workbench.<br><br>

### Banco de Dados
📂 Na pasta Códigos_SQL, você encontrará:<br>
  → create_tables.sql – criação do esquema e das tabelas<br>
  → insert_data.sql – população com dados fictícios para testes<br>
Execute esses scripts no MySQL antes de iniciar o programa.<br><br>

#### Observações
- Caso precise alterar as credenciais do banco, edite o arquivo conexao.py.
- Todos os dados utilizados são fictícios e servem apenas para fins de teste.
- O projeto implementa operações de CRUD completo para gerenciamento das tabelas relacionadas ao sistema de pedidos de pizza.<br><br>

❕ Projeto acadêmico desenvolvido exclusivamente para fins educacionais.
