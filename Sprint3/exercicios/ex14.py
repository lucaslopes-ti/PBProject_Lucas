def imprimir_parametros(*args, **kwargs):
    """Imprime os parâmetros não nomeados e nomeados, um por linha."""
    
    # imprimindo os parâmetros não nomeados
    for arg in args:
        print(arg)
    
    # imprimindo os valores dos parâmetros nomeados
    for value in kwargs.values():
        print(value)

# testando a função com os parâmetros fornecidos
imprimir_parametros(1, 3, 4, 'hello', parametro_nomeado='alguma coisa', x=20)
