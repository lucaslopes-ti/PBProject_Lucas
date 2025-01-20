import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql.functions import upper

args = getResolvedOptions(sys.argv, ['JOB_NAME', 'S3_INPUT_PATH', 'S3_TARGET_PATH'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

source_file = args['S3_INPUT_PATH']
target_file = args['S3_TARGET_PATH']

df = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": [source_file]},
    format="csv",
    format_options={"withHeader": True, "separator": ","},
)

df_spark = df.toDF()

df_spark.printSchema()

df_spark = df_spark.withColumn("nome", upper(df_spark["nome"]))

print(f"Contagem de linhas: {df_spark.count()}")

grouped = df_spark.groupBy("ano", "sexo").count()

grouped_sorted = grouped.orderBy("ano", ascending=False)

grouped_sorted.show()

female_names = df_spark.filter(df_spark['sexo'] == 'F')
most_frequent_female = female_names.groupBy("nome", "ano").count().orderBy("count", ascending=False).first()
print(f"Nome feminino com mais registros: {most_frequent_female['nome']} no ano {most_frequent_female['ano']}")

male_names = df_spark.filter(df_spark['sexo'] == 'M')
most_frequent_male = male_names.groupBy("nome", "ano").count().orderBy("count", ascending=False).first()
print(f"Nome masculino com mais registros: {most_frequent_male['nome']} no ano {most_frequent_male['ano']}")

total_by_year = df_spark.groupBy("ano").count().orderBy("ano", ascending=True).limit(10)
total_by_year.show()

dynamic_frame = DynamicFrame.fromDF(df_spark, glueContext, "dynamic_frame")

glueContext.write_dynamic_frame.from_options(
    frame=dynamic_frame,
    connection_type="s3",
    connection_options={"path": target_file + "/frequencia_registro_nomes_eua", "partitionKeys": ["sexo", "ano"]},
    format="json"
)

job.commit()
