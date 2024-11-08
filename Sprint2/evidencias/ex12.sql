WITH VendedorMenorVenda AS (
    SELECT 
        tbvendas.cdvdd, 
        SUM(tbvendas.qtd * tbvendas.vrunt) AS valor_total_vendas
    FROM 
        tbvendas
    WHERE 
        tbvendas.status = 'Concluído'
    GROUP BY 
        tbvendas.cdvdd
    HAVING 
        valor_total_vendas > 0
    ORDER BY 
        valor_total_vendas ASC
    LIMIT 1
)
SELECT 
    tbdependente.cddep, 
    tbdependente.nmdep, 
    tbdependente.dtnasc, 
    VendedorMenorVenda.valor_total_vendas
FROM 
    tbdependente
JOIN 
    VendedorMenorVenda ON tbdependente.cdvdd = VendedorMenorVenda.cdvdd;
