import json

arquivo_json = 'person.json'

with open(arquivo_json, 'r') as arquivo:
    dados = json.load(arquivo)

print(dados)