def remover_duplicate(lista):
    """Remove duplicados de uma lista e retorna uma nova lista."""
    return list(set(lista))


# lista definida

lista_definida = ['abc', 'abc', 'abc', '123', 'abc', '123', '123']

nova_lista = remover_duplicate(lista_definida)
print(nova_lista)

