import requests
import pandas
import json
import sqlalchemy

from secrets import ticketmaster_key

class Concert():
    def __init__(self, artist_list):
        self.artists_list = artist_list
        self.concerts_df = self.filter_concert_data()

    def get_concerts(self):
        '''Connect to ticketmaster API and obtain concerts based on most played artists'''

        query = 'https://app.ticketmaster.com/discovery/v2/events?apikey={apikey}'.format(apikey = ticketmaster_key)

        #This list will contain other list elements. Each element will correspond to a different artist and his/her events
        total_concerts_list = []
        #Iterate through the top 5 artists and pass artist name as keyword to search events
        for artist in self.artists_list:
            response = requests.get(
                query,
                params = {
                    'keyword': artist,
                    'countryCode': 'US',
                    'sort': 'date,asc'
                }
            )
            data = response.json()

            try:
                #Defines a list of dictionaries. Each dictionary is a concert/event with keys such as name, id, url, date, location, etc
                artist_concerts_list = data['_embedded']['events']
                #Append each list to the total concerts list. 
                total_concerts_list.append(artist_concerts_list) 
            except KeyError:
                #The key error occurs when there are no concert for that artist based on the parameters defined
                print('No concerts available in the US')


        return(total_concerts_list)


    def filter_concert_data(self):
        '''Filters API data to obtain event name, id, url, date and location'''
        total_concerts_list = self.get_concerts()

        #Declare empty lists to store the event name, id, url, date and location
        name_list = []
        id_list = []
        date_list = []
        city_list = []
        state_list = []
        url_list = []

        #Iterate through API results and populate lists
        for artist_concerts in total_concerts_list:
            for concert in artist_concerts:
                name_list.append(concert['name'])
                id_list.append(concert['id'])
                date_list.append(concert['dates']['start']['localDate'])
                city_list.append(concert['_embedded']['venues'][0]['city']['name'])
                state_list.append(concert['_embedded']['venues'][0]['state']['name'])
                url_list.append(concert['url'])
        
        #Create a dictionare to store the concert lists
        concert_dict = {
            'name': name_list,
            'id': id_list,
            'date': date_list,
            'city': city_list,
            'state': state_list,
            'url': url_list
        }

        #Create a dataframe using the concert dictionary
        df = pandas.DataFrame(concert_dict, columns = concert_dict.keys())

        return(df)

    def upload_concerts(self):
        '''Uploads the concert data to database. Only appends new tracks to DB'''
        #syntax: engine = create_engine("mysql://USER:PASSWORD@HOST/DATABASE")
        engine = sqlalchemy.create_engine("mysql+pymysql://root:Jams2009Charlie2014!@localhost/spoti-tours")
        #Create sql connection 
        connection = engine.connect()

        #Insert query
        self.concerts_df.to_sql('concerts', con = connection, if_exists = 'append', index = False)


if __name__ == '__main__':
    artist_list = ['Bizarrap', 'Rauw Alejandro', 'Tiago PZK', 'Marc Seguí', 'Bad Bunny']
    concert = Concert(artist_list)
    filtered_concerts = concert.filter_concert_data()
    print(filtered_concerts)
    #concert.upload_concerts()
    