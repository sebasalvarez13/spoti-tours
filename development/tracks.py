from sqlite3 import dbapi2
import pandas
import requests
import sqlalchemy
import pymysql

from secrets import spotify_token
from database import connection

class Tracks():
    def __init__(self, spotify_token):
        self.spotify_token = spotify_token
        self.filter_tracks_df = self.filter_track_data()
        self.connection = connection

    def get_tracks(self):
        '''Connects to Spotify API and obtains the recently played songs. Returns the parsed data'''
        #max number of items that can be returned
        limit = 50

        query = "https://api.spotify.com/v1/me/player/recently-played?limit={}".format(limit)
        headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
        }

        response = requests.get(query, headers = headers)

        api_data = response.json()

        return(api_data)


    def filter_track_data(self):
        '''Filters API data to obtain song, artist, album and uri'''
        #Declare empty lists to store the track name, artist, album, played_at and uri
        songs_list = []
        artist_list = []
        album_list = []
        played_at_list = []
        song_uri_list = []

        #Iterate through API results and populate lists
        api_data = self.get_tracks()

        for track in api_data['items']:
            songs_list.append(track['track']['name'])
            artist_list.append(track['track']['album']['artists'][0]['name'])
            album_list.append(track['track']['album']['name'])
            played_at_list.append(track['played_at'])
            song_uri_list.append(track['track']['uri'])

        #Create a dictionary and add the lists (values) to their respective key
        track_dict = {
            'song': songs_list,
            'artist': artist_list,
            'album': album_list,
            'played_at': played_at_list,
            'song_uri': song_uri_list
        }

        #Create a dataframe using the track dictionary
        df = pandas.DataFrame(track_dict, columns = track_dict.keys())

        return(df)


    def tracks_count(self):
        '''Retunrs the number of records in the tracks table'''    
        #Execute query
        query = '''SELECT count(*) FROM tracks;'''
        result = self.connection.execute(query)

        #Fetch count value
        track_count = result.fetchall()[0][0]

        return(track_count)


    def track_exists(self, song_uri):
        '''Retunrs true if song already exists in DB. Uses song_uri data to verify existence'''
        query = """SELECT count(*) FROM tracks WHERE song_uri = %s"""
        result = self.connection.execute(query, [song_uri])
        track_exists = result.fetchall()[0][0]

        if track_exists == 0:
            return False
        elif track_exists == 1:
            return True


    def upload_tracks(self):
        '''Uploads the track data to database. Ignores "played_at" field. Only appends new tracks to DB'''
        df = self.filter_tracks_df
        #Drops "played_at" column
        df = df.drop(['played_at'], axis = 1)

        #Deletes repeated tracks from filtered df
        df = df.drop_duplicates(subset= 'song_uri', keep= 'first')

        #Insert 'id' column at beggining of df before uploading to database. 
        last_id = self.tracks_count()
        df.insert(loc = 0, column = 'id', value = range((last_id+1), (last_id+len(df)+1))) 

        #Insert query
        query = """INSERT INTO tracks (song, artist, album, song_uri)
                VALUES (%s, %s, %s, %s)"""

        for index, row in df.iterrows():
            song_uri = row['song_uri']
            if self.track_exists(song_uri) == False:
                self.connection.execute(query, [row['song'], row['artist'], row['album'], song_uri])


