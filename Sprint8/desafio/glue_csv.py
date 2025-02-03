import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType

# Criando o contexto do Glue
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Configuração dos caminhos no S3
RAW_PATH = "s3://data-lake-desafio/Raw/Local/CSV/"
TRUSTED_PATH = "s3://data-lake-desafio/Trusted/Local/Parquet/"

# Definição de esquemas para Movies e Series
schemas = {
    "Movies": StructType([
        StructField("id", StringType(), True),
        StructField("tituloPincipal", StringType(), True),
        StructField("tituloOriginal", StringType(), True),
        StructField("anoLancamento", IntegerType(), True),
        StructField("tempoMinutos", IntegerType(), True),
        StructField("genero", StringType(), True),
        StructField("notaMedia", FloatType(), True),
        StructField("numeroVotos", IntegerType(), True),
        StructField("generoArtista", StringType(), True),
        StructField("personagem", StringType(), True),
        StructField("nomeArtista", StringType(), True),
        StructField("anoNascimento", IntegerType(), True),
        StructField("anoFalecimento", IntegerType(), True),
        StructField("profissao", StringType(), True),
        StructField("titulosMaisConhecidos", StringType(), True)
    ]),
    "Series": StructType([
        StructField("id", StringType(), True),
        StructField("tituloPincipal", StringType(), True),
        StructField("tituloOriginal", StringType(), True),
        StructField("anoLancamento", IntegerType(), True),
        StructField("anoTermino", IntegerType(), True),
        StructField("tempoMinutos", IntegerType(), True),
        StructField("genero", StringType(), True),
        StructField("notaMedia", FloatType(), True),
        StructField("numeroVotos", IntegerType(), True),
        StructField("generoArtista", StringType(), True),
        StructField("personagem", StringType(), True),
        StructField("nomeArtista", StringType(), True),
        StructField("anoNascimento", IntegerType(), True),
        StructField("anoFalecimento", IntegerType(), True),
        StructField("profissao", StringType(), True),
        StructField("titulosMaisConhecidos", StringType(), True)
    ])
}

# Função para processar e salvar os dados como Parquet sem partições por data
def process_data(data_type):
    input_path = f"{RAW_PATH}{data_type}/*/*/*/"
    output_path = f"{TRUSTED_PATH}{data_type}/"

    print(f"Processando {data_type}...")

    # Lendo o arquivo CSV com schema definido
    df = spark.read.option("header", "true").schema(schemas[data_type]).csv(input_path)

    # Adicionando a coluna de data de ingestão
    df = df.withColumn("data_ingestao", F.current_date())

    # Salvando os dados como Parquet sem particionar por data
    if df.count() > 0:
        df.write.mode("overwrite").parquet(output_path)
        print(f"{data_type} processado com sucesso!")
    else:
        print(f"Nenhum dado encontrado para {data_type}, pulando processamento.")

# Processando ambos os datasets (Movies e Series)
process_data("Movies")
process_data("Series")

print("Processamento de CSV concluído com sucesso!")
