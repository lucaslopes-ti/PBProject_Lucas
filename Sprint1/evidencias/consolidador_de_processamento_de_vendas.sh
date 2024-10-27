#!/bin/bash

# Caminho para o diretório correto onde os backups estão localizados
backup_dir="/home/boltzmann/Documents/ecommerce/vendas/vendas/backup/"

# Arquivo final de consolidação
output_file="${backup_dir}relatorio_final.txt"

# Verifique se o diretório de backup existe
if [ ! -d "$backup_dir" ]; then
    echo "Diretório de backup não encontrado: $backup_dir"
    exit 1
fi

# Cria (ou limpa) o arquivo relatorio_final.txt
touch "$output_file"
> "$output_file"

# Consolida todos os relatórios gerados
for file in "$backup_dir"relatorio-*.txt; do
    if [ -f "$file" ]; then
        echo "Consolidando: $file" >> "$output_file"
        cat "$file" >> "$output_file"
        echo -e "\n" >> "$output_file"
    fi
done

echo "Consolidação concluída. Arquivo final gerado em: $output_file"

