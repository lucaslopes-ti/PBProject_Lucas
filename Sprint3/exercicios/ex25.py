class Aviao:
    cor = "Azul" 

    def __init__(self, modelo, velocidade_maxima, capacidade):
        """Inicializa os atributos do avião."""
        self.modelo = modelo
        self.velocidade_maxima = velocidade_maxima
        self.capacidade = capacidade

    def __str__(self):
        """Representação em string para impressão do objeto."""
        return (f"O avião de modelo '{self.modelo}' possui uma velocidade máxima de "
                f"{self.velocidade_maxima}, capacidade para {self.capacidade} passageiros "
                f"e é da cor {Aviao.cor}.")


# Criando os objetos e armazenando na lista
avioes = [
    Aviao("BOIENG456", "1500 km/h", 400),
    Aviao("Embraer Praetor 600", "863 km/h", 14),
    Aviao("Antonov An-2", "258 km/h", 12)
]

# iterando pela lista e imprimindo os objetos
for aviao in avioes:
    print(aviao)