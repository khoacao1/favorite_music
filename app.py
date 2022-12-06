import json
from enum import unique
import flask
import os


from auth.spotifyrequest import getinfotoptrack, generatetoken, checkvalidid
from dotenv import find_dotenv, load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask import redirect, url_for
from flask_login import LoginManager, login_manager, login_user, login_required, current_user, logout_user

import base64

app = flask.Flask(__name__, static_folder='./build/static')


# Call function to generate a token
token = generatetoken()

# Load Database URL from .env file
load_dotenv(find_dotenv())
databaseURL = os.getenv("DATABASE_URL")
if databaseURL and databaseURL.startswith("postgres://"):
  databaseURL = databaseURL.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = databaseURL
# suppresses a warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)  # assign database to app

# Create a datanase table for username


class Username(db.Model):
  __tablename__ = 'username'
  userid = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(120), nullable=False)
  password = db.Column(db.String(80))

  def is_authenticated(self):
    return True

  def is_active(self):
    return True

  def is_anonymous(self):
    return False

  def get_id(self):
    return str(self.userid)

  def get_user(self):
    return str(self.username)

  def __repr__(self):
    return str(self.username)


class ArtistID(db.Model):
  __tablename__ = 'artistid'
  artid = db.Column(db.Integer, primary_key=True)
  usernameFromUser = db.Column(db.String(120), nullable=False)
  idartist = db.Column(db.String(120), nullable=False)


with app.app_context():
  db.create_all()  # Create all tables if not exist


# app = flask.Flask(__name__, static_folder='./build/static')
# This tells our Flask app to look at the results of `npm build` instead of the
# actual files in /templates when we're looking for the index page file. This allows
# us to load React code into a webpage. Look up create-react-app for more reading on
# why this is necessary.
bp = flask.Blueprint("bp", __name__, template_folder="./build")


@bp.route('/index')
@login_required
def index():
    # TODO: insert the data fetched by your app main page here as a JSON
  # DATA = {"your": "data here"}
  # data = json.dumps(DATA)

  currentusername = str(current_user)

  artistListObj = list(ArtistID.query.filter_by(
      usernameFromUser=currentusername).all())
  artistlist = [a.idartist for a in artistListObj]

  has_artists_saved = len(artistlist) > 0
  if has_artists_saved:
    songinfo = getinfotoptrack(token, artistlist),

    DATA = {
        "has_artists_saved": has_artists_saved,
        "song_name": songinfo[0][0],
        "artist_name": songinfo[0][1],
        "artist_url": songinfo[0][2],
        "album_name": songinfo[0][3],
        "album_url": songinfo[0][4],
        "album_pic_url": songinfo[0][5],
        "song_preview": songinfo[0][6],
        "song_url": songinfo[0][7],
        "genius": songinfo[0][8],
        "nameOfUser": currentusername,
        "artist_ids": artistlist
    }
  else:
    DATA = {
        "has_artists_saved": has_artists_saved,
        "song_name": None,
        "artist_name": None,
        "artist_url": None,
        "album_name": None,
        "album_url": None,
        "album_pic_url": None,
        "song_preview": None,
        "song_url": None,
        "genius": None,
        "nameOfUser": currentusername,
        "artist_ids": artistlist,
    }

  data = json.dumps(DATA)

  return flask.render_template(
      "index.html",
      data=data,
  )


app.register_blueprint(bp)
app.secret_key = b'This is Khoa 2!'  # for flashes Message

login_manager = LoginManager()  # for flask-login initial
login_manager.init_app(app)   # connect flask-login-manager to app
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
  return Username.query.get(int(user_id))


@app.route("/")
@login_required
def auth():
  if current_user.is_authenticated:
    return flask.redirect(flask.url_for("bp.index"))
  return flask.redirect(flask.url_for("login"))


@app.route("/signup")
def signup_page():
  return flask.render_template("signup.html",)


@app.route("/login")
def login_page():
  return flask.render_template("login.html",)


@app.route("/logout")
def logout_page():
  # variable=current_user.username
  logout_user()
  flask.flash("You have logged out!")
  return flask.render_template("logout.html",)


@app.route("/signup", methods=["POST"])
def signup():
  signup_username = flask.request.form.get('username')
  signup_password = flask.request.form.get('password')
  
  # check if it in database
  inputsignupusers = Username.query.filter_by(username=signup_username).first()
  if inputsignupusers:  # if in database, popup error
    flask.flash("Username already been taken. Try something else!")
    return flask.redirect(url_for("signup"))
  else:  # not in database, create new username
    encrypt_signup_password = base64.b64encode(signup_password.encode("utf-8"))
    signupuser = Username(username=signup_username,password=str(encrypt_signup_password))
    db.session.add(signupuser)
    db.session.commit()
    login_user(signupuser)
    return flask.redirect(flask.url_for("bp.index"))


@app.route("/login", methods=["POST", ])
def login():
  login_username = flask.request.form.get('username')
  login_password = flask.request.form.get('password')
  encrypt_login_password = encodepassword(login_password)

  users = Username.query.filter_by(username=login_username, password=str(encrypt_login_password)).first()
  if not users:
    flask.flash("Invalid Username or Password. Try Again!")
    return flask.redirect(url_for("login"))
  else:
    login_user(users)
    return flask.redirect(flask.url_for("bp.index"))

def encodepassword(password):
    return base64.b64encode(password.encode("utf-8"))

# ArtistID Database Handle


@app.route("/uploadartistid", methods=["POST"])
def uploadartistid():
  ArtistID.query.filter_by(usernameFromUser=str(current_user)).delete()
  artistidslist = flask.request.json.get("artist_list")
  inval_id = False
  invalid_count = 0

  for art_id in artistidslist:
    try:
      checkvalidid(token, art_id)
    except:
      inval_id = True
    if ArtistID.query.filter_by(usernameFromUser=str(current_user), idartist=art_id).first():
      inval_id = True
    if inval_id:
      invalid_count += 1
    else:
      currentusername = str(current_user)
      signupartist = ArtistID(
          usernameFromUser=currentusername, idartist=art_id)
      db.session.add(signupartist)
  db.session.commit()
  artistList = ArtistID.query.filter_by(
      usernameFromUser=str(current_user)).all()
  artistids = [a.idartist for a in artistList]
  return flask.jsonify({"artistids_server": artistids, "invalid_count": invalid_count})


app.run(
    host=os.getenv('IP', '0.0.0.0'),
    port=int(os.getenv('PORT', 8081)),
    debug=True,
)
