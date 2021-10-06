import requests
import tweepy
import config

def connect_to_tweepy():
    """ Get authorization to tweepy api """
    auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_token_secret)
    api = tweepy.API(auth)
    return api
    

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(config.bearerToken)}
    return headers


def connect_to_endpoint(url, headers,params):
    """ connect to twitter api """
    response = requests.request("GET", url, headers=headers,params=params)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def get_response_from_url(url,params=''):
    """ Get response from the url """
    headers = create_headers(config.bearerToken)
    json_response = connect_to_endpoint(url, headers,params)
    return json_response
    