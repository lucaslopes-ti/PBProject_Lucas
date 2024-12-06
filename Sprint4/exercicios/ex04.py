def calcular_valor_maximo(operadores,operandos) -> float:
    resultados = map(
        lambda oper: eval(f"{oper[1][0]} {oper[0]} {oper[1][1]}"),
        zip(operadores, operandos)
    )
    
    return max(resultados)
    
    
# Exemplo de uso
operadores = ['+', '-', '*', '/', '+']
operandos = [(3, 6), (-7, 4.9), (8, -8), (10, 2), (8, 4)]

print(calcular_valor_maximo(operadores, operandos))