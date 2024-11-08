SELECT 
    tbvendas.estado, 
    ROUND(AVG(tbvendas.qtd * tbvendas.vrunt), 2) AS gastomedio
FROM 
    tbvendas
WHERE 
    tbvendas.status = 'Concluído'
GROUP BY 
    tbvendas.estado
ORDER BY 
    gastomedio DESC;
