# Descrição do Projeto de Normalização e Modelo Dimensional

Este projeto tem como objetivo aplicar conceitos de normalização e modelagem dimensional em um banco de dados de uma concessionária. O desafio consiste em transformar uma tabela inicial ampla, `tb_locacao`, que contém dados de clientes, carros, vendedores, combustíveis e informações de locação, em um modelo de banco de dados eficiente e estruturado. O projeto abrange as etapas de criação de um modelo normalizado, estruturação de um modelo dimensional para análise, criação de scripts SQL, e enfrentamento de dificuldades técnicas ao longo do processo.

## Etapa 1: Análise e Normalização da Tabela `tb_locacao`

### Análise da Tabela Inicial

A tabela `tb_locacao` fornecida originalmente continha dados mistos sobre várias entidades diferentes, como clientes, carros, vendedores e locações. Manter esses dados em uma única tabela gerava redundâncias e dificultava a manutenção e a escalabilidade do banco. Para resolver esse problema, a primeira etapa foi identificar as entidades principais e dividir as colunas da tabela `tb_locacao` em tabelas menores, focadas em uma única entidade.

As principais entidades identificadas foram:

- **Cliente**: Inclui dados relacionados aos clientes, como `idCliente`, `nomeCliente`, `cidadeCliente`, `estadoCliente` e `paisCliente`.
- **Carro**: Inclui dados sobre os carros, como `idCarro`, `kmCarro`, `classiCarro`, `marcaCarro` e `anoCarro`.
- **Combustível**: Representa os tipos de combustível, com `idcombustivel` e `tipoCombustivel`.
- **Vendedor**: Inclui informações sobre os vendedores, como `idVendedor`, `nomeVendedor`, `sexoVendedor` e `estadoVendedor`.
- **Locação**: A tabela central que conecta todas as outras, contendo dados da transação de locação.

![evidencia](../evidencias/tabela_relacional.png)

### Processo de Normalização

Para evitar redundâncias e garantir a integridade referencial, aplicamos as seguintes etapas de normalização:

1. **Primeira Forma Normal (1NF)**: Eliminamos grupos repetidos. Cada tabela representa uma única entidade com colunas atômicas, ou seja, sem valores compostos ou múltiplos.
2. **Segunda Forma Normal (2NF)**: Garantimos que cada tabela depende da chave primária. Criamos uma chave primária para cada tabela, como `idCliente` em `Cliente` e `idCarro` em `Carro`, garantindo que cada coluna seja dependente de sua chave.
3. **Terceira Forma Normal (3NF)**: Removemos dependências transitivas. Em `Locacao`, por exemplo, as informações do cliente, carro, combustível e vendedor foram referenciadas por chaves estrangeiras, eliminando qualquer dependência transitiva.

### Estrutura Final Normalizada

Após o processo de normalização, criamos as seguintes tabelas:

- **Cliente**: Para armazenar informações dos clientes.
- **Carro**: Para os detalhes de cada carro.
- **Combustível**: Para os tipos de combustível utilizados.
- **Vendedor**: Para as informações sobre cada vendedor.
- **Locação**: Como tabela central, conectando todas as outras por meio de chaves estrangeiras.

Cada uma dessas tabelas foi criada utilizando scripts SQL com as colunas definidas de acordo com as necessidades de cada entidade, e as chaves estrangeiras foram estabelecidas para garantir integridade referencial.

## Etapa 2: Modelo Dimensional

Após a normalização, o próximo passo foi construir um modelo dimensional para facilitar análises e relatórios. O modelo dimensional é composto de uma tabela de fatos e várias tabelas de dimensões.

### Estrutura do Modelo Dimensional

- **Fato_Locacao**: A tabela de fatos central, `Fato_Locacao`, armazena dados quantitativos das locações, como o valor da diária e a quantidade de diárias. Esta tabela se conecta a todas as tabelas de dimensão por meio de chaves estrangeiras.
- **Dimensões**: Criamos as dimensões para descrever o contexto dos fatos:
    - **Dim_Cliente**: Descreve as informações dos clientes.
    - **Dim_Carro**: Descreve os detalhes dos carros.
    - **Dim_Combustivel**: Descreve os tipos de combustível.
    - **Dim_Vendedor**: Descreve os detalhes dos vendedores.

Para implementar o modelo dimensional, optamos por criar views no banco de dados. Cada view (como `Fato_Locacao`, `Dim_Cliente`, `Dim_Carro`, etc.) foi projetada para agregar informações de forma lógica, sem alterar as tabelas subjacentes.

## Principais Dificuldades e Soluções

### Dificuldade 1: Duplicidade de Dados na Tabela Carro

Durante a inserção de dados normalizados, um problema de duplicidade foi encontrado na tabela `Carro`, onde alguns registros de `idCarro` apareciam múltiplas vezes na tabela original `tb_locacao`. Isso causou um erro de chave primária ao tentar inserir esses dados na tabela `Carro`. Para solucionar isso, usamos uma subconsulta com `GROUP BY` para selecionar apenas o primeiro registro de cada `idCarro`, eliminando duplicatas.

### Dificuldade 2: Visualização dos Relacionamentos no ER Diagram

No DBeaver, um problema surgiu ao tentar visualizar os relacionamentos entre as views do modelo dimensional (`Fato_Locacao` e `Dim_*`). Como as views não suportam diretamente chaves estrangeiras, não foi possível exibir as linhas de relacionamento no diagrama ER. Para contornar isso, criamos tabelas temporárias e adicionamos chaves estrangeiras a elas para simular o relacionamento e visualizar a estrutura completa.

### Dificuldade 3: Estruturação do Script SQL e Organização das Dependências

Outro desafio foi organizar a criação das tabelas e views no script SQL para que as dependências fossem respeitadas. Como a tabela `Locacao` depende das outras tabelas normalizadas (`Cliente`, `Carro`, `Combustível` e `Vendedor`), foi essencial garantir que essas tabelas fossem criadas antes. Além disso, as views do modelo dimensional foram criadas após a criação do modelo relacional.

## Estrutura Final do Código SQL

Para facilitar a execução e manutenção, o código SQL foi dividido em duas partes:

- **Estruturas Normalizadas**: Criação das tabelas `Cliente`, `Carro`, `Combustivel`, `Vendedor` e `Locacao`, com suas respectivas chaves estrangeiras.
- **Estruturas Dimensionalizadas**: Criação das views `Fato_Locacao`, `Dim_Cliente`, `Dim_Carro`, `Dim_Combustivel`, e `Dim_Vendedor`, seguindo o modelo dimensional.

Essas etapas foram implementadas no DBeaver, e cada script foi testado e ajustado para garantir integridade referencial e consistência de dados.

## Conclusão

Este projeto foi uma prática essencial para consolidar conhecimentos sobre normalização e modelagem dimensional. A aplicação das formas normais nos permitiu dividir os dados em estruturas otimizadas e evitar redundâncias. Em seguida, o modelo dimensional facilitou a organização de dados para análise e relatórios.

As principais dificuldades enfrentadas — duplicidade de dados, visualização de relacionamentos e organização dos scripts — foram resolvidas com estratégias de agrupamento e criação de tabelas temporárias, proporcionando uma estrutura final consistente e adequada para análise e manutenção. Este trabalho reforça a importância de planejar cuidadosamente a estrutura de um banco de dados para maximizar eficiência e flexibilidade em diferentes cenários de uso.
