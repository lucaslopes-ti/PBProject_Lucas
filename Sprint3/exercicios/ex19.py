import random

#gera a lista aleatoria com 50 numeros no intervalo de 0 a 500
random_list = random.sample(range(500), 50)

#calcula o valor minimo e maximo
valor_minimo = min(random_list)
valor_maximo = max(random_list)

#calcula a media
media = sum(random_list) / len(random_list)

#ordena a lista para calcula a mediana
random_list.sort()
meio = len(random_list) // 2

# calculo da mediana
if len(random_list) % 2 == 0:
    mediana = (random_list[meio - 1] + random_list[meio]) / 2
else:
    mediana = random_list[meio]


print(f"Media: {media}, Mediana: {mediana}, Mínimo: {valor_minimo}, Máximo: {valor_maximo}")