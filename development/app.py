from crypt import methods
from sqlalchemy import table
from flask import Flask, render_template, request, redirect, url_for, session, flash
from users import User
from tracks import Tracks
from artists import Artist
from concerts import Concert
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

        #If username and password match, create a session and redirect user Spotify Authorization page
        if  user.user_exists(username, password):
            #Set up session data. Session stores data as a dictionary
            session['username'] = username
            session['password'] = password

            #Get authorization code from Spotify server
            response = get_authorization()
            url = response.url

            return redirect(url)
        else:
            #If username or password is incorrect, redirect to login page and flash message
            flash('Incorrect user or password. Try again!')
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
        #Store accesss token in Session key
        session['access_token'] = token_response['access_token']

        #If username is logged in session, redirect to recent songs in dashboard
        if 'username' in session:
            username = session['username']
            return redirect(url_for('recentsongs'))
        else:
            return redirect(url_for('login'))


@app.route('/dashboard/recentsongs', methods = ['GET', 'POST'])
def recentsongs():
    if request.method == 'GET':
        #Get 50 recently played songs for user
        tracks = Tracks(session['access_token'])
        #Return a dataframe with song, artist, album, played_at, song_uri
        recent_songs = tracks.filter_track_data()
        #Upload tracks to database
        tracks.upload_tracks()

        #Fix time format and timezone for recent_songs dataframe
        reproductions_fixed_time = reproductions_time_format(recent_songs)
        #Upload reproductions to database
        upload_reproductions(session['username'], reproductions_fixed_time)
        
        #Drop song_uri column before displaying in html page
        recent_songs_display = reproductions_fixed_time.drop(['song_uri'], axis = 1)
        #Convert df to html
        recent_songs_html = recent_songs_display.to_html(classes = "table table-dark table-striped", justify = 'left')

        return render_template('dashboard.html', table = recent_songs_html)


@app.route('/dashboard/topartists', methods = ['GET', 'POST'])
def topartists():
    if request.method == 'GET':
        artist = Artist()
        top_artists = artist.top_artists(session['username'])

        #Define top artists key for session
        session['topartists'] = top_artists['artist'].to_list() 
        print(session['topartists'])
        #Convert df to html
        top_artists_html = top_artists.to_html(classes = "table table-dark table-striped", justify = 'left')

        return render_template('dashboard.html', table = top_artists_html)


@app.route('/dashboard/concerts', methods = ['GET', 'POST'])
def concerts():
    if request.method == 'GET':
        concert = Concert(session['topartists'])
        concerts_df = concert.filter_concert_data()

        #Drop the concert id before displaying in webpage
        concerts_df = concerts_df.drop(['id'], axis = 1)

        #Convert df to html
        concerts_html = concerts_df.to_html(classes = "table table-dark table-striped", justify = 'left')
        
        return render_template('dashboard.html', table = concerts_html)


if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=8888, debug=True)