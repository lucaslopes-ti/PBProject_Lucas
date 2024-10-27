#!/bin/bash

# Definir o diretório de origem e destino
ecommerce_dir="/home/boltzmann/Documents/ecommerce"
vendas_dir="vendas"
backup_dir="vendas/backup"

# Criar diretório de vendas e copiar arquivo de vendas
mkdir -p $vendas_dir
cp $ecommerce_dir/dados_de_vendas.csv $vendas_dir/

# Entrar no diretório de vendas e criar subdiretório de backup
cd $vendas_dir
mkdir -p $backup_dir

# Definir a data de execução no formato yyyyMMdd
data_execucao=$(date +%Y%m%d)

# Fazer uma cópia do arquivo dados_de_vendas.csv para o diretório de backup com a data no nome
cp dados_de_vendas.csv $backup_dir/dados-$data_execucao.csv

# Renomear o arquivo no diretório de backup
mv $backup_dir/dados-$data_execucao.csv $backup_dir/backup-dados-$data_execucao.csv

# Gerar o relatório e salvá-lo com a data no nome (relatorio-<data>.txt)
relatorio="$backup_dir/relatorio-$data_execucao.txt"
echo "Data do sistema: $(date '+%Y/%m/%d %H:%M')" > $relatorio
echo "Data do primeiro registro de venda: $(head -n 2 dados_de_vendas.csv | tail -n 1 | cut -d',' -f5)" >> $relatorio
echo "Data do último registro de venda: $(tail -n 1 dados_de_vendas.csv | cut -d',' -f5)" >> $relatorio
echo "Quantidade total de itens diferentes vendidos: $(wc -l < dados_de_vendas.csv)" >> $relatorio
echo "Primeiras 10 linhas do arquivo:" >> $relatorio
head -n 11 $backup_dir/backup-dados-$data_execucao.csv >> $relatorio

# Compactar o arquivo de backup e remover o original
zip $backup_dir/backup-dados-$data_execucao.zip $backup_dir/backup-dados-$data_execucao.csv
rm $backup_dir/backup-dados-$data_execucao.csv

# Remover o arquivo de vendas original
rm dados_de_vendas.csv

