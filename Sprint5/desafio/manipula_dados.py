import boto3
import pandas as pd

# Criação da sessão com perfil default
session = boto3.Session(profile_name='default')

# Criação do cliente S3 usando a sessão
s3_client = session.client('s3')

# Função para baixar o arquivo do S3
def download_file_from_s3(bucket_name, file_name, download_path):
    s3_client.download_file(bucket_name, file_name, download_path)

# Configurações
bucket_name = 'meu-bucket-desafio'
s3_file_name = 'meu_arquivo.csv'
download_path = 'C:/Users/Lucas/OneDrive/PBProject_Lucas/Sprint5/desafio/professores_da_ufu_2023_download.csv'
result_file_path = 'C:/Users/Lucas/OneDrive/PBProject_Lucas/Sprint5/desafio/professores_da_ufu_2023_resultado.csv'

# Baixar o arquivo do S3
download_file_from_s3(bucket_name, s3_file_name, download_path)

# Usar o delimitador correto
df = pd.read_csv(download_path, delimiter=';', on_bad_lines='skip')

# Verificar os nomes das colunas
print("Colunas no DataFrame:", df.columns)

# 4.1 Cláusula que filtra dados usando dois operadores lógicos (ajustada para valores numéricos e células vazias)
filtered_df = df[(df['NIVEL'].fillna(0).astype(int) == 1) & (df['REG_TRAB'] == 'DE')]

# 4.2 Duas funções de agregação
aggregation1 = df.groupby('CAMPUS')['MATR_SIAPE'].count().reset_index()
aggregation2 = df.groupby('CAMPUS')['COD_FUNCAO'].nunique().reset_index()

# Merge das agregações de volta ao DataFrame original
df = pd.merge(df, aggregation1, on='CAMPUS', how='left', suffixes=('', '_MATR_SIAPE_COUNT'))
df = pd.merge(df, aggregation2, on='CAMPUS', how='left', suffixes=('', '_COD_FUNCAO_UNIQUE'))

# Renomear as colunas resultantes para maior clareza
df.rename(columns={'MATR_SIAPE_MATR_SIAPE_COUNT': 'COUNT_MATR_SIAPE', 'COD_FUNCAO_COD_FUNCAO_UNIQUE': 'UNIQUE_COD_FUNCAO'}, inplace=True)

# 4.3 Uma função condicional
df['NOVA_COLUNA'] = df['TITULACAO'].apply(lambda x: 'Doutor' if x == 'D' else 'Outro')

# 4.4 Uma função de conversão
df['DATA_ADM'] = pd.to_datetime(df['DATA_ADM'], format='%d/%m/%Y')

# 4.5 Uma função de data
df['ANO_ADM'] = df['DATA_ADM'].dt.year

# 4.6 Uma função de string
df['NOME_MAIUSCULO'] = df['NOME'].str.upper()

# Salvando o arquivo resultante
df.to_csv(result_file_path, index=False)

# Upload do arquivo resultante com novo nome
s3_client.upload_file(result_file_path, bucket_name, 'resultado_professores_ufu.csv')
print('Arquivo resultante carregado com sucesso!')
