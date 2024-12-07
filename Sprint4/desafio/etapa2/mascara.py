import hashlib

# Receber input do usuário
entrada = input("Digite uma string para mascarar: ")

# Gerar o hash SHA-1
hash_sha1 = hashlib.sha1(entrada.encode())

# Imprimir o hash na tela
print(f"O hash SHA-1 da string é: {hash_sha1.hexdigest()}")
