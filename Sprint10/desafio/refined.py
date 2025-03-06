import sys
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from pyspark.sql import functions as F
from pyspark.sql.types import IntegerType, FloatType, StringType, DateType

# 🚀 Inicializando o contexto do Glue
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# 🗂️ Caminhos das zonas
RAW_LOCAL_MOVIES_PATH = "s3://data-lake-desafio/Raw/Local/CSV/Movies/2025/01/05/movies.csv"
RAW_LOCAL_SERIES_PATH = "s3://data-lake-desafio/Raw/Local/CSV/Series/2025/01/05/series.csv"
RAW_TMDB_JSON_PATH = "s3://data-lake-desafio/Raw/TMDB/JSON/2025/01/28/movies_2000_to_2025.json"

dest_base_path = "s3://data-lake-desafio"

# Caminhos das tabelas finais
atores_path = f"{dest_base_path}/Refined/DimAtores/"
diretores_path = f"{dest_base_path}/Refined/DimDiretores/"
roteiristas_path = f"{dest_base_path}/Refined/DimRoteiristas/"
personagens_path = f"{dest_base_path}/Refined/DimPersonagens/"
filmes_path = f"{dest_base_path}/Refined/DimFilmes/"
tempo_path = f"{dest_base_path}/Refined/DimTempo/"
fato_path = f"{dest_base_path}/Refined/FatoFilmes/"

# 🔎 Função para criar dimensão de tempo
def criar_dim_tempo(df, coluna_data):
    return (
        df.withColumn("ano", F.year(F.to_date(coluna_data, "yyyy-MM-dd")))
          .withColumn("mes", F.month(F.to_date(coluna_data, "yyyy-MM-dd")))
          .withColumn("dia", F.dayofmonth(F.to_date(coluna_data, "yyyy-MM-dd")))
          .select("ano", "mes", "dia")
          .distinct()
          .withColumn("id_tempo", F.monotonically_increasing_id())
    )

# 📥 Carregar dados das fontes
df_local_movies = spark.read.option("header", "true").option("delimiter", "|").csv(RAW_LOCAL_MOVIES_PATH)
df_local_series = spark.read.option("header", "true").option("delimiter", "|").csv(RAW_LOCAL_SERIES_PATH)
df_tmdb = spark.read.option("multiline", "true").json(RAW_TMDB_JSON_PATH)

# 🧹 Limpeza e padronização dos DataFrames locais
df_local_movies = df_local_movies.withColumnRenamed("tituloPincipal", "tituloPrincipal")
df_local_series = df_local_series.withColumnRenamed("tituloPincipal", "tituloPrincipal")

# 🔄 Ajustando DataFrame do TMDB
# 🔄 Ajustando DataFrame do TMDB
df_tmdb = df_tmdb.withColumnRenamed("title", "tituloPrincipal") \
                 .withColumnRenamed("vote_average", "notaMedia") \
                 .withColumnRenamed("vote_count", "numeroVotos")

# ✅ Verificação da coluna release_date antes de processar anoLancamento
if "release_date" in df_tmdb.columns:
    df_tmdb = df_tmdb.withColumn("anoLancamento", F.year(F.to_date("release_date", "yyyy-MM-dd")))
else:
    df_tmdb = df_tmdb.withColumn("anoLancamento", F.lit(None).cast(IntegerType()))

# Continuação do processamento
df_tmdb = (
    df_tmdb.withColumn("genero", F.when(F.col("genres").isNotNull(), F.expr("concat_ws(',', genres)"))
                                 .otherwise(F.lit(None)))
           .withColumn("tituloOriginal", F.lit(None).cast(StringType()))
           .withColumn("tempoMinutos", F.lit(None).cast(IntegerType()))
           .withColumn("personagem", F.lit(None).cast(StringType()))
           .withColumn("nomeArtista", F.lit(None).cast(StringType()))
           .withColumn("profissao", F.lit(None).cast(StringType()))
           .withColumn("origem", F.lit("TMDB"))
           .select("id", "tituloPrincipal", "tituloOriginal", "anoLancamento", "tempoMinutos", 
                   "genero", "notaMedia", "numeroVotos", "personagem", "nomeArtista", "profissao", "origem")
)



# 📅 Criando dimensão de tempo com base na data de lançamento
dim_tempo = criar_dim_tempo(df_tmdb.withColumn("data_lancamento", F.to_date("release_date", "yyyy-MM-dd")), "data_lancamento")
dim_tempo.write.mode("overwrite").parquet(tempo_path)

# 🗄️ Criando dimensões
## DimFilmes
dim_filmes = df_tmdb.select("id", "tituloPrincipal", "anoLancamento", "genero").withColumnRenamed("id", "id_filme")
dim_filmes.write.mode("overwrite").parquet(filmes_path)

## DimAtores
dim_atores = df_local_movies.select("nomeArtista").filter(F.col("nomeArtista").isNotNull()).distinct().withColumn("id_ator", F.monotonically_increasing_id())
dim_atores.write.mode("overwrite").parquet(atores_path)

## DimDiretores
dim_diretores = df_local_movies.filter(F.col("profissao") == "director") \
    .select("nomeArtista").distinct().withColumn("id_diretor", F.monotonically_increasing_id())
dim_diretores.write.mode("overwrite").parquet(diretores_path)

## DimRoteiristas
dim_roteiristas = df_local_movies.filter(F.col("profissao") == "writer") \
    .select("nomeArtista").distinct().withColumn("id_roteirista", F.monotonically_increasing_id())
dim_roteiristas.write.mode("overwrite").parquet(roteiristas_path)

## DimPersonagens
dim_personagens = df_local_movies.select("personagem").filter(F.col("personagem").isNotNull()).distinct().withColumn("id_personagem", F.monotonically_increasing_id())
dim_personagens.write.mode("overwrite").parquet(personagens_path)

# 🧩 Criando a tabela fato com chaves estrangeiras
df_fato = (
    df_tmdb.alias("filmes")
    .join(dim_filmes.alias("dim_filmes"), F.col("filmes.tituloPrincipal") == F.col("dim_filmes.tituloPrincipal"), "left")
    .join(dim_tempo.alias("dim_tempo"), F.col("filmes.anoLancamento") == F.col("dim_tempo.ano"), "left")
    .select(
        F.monotonically_increasing_id().alias("id_fato"),
        F.col("dim_filmes.id_filme"),
        F.col("dim_tempo.id_tempo"),
        "notaMedia",
        "numeroVotos"
    )
)

df_fato.write.mode("overwrite").parquet(fato_path)

print("Tabelas fato e dimensões geradas e salvas com sucesso!")
