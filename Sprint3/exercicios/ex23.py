class Calculo:
    def soma(self, x, y):
        return x + y
    
    def subtracao(self, x, y):
        return x - y
    

# testando a classe
x = 4
y = 5

calculo = Calculo()

resultado_soma = calculo.soma(x, y)
resultado_subtracao = calculo.subtracao(x, y)

print(f"Somando: {x}+{y} = {resultado_soma}")
print(f"Subtraindo: {x}-{y} = {resultado_subtracao}")