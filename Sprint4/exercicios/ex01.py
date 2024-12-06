# Abrir o arquivo e ler os números
with open("number.txt", "r") as file:
    numeros = list(map(int, file.readlines()))  # Converte cada linha em um inteiro

# Filtrar apenas os números pares
pares = list(filter(lambda x: x % 2 == 0, numeros))

# Ordenar os números pares em ordem decrescente
pares_ordenados = sorted(pares, reverse=True)

# Selecionar os 5 maiores números pares
top_5_pares = pares_ordenados[:5]

# Calcular a soma dos 5 maiores números pares
soma_top_5 = sum(top_5_pares)

# Exibir a lista e a soma
print(top_5_pares)
print(soma_top_5)
