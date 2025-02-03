import requests
import pandas as pd


api_key = "1e8aa6dc5579d131ff74414300b05165"

# URL base da API TMDB
base_url = "https://api.themoviedb.org/3"

# Função para obter filmes mais bem avaliados
def obter_filmes_top_rated(api_key, language="pt-BR"):
    endpoint = f"{base_url}/movie/top_rated"
    params = {
        "api_key": api_key,
        "language": language
    }
    response = requests.get(endpoint, params=params)

    # Verificar se a resposta foi bem-sucedida
    if response.status_code == 200:
        return response.json()["results"]
    else:
        print(f"Erro na requisição: {response.status_code}")
        return None

# Função principal
def main():
    print("Extraindo dados dos filmes mais bem avaliados...")
    filmes = obter_filmes_top_rated(api_key)

    if filmes:
        # Convertendo para DataFrame
        df = pd.DataFrame(filmes)
        print("Dados extraídos com sucesso! Exibindo os 5 primeiros registros:")
        print(df[["title", "vote_average", "overview"]].head())

        # Salvar em arquivo CSV
        df.to_csv("filmes_top_rated.csv", index=False)
        print("Dados salvos no arquivo 'filmes_top_rated.csv'.")
    else:
        print("Falha ao extrair os dados.")

if __name__ == "__main__":
    main()
