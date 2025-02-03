from pyspark.sql import SparkSession
from pyspark import SparkContext, SQLContext
import random

# Etapa 1: Criar Spark Session
spark = SparkSession.builder \
    .master("local[*]") \
    .appName("Exercicio Intro") \
    .getOrCreate()

# Ler o arquivo CSV
caminho_arquivo = "/home/boltzmann/Documents/PBProject_Lucas/Sprint8/exercicios/nomes_aleatorios.txt"
df_nomes = spark.read.csv(caminho_arquivo, header=False, inferSchema=True)
df_nomes = df_nomes.withColumnRenamed("_c0", "Nomes")

df_nomes.show(5)
print("Esquema do DataFrame inicial:")
df_nomes.printSchema()

# Etapa 3: Adicionar coluna "Escolaridade" com valores aleatórios
def gerar_escolaridade():
    return random.choice(["Fundamental", "Medio", "Superior"])

gerar_escolaridade_udf = spark.udf.register("gerar_escolaridade", gerar_escolaridade)
df_nomes = df_nomes.withColumn("Escolaridade", gerar_escolaridade_udf())

df_nomes.show(5)

# Etapa 4: Adicionar coluna "Pais" com valores aleatórios
paises = ["Argentina", "Bolivia", "Brasil", "Chile", "Colombia", "Equador", "Guiana", "Paraguai", "Peru", "Suriname", "Uruguai", "Venezuela"]
def gerar_pais():
    return random.choice(paises)

gerar_pais_udf = spark.udf.register("gerar_pais", gerar_pais)
df_nomes = df_nomes.withColumn("Pais", gerar_pais_udf())

df_nomes.show(5)

# Etapa 5: Adicionar coluna "AnoNascimento" com valores aleatórios
def gerar_ano():
    return random.randint(1945, 2010)

gerar_ano_udf = spark.udf.register("gerar_ano", gerar_ano)
df_nomes = df_nomes.withColumn("AnoNascimento", gerar_ano_udf())

df_nomes.show(5)

# Etapa 6: Filtrar pessoas nascidas neste século (>= 2000)
df_select = df_nomes.filter(df_nomes.AnoNascimento >= 2000)
df_select.show(10)

# Etapa 7: Usar Spark SQL para filtrar pessoas nascidas neste século
df_nomes.createOrReplaceTempView("pessoas")
sql_result = spark.sql("SELECT * FROM pessoas WHERE AnoNascimento >= 2000")
sql_result.show(10)

# Etapa 8: Contar Millennials (1980-1994) usando método filter
millennials_count = df_nomes.filter((df_nomes.AnoNascimento >= 1980) & (df_nomes.AnoNascimento <= 1994)).count()
print(f"Número de Millennials: {millennials_count}")

# Etapa 9: Contar Millennials usando Spark SQL
sql_millennials_count = spark.sql(
    """
    SELECT COUNT(*) as qtd FROM pessoas
    WHERE AnoNascimento >= 1980 AND AnoNascimento <= 1994
    """
)
sql_millennials_count.show()

# Etapa 10: Quantidade de pessoas por país e geração
geracoes = """
    CASE 
        WHEN AnoNascimento BETWEEN 1944 AND 1964 THEN 'Baby Boomers'
        WHEN AnoNascimento BETWEEN 1965 AND 1979 THEN 'Geracao X'
        WHEN AnoNascimento BETWEEN 1980 AND 1994 THEN 'Millennials'
        WHEN AnoNascimento BETWEEN 1995 AND 2015 THEN 'Geracao Z'
        ELSE 'Outros'
    END AS Geracao
"""
sql_geracoes = spark.sql(
    f"""
    SELECT Pais, {geracoes}, COUNT(*) as Quantidade
    FROM pessoas
    GROUP BY Pais, {geracoes}
    ORDER BY Pais, Geracao, Quantidade
    """
)
sql_geracoes.show()
