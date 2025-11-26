-- Disciplina: Banco de Dados I
-- Professor: Maurício Pasetto de Freitas
-- Nomes: Maria Eduarda Santos e Yasmin Tarnovski Faccin.

-- CRIAÇÃO DE ESQUEMA E TABELAS
CREATE SCHEMA pizzaria_pedidos;
use pizzaria_pedidos;
-- DROP SCHEMA pizzaria_pedidos;

-- DROP TABLE Estado;
CREATE TABLE Estado (
    id INT PRIMARY KEY AUTO_INCREMENT,
    sigla VARCHAR(2) NOT NULL,
    nome VARCHAR(50) NOT NULL
);

-- DROP TABLE Cidade;
CREATE TABLE Cidade (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_estado INT NOT NULL,
    nome VARCHAR(100) NOT NULL,
    
    FOREIGN KEY (id_estado) REFERENCES Estado(id)
		ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- DROP TABLE Pessoa;
CREATE TABLE Pessoa (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(200) NOT NULL UNIQUE
);

-- DROP TABLE Telefone_pessoa;
CREATE TABLE Telefone_pessoa (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_pessoa INT NOT NULL,
    numero VARCHAR(16) NOT NULL,
    tipo ENUM('Fixo', 'Celular', 'Comercial') NOT NULL,
    
    FOREIGN KEY (id_pessoa) REFERENCES Pessoa(id)
		ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- DROP TABLE Endereco_pessoa;
CREATE TABLE Endereco_pessoa (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_pessoa INT NOT NULL,
    id_cidade INT NOT NULL,
    numero INT NOT NULL,
    cep VARCHAR(12) NOT NULL,
    rua VARCHAR(100) NOT NULL,
    logradouro VARCHAR(100),
    complemento VARCHAR(50),
    
    FOREIGN KEY (id_pessoa) REFERENCES Pessoa(id)
		ON UPDATE CASCADE
        ON DELETE CASCADE,
        
    FOREIGN KEY (id_cidade) REFERENCES Cidade(id)
		ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- DROP TABLE Cliente;
CREATE TABLE Cliente (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_pessoa INT NOT NULL,
    cpf VARCHAR(12) UNIQUE NOT NULL,
    
    FOREIGN KEY (id_pessoa) REFERENCES Pessoa(id)
		ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- DROP TABLE Funcionario;
CREATE TABLE Funcionario (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_pessoa INT NOT NULL,
    cpf VARCHAR(12) UNIQUE NOT NULL,
    salario DECIMAL(10,2) NOT NULL,
    turno ENUM('Matutino', 'Vespertino', 'Noturno') NOT NULL,
    
    FOREIGN KEY (id_pessoa) REFERENCES Pessoa(id)
		ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- DROP TABLE Cozinheiro;
CREATE TABLE Cozinheiro (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_funcionario INT NOT NULL,
    funcao ENUM('Chef', 'Auxiliar', 'Assar as pizzas', 'Montar as pizzas', 'Higienização de ingredientes', 'Controle de estoque') NOT NULL,
    
    FOREIGN KEY (id_funcionario) REFERENCES Funcionario(id)
		ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- DROP TABLE Entregador;
CREATE TABLE Entregador (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_funcionario INT NOT NULL,
    cnh VARCHAR(11) NOT NULL,
    placa_veiculo VARCHAR(8) NOT NULL,
    
    FOREIGN KEY (id_funcionario) REFERENCES Funcionario(id)
		ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- DROP TABLE Fornecedor;
CREATE TABLE Fornecedor (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_pessoa INT NOT NULL,
    cnpj VARCHAR(18) UNIQUE NOT NULL,
    
    FOREIGN KEY (id_pessoa) REFERENCES Pessoa(id)
		ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- DROP TABLE Ingrediente;
CREATE TABLE Ingrediente (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(50) NOT NULL,
    quantidade INT NOT NULL,
    disponibilidade ENUM('Sim','Não') NOT NULL,
    valor_unitario DECIMAL(10,2) NOT NULL
);

-- DROP TABLE Fornecedor_Ingrediente;
CREATE TABLE Fornecedor_Ingrediente (
    id_fornecedor INT NOT NULL,
    id_ingrediente INT NOT NULL,
    
    PRIMARY KEY (id_fornecedor, id_ingrediente),
    FOREIGN KEY (id_fornecedor) REFERENCES Fornecedor(id)
		ON UPDATE CASCADE
        ON DELETE CASCADE,
    
    FOREIGN KEY (id_ingrediente) REFERENCES Ingrediente(id)
		ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- DROP TABLE Sabor;
CREATE TABLE Sabor (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(50) NOT NULL
);

-- DROP TABLE Ingrediente_Sabor;
CREATE TABLE Ingrediente_Sabor (
    id_ingrediente INT NOT NULL,
    id_sabor INT NOT NULL,
    
    PRIMARY KEY (id_ingrediente, id_sabor),
    FOREIGN KEY (id_ingrediente) REFERENCES Ingrediente(id)
		ON UPDATE CASCADE
        ON DELETE CASCADE,
        
    FOREIGN KEY (id_sabor) REFERENCES Sabor(id)
		ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- DROP TABLE Pedido;
CREATE TABLE Pedido (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_cliente INT NOT NULL,
    valor_pagamento DECIMAL(10,2) NOT NULL,
    status ENUM('Aberto', 'Em preparo', 'Saiu para entrega', 'Entregue', 'Cancelado') NOT NULL,
    endereco_entrega VARCHAR(200) NOT NULL,
    data_pedido DATE NOT NULL,
    horario_pedido TIME NOT NULL,
    
    FOREIGN KEY (id_cliente) REFERENCES Cliente(id)
		ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- DROP TABLE Pizza;
CREATE TABLE Pizza (
    id INT PRIMARY KEY AUTO_INCREMENT,
    tamanho ENUM('P', 'M', 'G', 'GG') NOT NULL,
    valor_pizza DECIMAL(10,2) NOT NULL
);

-- DROP TABLE Pedido_Pizza;
CREATE TABLE Pedido_Pizza (
	id INT PRIMARY KEY AUTO_INCREMENT,
    id_pedido INT NOT NULL,
    id_pizza INT NOT NULL,
    
    FOREIGN KEY (id_pedido) REFERENCES Pedido(id)
		ON UPDATE CASCADE
        ON DELETE CASCADE,
        
    FOREIGN KEY (id_pizza) REFERENCES Pizza(id)
		ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- DROP TABLE Pizza_Sabor;
CREATE TABLE Pizza_Sabor (
    id_pedido_pizza INT NOT NULL, -- colocar sabores diferentes em pizzas do mesmo pedido
    id_sabor INT NOT NULL,
    
    PRIMARY KEY (id_pedido_pizza, id_sabor),
    FOREIGN KEY (id_pedido_pizza) REFERENCES Pedido_Pizza(id)
		ON UPDATE CASCADE
        ON DELETE CASCADE,
        
    FOREIGN KEY (id_sabor) REFERENCES Sabor(id)
		ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- DROP TABLE Entrega;
CREATE TABLE Entrega (
    id_pedido INT PRIMARY KEY NOT NULL,
    id_entregador INT NULL, -- o entegador ainda não foi atribuito
    data_entrega DATE NOT NULL,
    horario TIME NOT NULL,
    status ENUM('Pendente','Em rota','Entregue') NOT NULL,
    
    FOREIGN KEY (id_pedido) REFERENCES Pedido(id) -- só pode existir uma entrega se o pedido existir e se o pedido for deletado a entrega deve sumir junto
		ON UPDATE CASCADE
        ON DELETE CASCADE,
        
    FOREIGN KEY (id_entregador) REFERENCES Entregador(id)
		ON UPDATE CASCADE
        ON DELETE SET NULL -- o id_entregador vira NULL novamente
);
