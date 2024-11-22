# Função para a Etapa 1
def etapa_1():
    with open('actors.csv', 'r', encoding='utf-8') as file:
        header = file.readline()  # ignorar cabeçalho
        max_movies = 0
        actor_with_max_movies = ""

        for line in file:
            # dividindo a linha
            columns = [col.strip() for col in line.strip().split(',')]
            
            # verificando se qtd de colunas esta correta
            if len(columns) < 6:
                print(f"Erro ao processar linha: {line}")
                continue

            actor = columns[0]
            try:
                number_of_movies = int(columns[2])
            except ValueError:
                print(f"Erro ao converter o número de filmes na linha: {line}")
                continue

            if number_of_movies > max_movies:
                max_movies = number_of_movies
                actor_with_max_movies = actor

    with open('etapa-1.txt', 'w', encoding='utf-8') as output:
        output.write(f"{actor_with_max_movies}: {max_movies} filmes")
    print("Etapa 1 concluída! Resultado salvo em 'etapa-1.txt'.")


# Função para a Etapa 2
def etapa_2():
    with open('actors.csv', 'r', encoding='utf-8') as file:
        header = file.readline()  # Ignorar cabeçalho
        total_gross = 0
        count = 0

        for line in file:
            columns = [col.strip() for col in line.strip().split(',')]

            # Verificar se a coluna 'Gross' existe e é válida
            try:
                gross = float(columns[5])  # coluna 'Gross' está no índice 5
                total_gross += gross
                count += 1
            except (ValueError, IndexError):
                print(f"Erro ao processar linha: {line}")
                continue

    # Calcular a média
    if count > 0:
        average_gross = total_gross / count
    else:
        average_gross = 0

    with open('etapa-2.txt', 'w', encoding='utf-8') as output:
        output.write(f"Média de receita bruta dos principais filmes: {average_gross:.2f} milhões de dólares")
    print("Etapa 2 concluída! Resultado salvo em 'etapa-2.txt'.")


def etapa_3():
    with open('actors.csv', 'r', encoding='utf-8') as file:
        header = file.readline()  
        max_average = 0
        actor_with_max_average = ""

        for line in file:
            columns = [col.strip() for col in line.strip().split(',')]

            # Verificar se a coluna 'Average per Movie' existe e é válida
            try:
                average_per_movie = float(columns[3])  # Coluna 'Average per Movie' está no índice 3
                actor = columns[0]

                # Verificar se é a maior média encontrada até agora
                if average_per_movie > max_average:
                    max_average = average_per_movie
                    actor_with_max_average = actor
            except (ValueError, IndexError):
                print(f"Erro ao processar linha: {line}")
                continue

    # salvando o resultado no arquivo etapa-3
    with open('etapa-3.txt', 'w', encoding='utf-8') as output:
        output.write(f"{actor_with_max_average}: {max_average:.2f} milhões de dólares por filme")
    print("Etapa 3 concluída! Resultado salvo em 'etapa-3.txt'.")


from collections import Counter

def etapa_4():
    with open('actors.csv', 'r', encoding='utf-8') as file:
        header = file.readline()  # Ignorar cabeçalho
        movie_count = Counter()  # Usar Counter para contar as aparições dos filmes

        for line in file:
            # Dividir a linha preservando os campos corretamente
            columns = [col.strip() for col in line.strip().split(',')]

            # Verificar se a coluna '#1 Movie' existe
            try:
                movie = columns[4]  # Coluna '#1 Movie' está no índice 4
                movie_count[movie] += 1
            except IndexError:
                print(f"Erro ao processar linha: {line}")
                continue

    # Ordenar por quantidade (decrescente) e nome do filme (alfabético)
    sorted_movies = sorted(movie_count.items(), key=lambda x: (-x[1], x[0]))

    # Escrever o resultado no arquivo etapa-4.txt
    with open('etapa-4.txt', 'w', encoding='utf-8') as output:
        for idx, (movie, count) in enumerate(sorted_movies, start=1):
            output.write(f"{idx} - O filme ({movie}) aparece {count} vez(es) no dataset.\n")
    print("Etapa 4 concluída! Resultado salvo em 'etapa-4.txt'.")


# Função para a Etapa 5
def etapa_5():
    with open('actors.csv', 'r', encoding='utf-8') as file:
        header = file.readline()  # Ignorar cabeçalho
        actors = []

        for line in file:
            # Dividir a linha preservando os campos corretamente
            columns = [col.strip() for col in line.strip().split(',')]

            # Verificar se a coluna 'Total Gross' existe e é válida
            try:
                actor = columns[0]
                total_gross = float(columns[1])  # Coluna 'Total Gross' está no índice 1
                actors.append((actor, total_gross))
            except (ValueError, IndexError):
                print(f"Erro ao processar linha: {line}")
                continue

    # Ordenar pela receita total bruta (decrescente)
    sorted_actors = sorted(actors, key=lambda x: -x[1])

    # Escrever o resultado no arquivo etapa-5.txt
    with open('etapa-5.txt', 'w', encoding='utf-8') as output:
        for idx, (actor, total_gross) in enumerate(sorted_actors, start=1):
            output.write(f"{idx} - {actor} - {total_gross:.2f} milhões de dólares\n")
    print("Etapa 5 concluída! Resultado salvo em 'etapa-5.txt'.")


# Menu para escolher qual etapa executar
def menu():
    while True:
        print("\nEscolha uma etapa para executar:")
        print("1 - Etapa 1")
        print("2 - Etapa 2")
        print("3 - Etapa 3")
        print("4 - Etapa 4")
        print("5 - Etapa 5")
        print("0 - Sair")

        escolha = input("Digite o número da etapa: ")

        if escolha == '1':
            etapa_1()
        elif escolha == '2':
            etapa_2()
        elif escolha == '3':
            etapa_3()
        elif escolha == '4':
            etapa_4()
        elif escolha == '5':
            etapa_5()
        elif escolha == '0':
            print("Saindo...")
            break
        else:
            print("Opção inválida! Tente novamente.")

# Executar o menu principal
if __name__ == "__main__":
    menu()
