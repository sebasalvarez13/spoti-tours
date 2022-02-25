import pandas
import requests
import sqlalchemy
import pymysql


class Tracks():
    def __init__(self, spotify_token):
        self.spotify_token = spotify_token

    def get_tracks(self):
        '''Connects to Spotify API and obtains the recently played songs. Returns the parsed data'''
        #max number of items that can be returned
        limit = 50

        query = "https://api.spotify.com/v1/me/player/recently-played?limit={}".format(limit)

        response = requests.get(
            query,
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)}
        )

        data = response.json()

        return(data)


    def filter_track_data(self):
        '''Filters API data to obtain song, artist, album and uri'''
        data = self.get_tracks()

        #Declare empty lists to store the track name, artist, album, played_at and uri
        songs_list = []
        artist_list = []
        album_list = []
        played_at_list = []
        song_uri_list = []

        #Iterate through API results and populate lists
        for track in data['items']:
            songs_list.append(track['track']['name'])
            artist_list.append(track['track']['album']['artists'][0]['name'])
            album_list.append(track['track']['album']['name'])
            played_at_list.append(track['played_at'])
            song_uri_list.append(track['track']['uri'])

        #Create a dictionary and add the lists (values) to their respective key
        track_dict = {
            'songs': songs_list,
            'artist': artist_list,
            'album': album_list,
            'played_at': played_at_list,
            'song_uri': song_uri_list
        }

        #Create a dataframe using the track dictionary
        df = pandas.DataFrame(track_dict, columns = track_dict.keys())

        return(df)
            
if __name__ == '__main__':
    spotify_token = ''
    tracks = Tracks(spotify_token)
    print(tracks.filter_track_data())