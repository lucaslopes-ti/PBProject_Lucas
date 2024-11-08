SELECT 
    autor.codautor, 
    autor.nome, 
    autor.nascimento, 
    COUNT(livro.cod) AS quantidade
FROM 
    autor
LEFT JOIN 
    livro ON autor.codautor = livro.autor
GROUP BY 
    autor.codautor
ORDER BY 
    autor.nome ASC;
