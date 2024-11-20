def dividir_lista(lista):
    """Divide uma lista em 3 partes iguais e retorna as partes"""
    tamanho = len(lista) // 3
    return lista[:tamanho], lista[tamanho:2*tamanho], lista[2*tamanho:]

#testando a funcao fornecida
lista = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
parte1, parte2, parte3 = dividir_lista(lista)

print(parte1, parte2, parte3)