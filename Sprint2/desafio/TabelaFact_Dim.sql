-- View para Fato_Locacao
CREATE VIEW Fato_Locacao AS
SELECT 
    idLocacao, 
    idCliente, 
    idCarro, 
    idcombustivel, 
    idVendedor, 
    qtdDiaria, 
    vlrDiaria
FROM 
    Locacao;

-- View para Dim_Cliente
CREATE VIEW Dim_Cliente AS
SELECT 
    idCliente, 
    nomeCliente, 
    cidadeCliente, 
    estadoCliente, 
    paisCliente
FROM 
    Cliente;

-- View para Dim_Carro
CREATE VIEW Dim_Carro AS
SELECT 
    idCarro, 
    kmCarro, 
    classiCarro, 
    marcaCarro, 
    anoCarro
FROM 
    Carro;

-- View para Dim_Combustivel
CREATE VIEW Dim_Combustivel AS
SELECT 
    idcombustivel, 
    tipoCombustivel
FROM 
    Combustivel;

-- View para Dim_Vendedor
CREATE VIEW Dim_Vendedor AS
SELECT 
    idVendedor, 
    nomeVendedor, 
    sexoVendedor, 
    estadoVendedor
FROM 
    Vendedor;

