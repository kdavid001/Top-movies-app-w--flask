import requests

url ="https://api.themoviedb.org/3/search/movie"
API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwMWJhZGIxN2NmNjFkY2Q2MzhkYjZkYWEzNjQ3ODkxYiIsIm5iZiI6MTc0MzQyNzM5NC41OTYsInN1YiI6IjY3ZWE5NzQyNTA0MGE3NWI0YWU1N2QwMCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.IISVbxUhTOnUZOQdzb6RqTiyUDUH-59IKVovs62TgYU"
headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwMWJhZGIxN2NmNjFkY2Q2MzhkYjZkYWEzNjQ3ODkxYiIsIm5iZiI6MTc0MzQyNzM5NC41OTYsInN1YiI6IjY3ZWE5NzQyNTA0MGE3NWI0YWU1N2QwMCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.IISVbxUhTOnUZOQdzb6RqTiyUDUH-59IKVovs62TgYU"
}

query_param = {
    "query" : "interstella"
}

response = requests.get(url = url, headers = headers, params = query_param).json()
movie_list = []
for key, value in response.items():
    print(f"{key}: {value}")
    if "results" in response:
        for movie in response["results"]:
            movie_list.append(f"{movie.get(f"title", 'N/A')}, Release Date: {movie.get('release_date.year', 'N/A')}")

print(movie_list)