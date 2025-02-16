import sys
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from pyspark.sql import functions as F

# Criando contexto do Glue
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Caminhos da Trusted Zone
TRUSTED_TMDB_PATH = "s3://data-lake-desafio/Trusted/TMDB/Parquet/"
TRUSTED_LOCAL_PATH = "s3://data-lake-desafio/Trusted/Local/Parquet/"

# Caminho da Refined Zone
REFINED_PATH = "s3://data-lake-desafio/Refined/"

# Carregar dados do TMDB
df_tmdb = spark.read.parquet(f"{TRUSTED_TMDB_PATH}*/*/*/")

# Carregar dados locais (Movies e Series)
df_local_movies = spark.read.parquet(f"{TRUSTED_LOCAL_PATH}Movies/")
df_local_series = spark.read.parquet(f"{TRUSTED_LOCAL_PATH}Series/")

# Renomeando colunas para evitar conflito
df_tmdb = df_tmdb.withColumnRenamed("title", "tituloPrincipal") \
                 .withColumnRenamed("release_date", "dataLancamento") \
                 .withColumnRenamed("vote_average", "notaMedia") \
                 .withColumnRenamed("vote_count", "numeroVotos") \
                 .withColumnRenamed("popularity", "popularidade") \
                 .withColumnRenamed("original_language", "idiomaOriginal")

df_local_movies = df_local_movies.withColumnRenamed("tituloPincipal", "tituloPrincipal") \
                                 .withColumnRenamed("tituloOriginal", "tituloOriginalLocal")

df_local_series = df_local_series.withColumnRenamed("tituloPincipal", "tituloPrincipal") \
                                 .withColumnRenamed("tituloOriginal", "tituloOriginalLocal")

# Unir os dados corrigindo colunas diferentes
df_filmes = df_tmdb.unionByName(df_local_movies, allowMissingColumns=True)
df_filmes = df_filmes.unionByName(df_local_series, allowMissingColumns=True)

# Verificando Schema final antes do processamento
df_filmes.printSchema()

# Convertendo datas
df_filmes = df_filmes.withColumn("dataLancamento", F.to_date("dataLancamento", "yyyy-MM-dd"))

# Criar tabelas dimensão
dim_atores = df_filmes.selectExpr("id as id_ator", "nomeArtista as nome").distinct()
dim_diretores = df_filmes.selectExpr("id as id_diretor", "profissao").filter(F.col("profissao") == "Director").distinct()
dim_roteiristas = df_filmes.selectExpr("id as id_roteirista", "profissao").filter(F.col("profissao") == "Writer").distinct()
dim_personagens = df_filmes.selectExpr("id as id_personagem", "personagem").distinct()
dim_colecoes = df_filmes.selectExpr("id as id_colecao", "tituloPrincipal as nome_colecao").distinct()
dim_datas = df_filmes.selectExpr("year(dataLancamento) as ano", "month(dataLancamento) as mes", "day(dataLancamento) as dia").distinct()

# Criar tabela fato
fato_filmes = df_filmes.select(
    "id",
    "genero",
    "notaMedia",
    "numeroVotos",
    "popularidade",
    "idiomaOriginal"
)

# Salvando tabelas na camada Refined
dim_atores.write.mode("overwrite").parquet(f"{REFINED_PATH}DimAtores/")
dim_diretores.write.mode("overwrite").parquet(f"{REFINED_PATH}DimDiretores/")
dim_roteiristas.write.mode("overwrite").parquet(f"{REFINED_PATH}DimRoteiristas/")
dim_personagens.write.mode("overwrite").parquet(f"{REFINED_PATH}DimPersonagens/")
dim_colecoes.write.mode("overwrite").parquet(f"{REFINED_PATH}DimColecoes/")
dim_datas.write.mode("overwrite").parquet(f"{REFINED_PATH}DimDatas/")
fato_filmes.write.mode("overwrite").parquet(f"{REFINED_PATH}FatoFilmes/")

print("Processamento da camada Refined concluído com sucesso!")
