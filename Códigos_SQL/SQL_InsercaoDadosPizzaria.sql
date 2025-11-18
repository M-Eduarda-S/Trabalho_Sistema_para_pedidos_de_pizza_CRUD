-- POPULANDO TABELAS com dados totalmente fictícios
use pizzaria_pedidos;

DESCRIBE Estado;
DESCRIBE Cidade;
DESCRIBE Pessoa;
DESCRIBE Cliente;
DESCRIBE Funcionario;
DESCRIBE Cozinheiro;
DESCRIBE Entregador;
DESCRIBE Ingrediente;
DESCRIBE Sabor;
DESCRIBE Pedido;
DESCRIBE Pizza;
DESCRIBE Entrega;

SELECT * FROM Estado;
SELECT * FROM Cidade;
SELECT * FROM Pessoa;
SELECT * FROM Telefone_pessoa;
SELECT * FROM Endereco_pessoa;
SELECT * FROM Cliente;
SELECT * FROM Funcionario;
SELECT * FROM Cozinheiro;
SELECT * FROM Entregador;
SELECT * FROM Ingrediente;
SELECT * FROM Sabor;
SELECT * FROM Pedido;
SELECT * FROM Pizza;
SELECT * FROM Entrega;

INSERT INTO Estado (sigla, nome) VALUES
	('SC', 'Santa Catarina');
    
INSERT INTO Cidade (id_estado, nome) VALUES
	(1, 'Blumenau'),
	(1, 'Gaspar'),
	(1, 'Navegantes'),
	(1, 'Brusque'),
	(1, 'Itajaí');
    
INSERT INTO Pessoa (nome, email) VALUES
	('Marina Silva', 'marina.silva@example.com'),
	('Yasmin Faccin', 'yasmin.faccin@example.com'),
	('Maria Santos', 'maria.santos@example.com'),
	('Carlos Silveira', 'carlos.silveira@example.com'),
	('Fernanda Dias', 'fernanda.dias@example.com'), -- clientes
    ('Ricardo Mello', 'ricardo.mello@example.com'), -- funcionarios
	('Patricia Souza', 'patricia.souza@example.com'),
	('Lucas Andrade', 'lucas.andrade@example.com'),
	('Juliana Ramos', 'juliana.ramos@example.com'),
	('Thiago Weber', 'thiago.weber@example.com');
    
INSERT INTO Telefone_pessoa (id_pessoa, numero, tipo) VALUES
	(1, '47 98811-2233', 'Celular'),
	(2, '47 99722-3344', 'Celular'),
	(3, '47 99955-8899', 'Comercial'),
	(4, '47 98111-0099', 'Celular'),
	(5, '47 98888-4444', 'Celular'),
	(6, '47 97777-1212', 'Celular'),
	(7, '47 96666-3434', 'Celular'),
	(8, '47 95555-5656', 'Celular'),
	(9, '47 94444-7878', 'Celular'),
	(10,'47 93333-9090', 'Celular');

INSERT INTO Endereco_pessoa (id_pessoa, id_cidade, numero, cep, rua, logradouro, complemento) VALUES
	(1, 1, 120, '89010-001', 'Rua 7 de Setembro', 'Centro', NULL),
	(2, 2, 441, '89110-200', 'Av. das Comunidades', 'Centro', 'Casa'),
	(3, 3, 999, '89080-300', 'Rua das Palmeiras', 'Carijós', NULL),
	(4, 4, 55, '88350-100', 'Rua Barão do Rio Branco', 'Centro', 'Bloco B'),
	(5, 5, 222, '89120-400', 'Rua Blumenau', 'Centro', NULL),
	(6, 1, 321, '89012-020', 'Rua São Paulo', 'Victor Konder', NULL),
	(7, 2, 88, '89110-250', 'Rua Itajaí', 'Sete de Setembro', NULL),
	(8, 3, 300, '89080-500', 'Rua Indaial', 'Warnow', NULL),
	(9, 4, 450, '88350-300', 'Rua Brusque', 'Santa Terezinha', NULL),
	(10,5, 600, '89120-500', 'Rua Timbó', 'Arno Brandt', NULL);
    
INSERT INTO Cliente (id_pessoa, cpf) VALUES
	(1, '11122233344'),
	(2, '22233344455'),
	(3, '33344455566'),
	(4, '44455566677'),
	(5, '55566677788');
    
INSERT INTO Funcionario (id_pessoa, cpf, salario, turno) VALUES
	(6, '66677788899', 3200.00, 'Noturno'),
	(7, '77788899900', 3100.00, 'Matutino'),
	(8, '88899900011', 3000.00, 'Vespertino'),
	(9, '99900011122', 4200.00, 'Noturno'),
	(10,'00011122233', 3500.00, 'Matutino');
    
INSERT INTO Cozinheiro (id_funcionario, funcao) VALUES
	(1, 'Chef'),
	(2, 'Auxiliar'),
	(3, 'Montar as pizzas'),
	(4, 'Assar as pizzas'),
	(5, 'Controle de estoque');
    
INSERT INTO Entregador (id_funcionario, cnh, placa_veiculo) VALUES
	(1, 123456, 'QWE1A23'),
	(2, 654321, 'ASD2B34'),
	(3, 112233, 'ZXC3C45'),
	(4, 443322, 'RTY4D56'),
	(5, 778899, 'FGH5E67');
    
INSERT INTO Fornecedor (id_pessoa, cnpj) VALUES
	(6, '12.345.678/0001-10'),
	(7, '98.765.432/0001-55'),
	(8, '45.678.123/0001-22'),
	(9, '23.456.789/0001-33'),
	(10,'56.789.123/0001-44');
    
INSERT INTO Ingrediente (nome, quantidade, disponibilidade, valor_unitario) VALUES
	('Queijo Mussarela', 50, 'Sim', 2.50), 
	('Tomate', 40, 'Sim', 3.00),   
	('Manjericão', 30, 'Sim', 4.00),   
	('Cebola', 25, 'Sim', 3.50),   
	('Brócolis', 20, 'Sim', 5.00);   
    
INSERT INTO Fornecedor_Ingrediente VALUES
	(1,1),
	(2,2),
	(3,3),
	(4,4),
	(5,5);
    
INSERT INTO Sabor (nome) VALUES
	('Mussarela'),
	('Marguerita'),
	('Vegetariana'),
	('4 Queijos'),
	('Napolitana');

INSERT INTO Ingrediente_Sabor VALUES
	(1,1),
	(1,2),
	(2,2),
	(3,2),
	(2,3),
	(4,3),
	(5,3),
	(1,4),
	(2,5),
	(4,5);
    
INSERT INTO Pedido (id_cliente, valor_pagamento, status, endereco_entrega, quantidade_pizzas, data_pedido, horario_pedido) VALUES
	(1, 45.00, 'Aberto', 'Rua 7 de Setembro, 120 - Blumenau', 1, CURRENT_DATE, '19:10:00'),
	(2, 60.00, 'Em preparo', 'Av. das Comunidades, 441 - Gaspar', 2, CURRENT_DATE, '19:20:00'),
	(3, 32.00, 'Saiu para entrega', 'Rua das Palmeiras, 999 - Indaial', 1, CURRENT_DATE, '19:30:00'),
	(4, 85.00, 'Entregue', 'Rua Barão do Rio Branco, 55 - Brusque', 2, CURRENT_DATE, '19:00:00'),
	(5, 50.00, 'Aberto', 'Rua Blumenau, 222 - Timbó', 1, CURRENT_DATE, '19:40:00');
    
INSERT INTO Pizza (id_pedido, tamanho, valor_pizza) VALUES
	(1, 'M', 45.00),
	(2, 'G', 60.00),
	(2, 'P', 30.00),
	(3, 'M', 32.00),
	(4, 'G', 85.00);
    
INSERT INTO Pizza_Sabor VALUES
	(1,1),
	(2,2),
	(2,4),
	(3,3),
	(4,5);
    
INSERT INTO Entrega (id_pedido, id_entregador, data_entrega, horario, status) VALUES
	(1, 1, CURRENT_DATE, '19:40:00', 'Em rota'),
	(2, 2, CURRENT_DATE, '19:50:00', 'Pendente'),
	(3, 3, CURRENT_DATE, '19:45:00', 'Em rota'),
	(4, 4, CURRENT_DATE, '19:20:00', 'Entregue'),
	(5, 5, CURRENT_DATE, '20:00:00', 'Pendente');