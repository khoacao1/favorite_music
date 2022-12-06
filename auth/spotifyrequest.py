import requests
import os
import random
from dotenv import find_dotenv, load_dotenv
from auth.geniusrequest import getlyricgenius

# Function to generate a token as login on Spotify


def generatetoken():

  load_dotenv(find_dotenv())
  CLIENT_ID = os.getenv("CLIENT_ID")
  CLIENT_SECRET = os.getenv("CLIENT_SECRET")

  AUTH_URL = 'https://accounts.spotify.com/api/token'

  try:
    # POST
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })

    # Convert the response to JSON
    auth_response_data = auth_response.json()

    # Save the access token
    access_token = auth_response_data['access_token']

    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }

  except:  # Catch any error and print the message
    print("Cannot access to Spotify")
    return None  # Return None if something goes wrong with Spotify Auth
  return headers


# Function to generate ramdom artist and their top track


def getinfotoptrack(headers, listid):
  # Artist List
  # artistid = ["5uCXJWo3WoXgqv3T1RlAbh",
  #             "2Kx7MNY7cI1ENniW7vT30N",
  #             "5z1VAFwT35EVvCp1XlZZuL",
  #             "29WzbAQtDnBJF09es0uddn",
  #             "2P1puQXmG48EVLBrHbum1J",
  #             "7rwI5cbw9cUKFVul2rZMiZ", ]
  artistid = listid

  # If cannot get the auth token, return empty and skip the next request
  if headers is None:
    return None

  # request the song data and pick one randomly to display
  try:
    response = requests.get(
        "https://api.spotify.com/v1/artists/" + random.choice(artistid) + "/top-tracks?market=US", headers=headers)
    response_json = response.json()

    i = random.randrange(0, 10)
    track = response_json["tracks"][i]

    # Request the lyric URL
    geniuslink = getlyricgenius(
        track["name"] + " " + track["artists"][0]["name"])

    songinfos = (track["name"],  # songname
                 track["artists"][0]["name"],  # artistname
                 track["artists"][0]["external_urls"]["spotify"],  # artist_url
                 track["album"]["name"],  # albumname
                 track["album"]["external_urls"]["spotify"],  # album_url
                 track["album"]["images"][0]["url"],  # album_img
                 track["preview_url"],  # preview_url
                 track["external_urls"]["spotify"],  # track_url
                 geniuslink,)
    return songinfos
  except:  # Catch any error and print the message
    print("Something went wrong with the Song's Info!")
    return None  # Return empty data to html


def checkvalidid(headers, artid):
  response = requests.get(
      "https://api.spotify.com/v1/artists/" + artid + "/top-tracks?market=US", headers=headers)
  response_json = response.json()
  track = response_json["tracks"][0]

  return track["name"]
