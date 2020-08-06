import time
import requests

# find all matches using OpenDota API. Call DotaBuff to get list of IDs.
from requests.exceptions import ChunkedEncodingError
from requests.exceptions import ConnectionError

api_url = 'https://api.stratz.com/api/v1/'
headers = {'Content-Type': 'application/json'}


def get_heroes():
    api_call = '{0}Hero'.format(api_url)

    with requests.get(api_call) as response:

        if response.status_code == 200:
            return response.content
        else:
            print("heroes not gotten")
            return response.raise_for_status()


def get_version():
    api_call = '{0}GameVersion'.format(api_url)

    with requests.get(api_call) as response:

        if response.status_code == 200:
            return response.content
        else:
            print("gameversion not gotten")
            return response.raise_for_status()

def get_match(matchid, counter):
    api_call = '{0}match/{1}/breakdown'.format(api_url, matchid)
    time.sleep(1)
    try:
        response = requests.get(api_call, headers = {'User-agent': 'bot google 1.0'})

        if response.status_code == 200:
            print(response.content)
            return response.content
        elif response.status_code == 429:
            print("waiting: {0}".format(response.headers.get('Retry-After')))
            time.sleep(int(response.headers.get('Retry-After')))
        elif counter < 3:
            time.sleep(1)
            print("failed, attempting again: {0}".format(counter))
            print(matchid)
            print(response.status_code)
            print(response.headers.items())
            counter += 1
            get_match(matchid, counter)

        else:
            print("failed and counter overstepped.")
            return False
    except ChunkedEncodingError:
        print("api call not answered correctly, and resulting in chunk encoding issue for: {0}".format(matchid))
    except ConnectionError:
        print("Connection error was raised for: {0}".format(matchid))
