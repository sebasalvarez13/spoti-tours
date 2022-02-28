import requests
from secrets import client_id, client_secret

def get_authorization():
    '''Using Authorization Code Flow. Request auth from user to get recently played songs'''
    query = "https://accounts.spotify.com/authorize"
    scope = "user-read-recently-played"
    redirect_uri = "http://localhost:8888/callback"
    parameters = {
        "client_id": client_id,
        "scope": scope,
        "response_type": "code",
        "redirect_uri": redirect_uri
        }

    response = requests.get(query, params = parameters)

    return(response)


def get_token(code):
    query = "https://accounts.spotify.com/api/token"
    redirect_uri = "http://localhost:8888/callback"
    data = {
            "grant_type": 'authorization_code',
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri
        }
    
    response = requests.post(query, data)

    response_json = response.json()

    return(response_json)

