import requests
import boto3
import json
from datetime import datetime

# Configuração da API TMDB
API_KEY = 'YOUR_KEY'
BASE_URL = 'https://api.themoviedb.org/3'

# Configuração AWS S3
s3 = boto3.client('s3')
BUCKET_NAME = 'data-lake-desafio'

# Função para buscar filmes no TMDb
def fetch_movies_by_year_genre(start_year, end_year, genres, max_records=100):
    results = []
    for year in range(start_year, end_year + 1):
        page = 1
        while True:
            try:
                url = f"{BASE_URL}/discover/movie"
                params = {
                    "api_key": API_KEY,
                    "primary_release_year": year,
                    "with_genres": ','.join(map(str, genres)),
                    "page": page
                }
                response = requests.get(url, params=params)
                if response.status_code != 200:
                    print(f"Erro na API: {response.status_code}")
                    break
                
                data = response.json()
                for movie in data.get('results', []):
                    # Filtrar campos relevantes
                    results.append({
                        "id": movie.get("id"),
                        "title": movie.get("title"),
                        "release_date": movie.get("release_date"),
                        "genres": movie.get("genre_ids", []),
                        "original_language": movie.get("original_language"),
                        "overview": movie.get("overview"),
                        "popularity": movie.get("popularity"),
                        "vote_average": movie.get("vote_average"),
                        "vote_count": movie.get("vote_count")
                    })

                # Controle de página
                if page >= data.get('total_pages', 0):
                    break
                page += 1

                # Limitar o número de registros
                if len(results) >= max_records:
                    results = results[:max_records]
                    break

            except Exception as e:
                print(f"Erro ao buscar filmes: {e}")
                break
    return results

# Função para salvar os dados no S3
def save_to_s3(data, path):
    try:
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=path,
            Body=json.dumps(data, indent=2),
            ContentType='application/json'
        )
        print(f"Dados salvos com sucesso em {path}")
    except Exception as e:
        print(f"Erro ao salvar no S3: {e}")

# Para executar o fluxo completo
if __name__ == "__main__":
    start_year = 2000
    end_year = datetime.now().year
    genres = [35, 16]  # IDs para Comédia e Animação
    
    # Buscar os dados
    data = fetch_movies_by_year_genre(start_year, end_year, genres)
    
    # Salvar no S3
    save_to_s3(data, f"raw/tmdb/json/movies_{start_year}_to_{end_year}.json")
