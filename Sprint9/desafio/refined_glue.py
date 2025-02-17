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

# 🔹 Carregar dados do TMDB
df_tmdb = spark.read.parquet(f"{TRUSTED_TMDB_PATH}*/*/*/")

# 🔹 Carregar dados locais (Movies e Series) 
df_local_movies = spark.read.option("header", "true").option("delimiter", "|").csv(f"{TRUSTED_LOCAL_PATH}Movies/")
df_local_series = spark.read.option("header", "true").option("delimiter", "|").csv(f"{TRUSTED_LOCAL_PATH}Series/")

print("Schema do TMDB:")
df_tmdb.printSchema()

print("Schema dos Filmes Locais:")
df_local_movies.printSchema()

print("Schema das Séries Locais:")
df_local_series.printSchema()

df_filmes = df_tmdb.selectExpr("id", "tituloPrincipal", "dataLancamento", "notaMedia", "numeroVotos", "popularidade", "idiomaOriginal")

df_local_movies = df_local_movies.selectExpr("id", "tituloPrincipal", "tituloOriginalLocal", "anoLancamento", "genero", "notaMedia", "numeroVotos", "generoArtista", "personagem", "nomeArtista", "profissao")

df_local_series = df_local_series.selectExpr("id", "tituloPrincipal", "tituloOriginalLocal", "anoLancamento", "genero", "notaMedia", "numeroVotos", "generoArtista", "personagem", "nomeArtista", "profissao")

df_filmes = df_filmes.unionByName(df_local_movies, allowMissingColumns=True)
df_filmes = df_filmes.unionByName(df_local_series, allowMissingColumns=True)


# Renomear colunas para evitar conflitos entre TMDB e Local
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


# 🔹 Adicionando a origem dos dados
df_tmdb = df_tmdb.withColumn("origem", F.lit("TMDB"))
df_local_movies = df_local_movies.withColumn("origem", F.lit("Local"))
df_local_series = df_local_series.withColumn("origem", F.lit("Local"))

# 🔹 Unindo os dados de TMDB + CSVs Locais
df_filmes = df_tmdb.unionByName(df_local_movies, allowMissingColumns=True)
df_filmes = df_filmes.unionByName(df_local_series, allowMissingColumns=True)

# 🔹 Criando um ID único para cada filme
df_filmes = df_filmes.withColumn("id_filme", F.monotonically_increasing_id())

# 🔹 Criando a DimAtores
dim_atores = df_filmes.selectExpr("id_filme", "nomeArtista as nome").distinct()
dim_atores = dim_atores.withColumn("id_ator", F.monotonically_increasing_id())
dim_atores = dim_atores.select("id_ator", "nome", "id_filme")

# 🔹 Criando a DimPersonagens
dim_personagens = df_filmes.selectExpr("id_filme", "personagem").distinct()
dim_personagens = dim_personagens.withColumn("id_personagem", F.monotonically_increasing_id())
dim_personagens = dim_personagens.select("id_personagem", "personagem", "id_filme")

# 🔹 Crianndo a DimDiretores 
dim_diretores = df_filmes.selectExpr("id_filme", "profissao", "nomeArtista") \
                         .filter(F.col("profissao") == "Director").distinct()
dim_diretores = dim_diretores.withColumn("id_diretor", F.monotonically_increasing_id())
dim_diretores = dim_diretores.select("id_diretor", "nomeArtista", "id_filme")

# 🔹 Criar a DimRoteiristas
dim_roteiristas = df_filmes.selectExpr("id_filme", "profissao", "nomeArtista") \
                           .filter(F.col("profissao") == "Writer").distinct()
dim_roteiristas = dim_roteiristas.withColumn("id_roteirista", F.monotonically_increasing_id())
dim_roteiristas = dim_roteiristas.select("id_roteirista", "nomeArtista", "id_filme")

# 🔹 Salvando tabelas corrigidas na camada Refined
dim_atores.write.mode("overwrite").parquet(f"{REFINED_PATH}DimAtores/")
dim_personagens.write.mode("overwrite").parquet(f"{REFINED_PATH}DimPersonagens/")
dim_diretores.write.mode("overwrite").parquet(f"{REFINED_PATH}DimDiretores/")
dim_roteiristas.write.mode("overwrite").parquet(f"{REFINED_PATH}DimRoteiristas/")

print("Processamento das dimensões concluído com sucesso!")
