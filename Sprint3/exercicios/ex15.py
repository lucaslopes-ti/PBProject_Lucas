class Lampada:
    def __init__(self, estado_inicial: bool):
        """Inicializa a lampada com o estado especificado."""
        self.ligada = estado_inicial  

    def liga(self):
        """Liga a lampada."""
        self.ligada = True
    
    def desliga(self):
        """Desliga a lampada."""
        self.ligada = False

    def esta_ligada(self):
        """Retorna o estado da lampada."""
        return self.ligada


# Testando a classe Lampada
lampada = Lampada(False)

lampada.liga()
print("A lampada esta ligada?", lampada.esta_ligada())  

lampada.desliga()
print("A lampada ainda esta ligada?", lampada.esta_ligada())  
