# lista de palavras

palavras = ['maça', 'arara', 'audio', 'radio', 'radar', 'moto']

# iterar sobre a lista e verificar se palindrono ou nao

for palavra in palavras:
    if palavra == palavra[::-1]:
        print(f"A palavra: {palavra} é um palíndromo")
    else:
        print(f"A palavra: {palavra} não é um palíndromo")

