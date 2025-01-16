from pyspark import SparkContext

# Inicializar o SparkContext
sc = SparkContext("local", "Contador de Palavras")

# Carregar o arquivo
rdd = sc.textFile("/home/jovyan/Downloads/README.MD")

# Dividir o texto em palavras
palavras = rdd.flatMap(lambda line: line.split(" "))

# Filtrar palavras vazias ou espaços
palavras_filtradas = palavras.filter(lambda word: word.strip() != "")

# Contar as ocorrências de cada palavra
contador_palavras = palavras_filtradas.map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)

# Exibir os resultados
for palavra, contagem in contador_palavras.collect():
    print(f"{palavra}: {contagem}")
