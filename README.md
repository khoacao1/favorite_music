# Favorite Music App
This Web App Using the API from Spotify and Genuis, to display random top 10 songs from 
user's favorite artist list.

User will be able to add, remove Artist's IDs to the Database through a list when click on **Save**.

From the web app, user can also click on the name of the artist, or album to get direct to Spotify Page about that 
content you chose.
***
## Clone this repo to yours
1. In your VM terminal, in your home directory, clone the repo: `git clone https://github.com/khoacao1/favorite_music.git`
2. `cd` into the repository that is created and you should see all the files now.

### Technologies
- VScode

### Framework
- Flask

### Libraries
- requests
- dotenv
- flask_login

## Requirements
1. run `sudo apt install npm`
2. run `pip install -r requirements.txt`

### APIs
- Spotify: [Artist's Top Track]

- Genuis: [Lyric Search]

## Signup for [Spotify Developer] and [Genuis Developer]

Create an App with App Name and use the information the App provides.

## Setup
1. Create a .env file in the auth directory
2. From [https://developer.spotify.com/dashboard/applications] choose your app.
    + Add your Spotify CLIENT_ID, CLIENT_SECRET to .env file with the line:

            `export CLIENT_ID = "<CLIENT_ID>"`

            `export CLIENT_SECRET = "<YOUR_CLIENT_SECRET>"`

3. From [https://genius.com/api-clients] choose **All API Clients** and generate your *ACCESS TOKEN*.

    + Add your GENUIS ACCESS TOKEN to .env file with the line:

            `export GENIUS_CLIENT_ACCESS_TOKEN = "<YOUR_ACCESS_TOKEN>"`


## Setup psql
- Update your package index: run `sudo apt update` in the terminal
- Install postgresql: run `sudo apt install postgresql` in the terminal
- To run the psql prompt: run `sudo -u postgres psql` in the terminal

## Setup Heroku Database
1. In the directory, login and fill creds: `heroku login -i`
2. Create a new Heroku app: `heroku create` if you haven't got one. If you want to use the heroku app that you have 
already created, you can skip this step.
3. Create a new remote DB on your Heroku app: `heroku addons:create heroku-postgresql:hobby-dev -a {your-app-name}` 
no braces on the app-name.
4. See the config vars set by Heroku for you: `heroku config`. Copy paste the value for DATABASE_URL.
5. Set the value of DATABASE_URL to the .env file with the line:

        `export DATABASE_URL='copy-paste-value-in-here'`

6. IF THE URL STARTS WITH `postgres:`, replace that with `postgresql:`.

## Run Application
1. Run command in terminal (in your project directory): `npm run build`. This will update anything related to your 
`App.js` file (so `public/index.html`, any CSS you're pulling in, etc).
2. Run command in terminal `python3 main.py`
3. Preview web page in browser 'localhost:8080/'




[Artist's Top Track]:https://developer.spotify.com/console/get-artist-top-tracks/?country=SE&id=43ZHCT0cAZBISjO8DG9PnE
[Lyric Search]:https://docs.genius.com/#search-h2
[Spotify Developer]:https://developer.spotify.com/dashboard/login
[Genuis Developer]:https://genius.com/developers
[https://developer.spotify.com/dashboard/applications]:https://developer.spotify.com/dashboard/applications
[https://genius.com/api-clients]:https://genius.com/api-clients