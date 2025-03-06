import requests

API_KEY = '1e8aa6dc5579d131ff74414300b05165'
BASE_URL = 'https://api.themoviedb.org/3'

def get_ghibli_movies():
    # Passo 1: Obtenha o ID da empresa (Studio Ghibli)
    search_company_url = f"{BASE_URL}/search/company?api_key={API_KEY}&query=Studio%20Ghibli"
    company_response = requests.get(search_company_url).json()
    company_id = company_response['results'][0]['id']  # Geralmente é 10342

    # Passo 2: Obtenha a quantidade total de resultados e busque os filmes com paginação
    discover_url = f"{BASE_URL}/discover/movie?api_key={API_KEY}&with_companies={company_id}&sort_by=release_date.asc&page=1"
    initial_response = requests.get(discover_url).json()
    
    total_results = initial_response.get('total_results', 0)
    total_pages = initial_response.get('total_pages', 1)

    movies = initial_response.get('results', [])

    # Passo 3: Percorra as outras páginas para obter todos os filmes
    for page in range(2, total_pages + 1):
        page_url = f"{BASE_URL}/discover/movie?api_key={API_KEY}&with_companies={company_id}&sort_by=release_date.asc&page={page}"
        response = requests.get(page_url).json()
        movies.extend(response.get('results', []))

    # Passo 4: Exiba a quantidade total e os filmes
    print(f"\n🎥 Quantidade total de filmes do Studio Ghibli: {total_results}\n")
    for movie in sorted(movies, key=lambda x: x['release_date'] or ''):
        title = movie['title']
        release_date = movie['release_date'] if movie['release_date'] else 'Data desconhecida'
        print(f"📽️ {title} - {release_date}")

get_ghibli_movies()
