# Resumo da Sprint 7

## **Instruções/Informações/Anotações**

Nesta sprint, o objetivo principal foi trabalhar com ingestão e transformação de dados utilizando serviços AWS como Lambda, S3, Glue e Spark. Além disso, consolidamos o conhecimento sobre integração de APIs, automação de pipelines e manipulação de dados em larga escala para análise.

---

## **Exercícios**

### **Exercício 1: Contador de Palavras com PySpark**
#### **Objetivo**
Desenvolver um programa utilizando PySpark para contar palavras em um arquivo README e exibir as palavras mais frequentes.

#### **Etapas Realizadas**
1. Configurado o ambiente local com PySpark.
2. Lido o arquivo README e dividido o texto em palavras.
3. Aplicado transformação para contar ocorrências de cada palavra.
4. Exibido o resultado com as palavras mais frequentes em ordem decrescente.

---

### **Exercício 2: ETL com PySpark**

Exercício 3: ETL com AWS Glue

Objetivo

Utilizar o AWS Glue para realizar ETL nos dados brutos da RAW Zone e salvá-los na Curated Zone.
Etapas Realizadas

    Configurado um Crawler no Glue para catalogar os dados brutos no S3.
    Criado um Job no AWS Glue com PySpark para:
        Remover dados inconsistentes.
        Normalizar colunas (ex.: formato de data).
        Salvar os dados transformados no formato Parquet.
    Configurado o job para rodar periodicamente com triggers.

---

## **Desafio - Ingestão e Armazenamento de Dados com Lambda e S3**

### **Introdução**

O desafio foi focado na ingestão de dados da API TMDB e no armazenamento estruturado no S3, criando um pipeline automatizado com AWS Lambda. A proposta foi integrar dados de filmes e séries dos gêneros **Comédia** e **Animação**, lançados de 2000 até o presente.

### **Objetivo**

Criar um pipeline que consome dados da API TMDB, automatiza o upload no S3 e prepara os dados para futuras análises.

### **Etapas do Desafio**

1. **Configuração Inicial**
   - Criado o bucket `data-lake-desafio` no S3 com as zonas:
     - **RAW Zone**: Para dados brutos (JSON).
     - **Curated Zone**: Para dados transformados.

2. **Desenvolvimento da Função Lambda**
   - Criada uma função Lambda para consumir dados da API TMDB.
   - Configurado o caminho de salvamento: `raw/tmdb/json/movies_2000_to_2025.json`.

3. **Configuração de Layers**
   - Criada uma Layer no Lambda para incluir a biblioteca `requests`.

4. **Automação com EventBridge**
   - Configurado o AWS EventBridge para executar a Lambda periodicamente.

5. **Validação**
   - Dados foram salvos corretamente no S3 e estão prontos para transformação.

**Evidências**:

Execução do Lambda:

![Lambda Execução](../Sprint7/evidencias/execucao_lambda_tmbd.png)

Dados no S3:

![S3 Dados](../Sprint7/evidencias/execucao_s3_tmdb.png)

---

## **Perguntas para a Dashboard**

1. **Qual é a média das notas (vote_average) por ano e por gênero?**
2. **Quais são os filmes mais populares em Comédia e Animação?**
3. **Existe uma correlação entre o número de votos (vote_count) e a popularidade (popularity)?**
4. **Quais são os idiomas predominantes nos filmes de cada gênero?**
5. **Quais são os gêneros mais bem avaliados em média ao longo dos anos?**

---

## **Impressões Pessoais**

Achei esta sprint extremamente produtiva e desafiadora, principalmente ao integrar diversos serviços AWS, como Lambda, S3, Glue e Spark. As dificuldades, como manipulação de dados e configuração de permissões, proporcionaram aprendizados valiosos. A prática consolidou minha habilidade de criar pipelines escaláveis e integrações eficientes na nuvem.

