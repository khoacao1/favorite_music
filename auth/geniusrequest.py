import requests
import os
from dotenv import find_dotenv, load_dotenv

# Function use @param:search to return the lyric URL


def getlyricgenius(search):

  load_dotenv(find_dotenv())
  GENIUS_CLIENT_ID = os.getenv("GENIUS_CLIENT_ACCESS_TOKEN")

  searchterm = search

  genius_search_url = f"http://api.genius.com/search?q={searchterm}&access_token={GENIUS_CLIENT_ID}"

  try:
    response = requests.get(genius_search_url)

    response_json = response.json()

    linktolyric = response_json["response"]["hits"][0]["result"]["url"]

  except:  # Catch any error and print the message
    print("Cannot get the Lyric")

  return linktolyric
