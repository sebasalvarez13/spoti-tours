import pandas
import sqlalchemy
import pymysql
import re
import datetime

from datetime import timezone
from secrets import spotify_token
from tracks import Tracks


def upload_reproductions(username, df_tracks):
    '''Uploads the song_id, users_id and played_at'''
    #syntax: engine = create_engine("mysql://USER:PASSWORD@HOST/DATABASE")
    engine = sqlalchemy.create_engine("mysql+pymysql://root:Jams2009Charlie2014!@localhost/spoti-tours")
    #Create sql connection 
    connection = engine.connect()

    #Compare song_uri to data in 'tracks' table and get song_id
    for index, row in df_tracks.iterrows():
        song_uri = row['song_uri']
        played_at = row['played_at']
        
        #Select query. Pass df['song_uri'] as parameter %s
        query = '''SELECT id FROM tracks 
                    WHERE song_uri = %s'''
        result = connection.execute(query, [song_uri])

        #Store song_id. If id is null assign 0
        try:
            song_id = result.fetchall()[0][0]
        except IndexError:
            song_id = 0
        
        #Get user_id from users table
        query2 = '''SELECT id FROM users 
                    WHERE username = %s'''
        result2 = connection.execute(query2, [username])
        user_id = result2.fetchall()[0][0]

        #Assign id to reproduction record
        result = connection.execute('SELECT count(*) FROM reproductions;')
        reproductions_count = result.fetchall()[0][0]

        if reproductions_count == 0:
            id = 1
            query = '''INSERT INTO reproductions VALUES (%s, %s, %s, %s);'''
            result = connection.execute(query, [id, song_id, user_id, played_at])
        else:
            query = '''INSERT INTO reproductions (song_id, user_id, played_at) VALUES (%s, %s, %s);'''
            result = connection.execute(query, [song_id, user_id, played_at])


def format_time(df_tracks):
    '''Change format for played_at so it can be inserted into mysql database. Retunr df with correct datetime format'''
    df_tracks = df_tracks
    fixed_times = []

    for time in df_tracks['played_at']:
        #Spotify returns time as a string in UTC. Filter string from  ".xxxZ" element
        time_fltrd = re.search('[0-9]+\-[0-9]+\-[0-9]+T[0-9]+\:[0-9]+\:[0-9]+', time)

        #Convert time string to datetime object
        spotify_time_obj = datetime.datetime.strptime(time_fltrd.group(), '%Y-%m-%dT%H:%M:%S') 

        #Convert time object to string in correct sql datetime format
        sql_time_str = spotify_time_obj.strftime('%Y-%m-%d %H:%M:%S')
        #Append fixed times to list
        fixed_times.append(sql_time_str)

    #Replace original 'played_at' column with fixed values
    df_tracks = df_tracks.drop(['played_at'], axis = 1)
    df_tracks['played_at'] = fixed_times

    return df_tracks

    print(fixed_times)

    '''
    #Convert datetime object in UTC to local time
    #local_time_obj = spotify_time_obj.replace(tzinfo=timezone.utc).astimezone(tz=None)

    
    #Strip datetime object in local time into string
    time = local_time_obj.strftime("%H:%M:%S")
    date = local_time_obj.strftime("%m-%d-%Y")
    '''

if __name__ == '__main__':
    tracks = Tracks(spotify_token)
    df_tracks = tracks.df_tracks
    #print(df_tracks)
    username = 'picoletosa'
    new_df_tracks = format_time(df_tracks)
    upload_reproductions(username, new_df_tracks)
