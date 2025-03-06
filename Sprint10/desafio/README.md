## Desafio - Construção da Dashboard do Studio Ghibli no QuickSight

### Introdução

Este desafio teve como objetivo a criação de uma dashboard interativa no Amazon QuickSight para analisar os filmes do Studio Ghibli. A partir da coleta e tratamento de dados no AWS Glue, estruturamos um modelo dimensional e criamos visualizações que permitem extrair insights sobre os filmes do estúdio.

### Objetivo

O objetivo foi processar e disponibilizar os dados do Studio Ghibli no QuickSight, utilizando o Data Lake no AWS S3 como repositório e o AWS Glue para transformar e estruturar os dados. Além disso, buscamos criar visualizações significativas para entender a popularidade, avaliações e outros padrões nos filmes do estúdio.

### Etapas do Desafio

#### 1. Coleta e Tratamento dos Dados

Os dados foram coletados de diferentes fontes e armazenados no S3:

- JSON do TMDB contendo informações sobre os filmes do Studio Ghibli:
  ```
  s3://data-lake-desafio/Raw/TMDB/JSON/2025/02/25/studio_ghibli_movies_1.json
  ```

- Arquivos CSV de filmes e séries gerais:
  ```
  s3://data-lake-desafio/Raw/Local/CSV/Movies/2025/01/05/movies.csv
  s3://data-lake-desafio/Raw/Local/CSV/Series/2025/01/05/series.csv
  ```

#### 2. Modelagem Dimensional

Para garantir um melhor desempenho na análise, seguimos uma abordagem de modelagem dimensional, criando tabelas Fato e Dimensão:

- **Fato Produção:** Contendo os principais dados sobre cada filme, como título, ano de lançamento, média de votos e popularidade.
- **Dimensão Filme:** Tabela separada para consolidar informações específicas dos filmes.
- **Dimensão Tempo:** Permite analisar as produções por ano de lançamento.
- **Dimensão Artista:** Contendo os diretores e roteiristas envolvidos nas produções.
- **Dimensão Gênero:** Criada para categorizar os filmes de acordo com seus gêneros principais.

#### 3. Criação da Camada Refined

Os dados foram processados e estruturados na camada Refined:
```
s3://data-lake-desafio/Refined/
```
As tabelas criadas incluem:
- `dim_filme`
- `dim_tempo`
- `dim_artista`
- `dim_genero`
- `fato_producao`

#### 4. Construção da Dashboard no QuickSight

A partir das tabelas estruturadas, importamos os dados para o QuickSight e criamos visualizações interativas. Os principais gráficos criados incluem:

- **Métricas Principais (Cards numéricos):** Total de filmes, média de avaliação, período de lançamento mais longo.
- **Gráfico de Linhas:** Evolução dos lançamentos ao longo dos anos.
- **Gráfico de Dispersão:** Relação entre popularidade e avaliação.
- **Gráfico de Barras Horizontais:** Distribuição dos idiomas dos filmes.
- **Tabela Interativa:** Top 10 filmes melhor avaliados.
- **Nuvem de Palavras:** Análise das palavras mais frequentes nas sinopses.

#### 5. Filtros e Personalização

- Criamos **filtros interativos** para selecionar filmes por ano de lançamento, idioma e nota.
- Implementamos um campo calculado para classificação das notas:
  ```
  ifelse(
      {vote_average} >= 8.5, 'Best',
      {vote_average} >= 7.0, 'Excellent',
      {vote_average} >= 5.0, 'Good',
      'Below Avg'
  )
  ```

### Resultados e Insights

Os principais insights extraídos incluem:
- A maioria dos filmes do Studio Ghibli tem avaliações acima de 7.0.
- Os filmes mais populares não são necessariamente os mais bem avaliados.
- O estúdio teve períodos de lançamentos mais frequentes em determinadas décadas.

### Erros e Soluções

1. **Registros duplicados**: Identificamos duplicatas na tabela fato, o que impactava nas contagens dos filmes. Solução: aplicar `dropDuplicates()` no Spark.
2. **Falta de gêneros nos filmes do TMDB**: Criamos uma nova tabela de dimensão para categorizar os filmes corretamente.
3. **Problema no filtro de anos**: Corrigido convertendo a coluna de data para o formato adequado.

### Conclusão

O desafio proporcionou uma experiência prática na construção de dashboards interativas com o Amazon QuickSight, estruturando um Data Lake e criando uma modelagem dimensional eficiente. O resultado final permitiu explorar de forma intuitiva os dados do Studio Ghibli e gerar insights valiosos sobre seus filmes.

