import boto3

# Criação da sessão com perfil default
session = boto3.Session(profile_name='default')

# Criação do cliente S3 usando a sessão
s3_client = session.client('s3')

# Nome do bucket
bucket_name = 'meu-bucket-desafio'
# Caminho do arquivo local
file_path = 'C:/Users/Lucas/OneDrive/PBProject_Lucas/Sprint5/desafio/professores_da_ufu_2023.csv'
# Nome do arquivo no S3
s3_file_name = 'meu_arquivo.csv'

# Criação do bucket
s3_client.create_bucket(Bucket=bucket_name)

# Upload do arquivo
s3_client.upload_file(file_path, bucket_name, s3_file_name)
print('Arquivo carregado com sucesso!')
