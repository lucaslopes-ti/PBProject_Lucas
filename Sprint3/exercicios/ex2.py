# Declara explicitamente a lista chamada 'numeros'
numeros = []

# Preenche a lista com três números usando a função range()
for num in range(1, 4):  # Gera os números 1, 2, e 3
    numeros.append(num)

# Verifica cada número se é par ou ímpar
for numero in numeros:
    if numero % 2 == 0:
        print(f"Par: {numero}")
    else:
        print(f"Ímpar: {numero}")