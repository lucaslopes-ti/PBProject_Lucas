from functools import reduce

def calcula_saldo(lancamentos) -> float:
    #continue este código
    #converte cada lancamento de um valor positivo ou negativo usando o map
    valores = map(lambda x: x[0] if x[1] == 'C' else -x[0], lancamentos)

    #reduz os valores para calcular o saldo final
    saldo = reduce(lambda acc, val: acc + val, valores, 0)
    
    return float(saldo)
    

# Exemplo de uso
lancamentos = [
    (200, 'D'),
    (300, 'C'),
    (100, 'C')
]

print(calcula_saldo(lancamentos))