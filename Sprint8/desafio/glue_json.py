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
RAW_PATH = "s3://data-lake-desafio/Raw/TMDB/JSON/"
TRUSTED_PATH = "s3://data-lake-desafio/Trusted/TMDB/Parquet/"

# Definição do esquema para os arquivos JSON
schema_json = StructType([
    StructField("id", IntegerType(), True),
    StructField("title", StringType(), True),
    StructField("release_date", StringType(), True),
    StructField("genres", StringType(), True),
    StructField("original_language", StringType(), True),
    StructField("overview", StringType(), True),
    StructField("popularity", FloatType(), True),
    StructField("vote_average", FloatType(), True),
    StructField("vote_count", IntegerType(), True)
])

# Lendo os arquivos JSON do S3
df = spark.read.option("multiline", "true").schema(schema_json).json(f"{RAW_PATH}*/*/*/")

# Convertendo a release_date para data e extraindo ano/mês/dia
df = df.withColumn("release_date", F.to_date("release_date", "yyyy-MM-dd"))
df = df.withColumn("ano", F.year("release_date"))
df = df.withColumn("mes", F.month("release_date"))
df = df.withColumn("dia", F.dayofmonth("release_date"))

# Criando partições no formato correto (2025/2/3)
df.write.mode("overwrite").partitionBy("ano", "mes", "dia").parquet(TRUSTED_PATH)

print("Processamento de JSON concluído com sucesso!")
