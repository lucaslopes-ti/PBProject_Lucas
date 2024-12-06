def maiores_que_media(conteudo: dict) -> list:
    # Calcular a média dos valores
    media = sum(conteudo.values()) / len(conteudo)
    
    # Filtrar produtos com valores acima da média e gerar uma lista de tuplas
    produtos_acima_da_media = [(produto, preco) for produto, preco in conteudo.items() if preco > media]
    
    # Ordenar os produtos pelo preço em ordem crescente
    produtos_ordenados = sorted(produtos_acima_da_media, key=lambda x: x[1])
    
    return produtos_ordenados

# Exemplo de uso
conteudo = {
    "arroz": 4.99,
    "feijão": 3.49,
    "macarrão": 2.99,
    "leite": 3.29,
    "pão": 1.99
}

resultado = maiores_que_media(conteudo)
print(resultado)
