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

# 🔹 Carregar dados locais (Movies e Series) garantindo o delimitador correto
df_local_movies = spark.read.option("header", "true").option("delimiter", "|").csv(f"{TRUSTED_LOCAL_PATH}Movies/")
df_local_series = spark.read.option("header", "true").option("delimiter", "|").csv(f"{TRUSTED_LOCAL_PATH}Series/")

# 🔹 Adicionando a origem dos dados
df_tmdb = df_tmdb.withColumn("origem", F.lit("TMDB"))
df_local_movies = df_local_movies.withColumn("origem", F.lit("Local"))
df_local_series = df_local_series.withColumn("origem", F.lit("Local"))

# 🔹 Unindo os dados de TMDB + CSVs Locais
df_filmes = df_tmdb.unionByName(df_local_movies, allowMissingColumns=True)
df_filmes = df_filmes.unionByName(df_local_series, allowMissingColumns=True)

# 🔹 Criando um ID único para cada filme
df_filmes = df_filmes.withColumn("id_filme", F.monotonically_increasing_id())

# 🔹 Criando DimAtores
dim_atores = df_filmes.selectExpr("id_filme", "nomeArtista as nome").distinct()
dim_atores = dim_atores.withColumn("id_ator", F.monotonically_increasing_id())
dim_atores = dim_atores.select("id_ator", "nome", "id_filme")

# 🔹 Criando DimPersonagens
dim_personagens = df_filmes.selectExpr("id_filme", "personagem").distinct()
dim_personagens = dim_personagens.withColumn("id_personagem", F.monotonically_increasing_id())
dim_personagens = dim_personagens.select("id_personagem", "personagem", "id_filme")

# 🔹 Criando DimDiretores
dim_diretores = df_filmes.selectExpr("id_filme", "profissao", "nomeArtista") \
                         .filter(F.col("profissao") == "Director").distinct()
dim_diretores = dim_diretores.withColumn("id_diretor", F.monotonically_increasing_id())
dim_diretores = dim_diretores.select("id_diretor", "nomeArtista", "id_filme")

# 🔹 Criando DimRoteiristas
dim_roteiristas = df_filmes.selectExpr("id_filme", "profissao", "nomeArtista") \
                           .filter(F.col("profissao") == "Writer").distinct()
dim_roteiristas = dim_roteiristas.withColumn("id_roteirista", F.monotonically_increasing_id())
dim_roteiristas = dim_roteiristas.select("id_roteirista", "nomeArtista", "id_filme")

# 🔹 Criando DimColecoes (agrupando os filmes por coleção)
dim_colecoes = df_filmes.selectExpr("id_filme", "tituloPrincipal as nome_colecao").distinct()
dim_colecoes = dim_colecoes.withColumn("id_colecao", F.monotonically_increasing_id())
dim_colecoes = dim_colecoes.select("id_colecao", "nome_colecao", "id_filme")

# 🔹 Criando DimDatas (extraindo ano, mês e dia do lançamento)
dim_datas = df_filmes.withColumn("ano", F.year(F.col("dataLancamento"))) \
                     .withColumn("mes", F.month(F.col("dataLancamento"))) \
                     .withColumn("dia", F.dayofmonth(F.col("dataLancamento"))) \
                     .select("id_filme", "ano", "mes", "dia").distinct()

# 🔹 Criando a Tabela Fato
fato_filmes = df_filmes.select(
    "id_filme",
    "genero",
    "notaMedia",
    "numeroVotos",
    "popularidade",
    "idiomaOriginal",
    "origem"
)

# 🔹 Salvando tabelas na camada Refined
dim_atores.write.mode("overwrite").parquet(f"{REFINED_PATH}DimAtores/")
dim_personagens.write.mode("overwrite").parquet(f"{REFINED_PATH}DimPersonagens/")
dim_diretores.write.mode("overwrite").parquet(f"{REFINED_PATH}DimDiretores/")
dim_roteiristas.write.mode("overwrite").parquet(f"{REFINED_PATH}DimRoteiristas/")
dim_colecoes.write.mode("overwrite").parquet(f"{REFINED_PATH}DimColecoes/")
dim_datas.write.mode("overwrite").parquet(f"{REFINED_PATH}DimDatas/")
fato_filmes.write.mode("overwrite").parquet(f"{REFINED_PATH}FatoFilmes/")

print("Processamento das dimensões e da tabela fato concluído com sucesso!")
