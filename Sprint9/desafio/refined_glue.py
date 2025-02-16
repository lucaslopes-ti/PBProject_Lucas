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

# 🔹 Carregar dados do TMDB e Local (Unindo ambos)
df_tmdb = spark.read.parquet(f"{TRUSTED_TMDB_PATH}*/*/*/")
df_local = spark.read.parquet(f"{TRUSTED_LOCAL_PATH}Movies/")
df_series = spark.read.parquet(f"{TRUSTED_LOCAL_PATH}Series/")

df_filmes = df_tmdb.unionByName(df_local, allowMissingColumns=True)
df_filmes = df_filmes.unionByName(df_series, allowMissingColumns=True)

# 🔹 Criar tabelas dimensão
dim_atores = df_filmes.selectExpr("id as id_ator", "nomeArtista as nome").distinct()
dim_diretores = df_filmes.selectExpr("id as id_diretor", "profissao").filter(F.col("profissao") == "Director").distinct()
dim_roteiristas = df_filmes.selectExpr("id as id_roteirista", "profissao").filter(F.col("profissao") == "Writer").distinct()
dim_personagens = df_filmes.selectExpr("id as id_personagem", "personagem").distinct()
dim_colecoes = df_filmes.selectExpr("id as id_colecao", "tituloPincipal as nome_colecao").distinct()
dim_datas = df_filmes.selectExpr("year(release_date) as ano", "month(release_date) as mes", "day(release_date) as dia").distinct()

# 🔹 Criar tabela fato
fato_filmes = df_filmes.select(
    "id",
    "genero",
    "notaMedia",
    "numeroVotos",
    "popularidade",
    "original_language"
)

# 🔹 Salvando tabelas na camada Refined
dim_atores.write.mode("overwrite").parquet(f"{REFINED_PATH}DimAtores/")
dim_diretores.write.mode("overwrite").parquet(f"{REFINED_PATH}DimDiretores/")
dim_roteiristas.write.mode("overwrite").parquet(f"{REFINED_PATH}DimRoteiristas/")
dim_personagens.write.mode("overwrite").parquet(f"{REFINED_PATH}DimPersonagens/")
dim_colecoes.write.mode("overwrite").parquet(f"{REFINED_PATH}DimColecoes/")
dim_datas.write.mode("overwrite").parquet(f"{REFINED_PATH}DimDatas/")
fato_filmes.write.mode("overwrite").parquet(f"{REFINED_PATH}FatoFilmes/")

print("Processamento da camada Refined concluído com sucesso!")
