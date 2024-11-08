SELECT 
    tbvendas.cdpro, 
    tbvendas.nmcanalvendas, 
    tbvendas.nmpro, 
    SUM(tbvendas.qtd) AS quantidade_vendas
FROM 
    tbvendas
WHERE 
    tbvendas.status = 'Concluído'
    AND tbvendas.nmcanalvendas IN ('Ecommerce', 'Matriz')
GROUP BY 
    tbvendas.cdpro, tbvendas.nmcanalvendas, tbvendas.nmpro
ORDER BY 
    quantidade_vendas ASC
LIMIT 10;
