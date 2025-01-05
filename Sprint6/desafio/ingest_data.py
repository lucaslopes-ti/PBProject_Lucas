import boto3
import os
from datetime import datetime

# Configurações AWS e bucket
BUCKET_NAME = "data-lake-desafio"  
AWS_REGION = "us-east-1"

# Caminho dos arquivos
FILES_PATHS = {
    "movies": "/data/movies.csv", 
    "series": "/data/series.csv",  
}

def upload_to_s3(file_path, s3_key):
    """Carrega arquivo local para o S3."""
    try:
        s3_client = boto3.client("s3")
        s3_client.upload_file(file_path, BUCKET_NAME, s3_key)
        print(f"Upload realizado com sucesso: {s3_key}")
    except Exception as e:
        print(f"Erro ao fazer upload: {e}")

def main():
    # Data de processamento
    today = datetime.now()
    date_path = today.strftime("%Y/%m/%d")

    for data_type, file_path in FILES_PATHS.items():
        if not os.path.exists(file_path):
            print(f"Arquivo não encontrado: {file_path}")
            continue

        # Define o caminho no S3
        s3_key = f"Raw/Local/CSV/{data_type.capitalize()}/{date_path}/{os.path.basename(file_path)}"

        # Envia para o S3
        upload_to_s3(file_path, s3_key)

if __name__ == "__main__":
    main()
