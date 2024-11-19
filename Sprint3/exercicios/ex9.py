# definido a lista

primeirosNomes = ['Joao', 'Douglas', 'Lucas', 'José']
sobreNomes = ['Soares', 'Souza', 'Silveira', 'Pedreira']
idades = [19, 28, 25, 31]

# iterando pelos dados

for i, (primeirosNomes, sobreNomes, idade) in enumerate(zip(primeirosNomes, sobreNomes, idade)):
    print(f"{i} - {primeirosNomes} {sobreNomes} está com {idade} anos")