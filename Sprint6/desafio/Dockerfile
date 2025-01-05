# Imagem base
FROM python:3.9-slim

# Diretório de trabalho
WORKDIR /app

# Copiar arquivos para o container
COPY . /app

# Instalar dependências
RUN pip install boto3

# Comando de execução
CMD ["python", "ingest_data.py"]
