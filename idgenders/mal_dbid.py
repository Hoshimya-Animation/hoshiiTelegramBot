# Import the requests library to handle HTTP requests
import requests

# Import the lru_cache decorator from functools to cache function results
from functools import lru_cache

# Define a function to get a list of anime IDs, using lru_cache to cache the results
@lru_cache(100)
def getIDAnime() -> list:
    # Send a GET request to the specified URL and parse the JSON response
    get_json = requests.get('https://raw.githubusercontent.com/seanbreckenridge/mal-id-cache/master/cache/anime_cache.json').json()
    # Combine the 'sfw' and 'nsfw' lists from the JSON response and sort them
    id_anime = sorted(get_json['sfw'] + get_json['nsfw'])
    # Return the sorted list of anime IDs
    return id_anime

# Define a function to get a list of manga IDs, using lru_cache to cache the results
@lru_cache(100)
def getIDManga() -> list:
    # Send a GET request to the specified URL and parse the JSON response
    get_json = requests.get('https://raw.githubusercontent.com/seanbreckenridge/mal-id-cache/master/cache/manga_cache.json').json()
    # Combine the 'sfw' and 'nsfw' lists from the JSON response and sort them
    id_manga = sorted(get_json['sfw'] + get_json['nsfw'])
    # Return the sorted list of manga IDs
    return id_manga

# Clear the cache for the getIDAnime function
getIDAnime.cache_clear()
# Clear the cache for the getIDManga function
getIDManga.cache_clear()
