SELECT 
    tbvendas.cdcli, 
    tbvendas.nmcli, 
    ROUND(SUM(tbvendas.qtd * tbvendas.vrunt), 2) AS gasto
FROM 
    tbvendas
WHERE 
    tbvendas.status = 'Concluído'
GROUP BY 
    tbvendas.cdcli, tbvendas.nmcli
ORDER BY 
    gasto DESC
LIMIT 1;
