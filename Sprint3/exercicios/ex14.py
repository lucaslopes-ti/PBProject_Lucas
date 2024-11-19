def imprimir_parametros(*args, **kwargs):
    """Imprime os parametros nao nomeados e nomeados"""

    print("Parametros nao nomeados")
    index = 2  
    for arg in args:
        print(f" {index}: {arg}")
        index += 1  

    
    print("Parametros nomeados:")
    for key, value in kwargs.items():
        print(f" {key}: {value}")
    

# testando a funcao

imprimir_parametros(1, 3, 4, 'hello', parametro_nomeado='alguma coisa', x=20)