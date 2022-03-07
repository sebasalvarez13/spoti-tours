from sqlalchemy import table
from flask import Flask, render_template, request, redirect, url_for, session
from users import User
from tracks import Tracks
from artists import Artist
from authorization import *
from reproductions import *


app = Flask(__name__)
app.secret_key = 'secretkey'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        user = User()
        user.register_user(first_name, last_name, email, username, password)

        return redirect(url_for('home'))
    else:
        return render_template('register.html', action = 'register')


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User()
        #Define boolean login to verify username and password
        login = user.login_user(username, password)

        #If username and password match, create a session and redirect user Spotify Authorization page
        if  login is True:
            #Set up session data. Session stores data as a dictionary
            session['username'] = username
            session['password'] = password

            #Get authorization code from Spotify server
            response = get_authorization()
            url = response.url

            return redirect(url)
        else:
            #If username or password is incorrect, redirect to login page and display "Username/password incorrect"
            return redirect(url_for('login'))
    else:
        return render_template('login.html', action = 'login')


@app.route('/callback', methods = ['GET', 'POST'])
def callback():
    if request.method == 'GET':
        #Obtain the authorization code from the URL
        code = request.args.get("code")
        #Pass code to Spotify server to obtain access_token
        token_response = get_token(code)
        #access_token = token_response['access_token']
        session['access_token'] = token_response['access_token']

        #Verify that user is logged in session
        if 'username' in session:
            username = session['username']
            return redirect(url_for('dashboard', user = username))
        else:
            return redirect(url_for('login'))


@app.route('/dashboard/<user>', methods = ['GET', 'POST'])
def dashboard(user):
    if request.method == 'GET':
        #Get 50 recently played songs for user
        tracks = Tracks(session['access_token'])
        #Return a dataframe with song, artist, album, played_at, song_uri
        recent_songs = tracks.filter_track_data()

        #Upload tracks to database
        tracks.upload_tracks()

        #Upload reproductions to database
        format_reprod = format_time(recent_songs)
        upload_reproductions(user, format_reprod)
        
        #Drop song_uri column before displaying in html page
        recent_songs = format_reprod.drop(['song_uri'], axis = 1)
        #Convert df to html
        recent_songs_html = recent_songs.to_html(justify = 'left')

        #return(recent_songs_html)
        return render_template('dashboard.html', table = recent_songs_html)


@app.route('/dashboard/topartists', methods = ['GET', 'POST'])
def topartists():
    if request.method == 'GET':
        artist = Artist()
        top_artists = artist.most_played_artists()

        #Convert df to html
        top_artists_html = top_artists.to_html(justify = 'left')

        #return(recent_songs_html)
        return render_template('dashboard.html', table = top_artists_html)


if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=8888, debug=True)