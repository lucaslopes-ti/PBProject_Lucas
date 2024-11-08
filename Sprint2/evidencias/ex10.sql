SELECT 
    tbvendedor.nmvdd AS vendedor, 
    ROUND(SUM(tbvendas.qtd * tbvendas.vrunt), 2) AS valor_total_vendas,
    ROUND(SUM(tbvendas.qtd * tbvendas.vrunt * 
        CASE 
            WHEN tbvendedor.perccomissao = 1 THEN 0.01
            WHEN tbvendedor.perccomissao = 0.5 THEN 0.005
            ELSE 0 
        END), 2) AS comissao
FROM 
    tbvendas
JOIN 
    tbvendedor ON tbvendas.cdvdd = tbvendedor.cdvdd
WHERE 
    tbvendas.status = 'Concluído'
GROUP BY 
    tbvendedor.nmvdd
ORDER BY 
    comissao DESC;
