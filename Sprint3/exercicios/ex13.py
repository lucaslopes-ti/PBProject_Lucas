arquivo_base = 'arquivo_texto.txt'

# abrindo o arquivo no modo leitura e lendo o arquivo
with open(arquivo_base, 'r') as arquivo:
    conteudo = arquivo.read()

print(conteudo, end='')