from pyspark.sql import SparkSession

# Criando a sessão Spark
spark = SparkSession.builder \
    .appName("Visualizar Parquet Local Filmes") \
    .getOrCreate()

# Caminho base para os arquivos Parquet locais
PARQUET_BASE_PATH = r"C:\Users\Lucas\iCloudDrive\PB_Lucas\PBProject_Lucas\Sprint9\desafio\parquet_files\part-"

# Número de partes (0000 até 0003)
num_partes = 4

# Itera por cada parte e imprime o schema e algumas amostras dos dados
for i in range(num_partes):
    part_number = str(i).zfill(5)  # Gera '0000', '0001', etc.
    path = f"{PARQUET_BASE_PATH}{part_number}.parquet"
    try:
        print(f"\n📄 **Arquivo:** {path}")
        df = spark.read.parquet(path)
        df.printSchema()  # Mostra o schema
        df.show(5, truncate=False)  # Mostra 5 linhas para verificar os dados

    except Exception as e:
        print(f"⚠️ Erro ao ler {path}: {e}")
