def soma_numeros(numeros: str) -> int:
    """Recebe uma string de numeros separados por virgula e retorna a soma."""
    return sum(int(num) for num in numeros.split(','))

#testando a funcao com a string
string_numeros = "1,3,4,6,10,76"
resultado = soma_numeros(string_numeros)


print(resultado)