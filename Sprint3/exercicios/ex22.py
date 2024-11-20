class Pessoa:
    def __init__(self, id):
        """Inicializa a Pessoa com um ID e um nome privado"""
        self.id = id
        self.__nome = None

    @property
    def nome(self):
        """Retorna o valor do atributo privado __nome """
        return self.__nome
    

    @nome.setter
    def nome(self, value):
        """Define o valor do atributo privado"""
        self.__nome = value
    

#testando a classe Pessoa
pessoa = Pessoa(0) 
pessoa.nome = 'Fulano De Tal'
print(pessoa.nome)