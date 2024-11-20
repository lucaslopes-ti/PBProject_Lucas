class Ordenadora:
    def __init__(self, listaBaguncada):
        """Inicializa o objeto com a lista desordenada."""
        self.listaBaguncada = listaBaguncada

    def ordenacaoCrescente(self):
        """Ordena a lista em ordem crescente e a retorna."""
        return sorted(self.listaBaguncada)

    def ordenacaoDecrescente(self):
        """Ordena a lista em ordem decrescente e a retorna."""
        return sorted(self.listaBaguncada, reverse=True)


# criando o objeto para ordenação crescente
crescente = Ordenadora([3, 4, 2, 1, 5])
resultado_crescente = crescente.ordenacaoCrescente()

# criando o objeto para ordenação decrescente
decrescente = Ordenadora([9, 7, 6, 8])
resultado_decrescente = decrescente.ordenacaoDecrescente()

# imprimindo os resultados
print(resultado_crescente) 
print(resultado_decrescente)  
