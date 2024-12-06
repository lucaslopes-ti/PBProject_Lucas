import csv

def processar_notas(arquivo_csv):
    with open(arquivo_csv, 'r', encoding = 'utf-8') as file:
        leitor_csv = csv.reader(file)
        
        relatorio = []
        
        for linha in leitor_csv:
            nome = linha[0]
            notas = list(map(int, linha[1:]))
            
            maiores_notas = sorted(notas, reverse = True)[:3]
            
            media = round(sum(maiores_notas) / 3, 2)
            
            
            relatorio.append((nome, maiores_notas, media))
            
            
        relatorio.sort(key = lambda x: x[0])
        
        for nome, maiores_notas, media in relatorio:
          print(f"Nome: {nome} Notas: {maiores_notas} Média: {media}")
          
arquivo = "estudantes.csv"
          
processar_notas(arquivo)