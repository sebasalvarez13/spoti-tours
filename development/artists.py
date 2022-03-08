import pandas
import sqlalchemy


class Artist():
    def __init__(self):
        pass

    def top_artists(self, username):
        '''Returns the 5 most played artist per user'''
        #syntax: engine = create_engine("mysql://USER:PASSWORD@HOST/DATABASE")
        engine = sqlalchemy.create_engine("mysql+pymysql://root:Jams2009Charlie2014!@localhost/spoti-tours")
        
        #Create sql connection
        connection = engine.connect()

        #Open sql script. Script limit sets to 5
        with open('../sql_queries/most_played_artists.sql', 'r') as sql_file:
            sql_string = sql_file.read()

        #Get user_id from users table
        query2 = '''SELECT id FROM users 
                    WHERE username = %s'''
        result2 = connection.execute(query2, [username])
        user_id = result2.fetchall()[0][0]

        #Execute query
        result = connection.execute(sql_string, [user_id])

        #Fetch artist names
        artists = result.fetchall()
        artists_list = []
        reproductions_list = []

        for artist in artists:
            artists_list.append(artist[1])
            reproductions_list.append(artist[2])

        top_artists_dict = {
            'artist': artists_list,
            'reproductions': reproductions_list
        }

        #Create dataframe with artist name and reproductions
        df = pandas.DataFrame(top_artists_dict, columns = top_artists_dict.keys())

        return(df)

if __name__ == '__main__':
    artist = Artist()
    top_artists_df = artist.top_artists('picoletosa')

    session = {}
    session['topartists'] = top_artists_df['artist']

    for artist in session['topartists']:
        print(artist)
    