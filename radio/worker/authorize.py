import base64, logging, io, json, os, requests, six, time

# import environment variables
SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')         # Spotify client id stored as local env. var.
SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET') # Spotify client secret stored as local env. var.
ROOT = os.environ.get('ROOT')   # because local paths change between machines

assert SPOTIFY_CLIENT_ID
assert SPOTIFY_CLIENT_SECRET
assert ROOT

# Authorization for Spotify
def get_token() -> str:
    '''
    Steps:
        X get token from local file ".data"
        X check if access_token is expired:
            X it is expired:
                X call token url with correct parameters and headers
                X update .data with new tokens  
        X return access token
    '''
    cache_token = get_cache_token()

    if is_token_expired(cache_token) or cache_token.get("token") in (None, "null"):
        cache_token = refresh_access_token(cache_token['refresh_token'])

    return cache_token['token']


# Read cached token from FileShare
def get_cache_token() -> dict:
    """
    Steps:
        X load local data
        X return payload
    """
        
    path = f'{ROOT}/.data' if os.path.exists(f'{ROOT}/.data') else '~/.data'
    with open(path, 'r') as f:
        data = json.load(f)
        payload = {
            "refresh_token": data.get("refresh_token", None),
            "timestamp": data.get("timestamp", None),
            "token": data.get("token", None),
        }

    return payload      
    

# Check if cached token is still valid 
def is_token_expired(token_info) -> bool:
    """
    Steps:
        X get current time
        X measure difference between now and timestamp
        X create boolean about expired
            X fall back on setting expired true
    """
    now = int(time.time())

    try:
        time_difference = now - int(token_info["timestamp"])
        print(f"Time difference: {time_difference}")
        expired = time_difference > 3600
    except:
        expired = True  # TODO: clean this up

    if token_info.get("token") in (None, "null"):
        expired = True

    return expired


# Refresh token from cache
def refresh_access_token(refresh_token) -> dict:
    '''
    Steps:
        X set correct payload (refresh_token) 
        X set correct header  (client id and secret)
        X post request 
        X convert response to json
        X update token_info in FileShare cache  
        X return token info
    '''
    # parameters for post request
    OAUTH_TOKEN_URL = "https://accounts.spotify.com/api/token"
    PAYLOAD = {
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token'
    }
    HEADERS = make_headers()
    
    # post request
    response = requests.post(
        url=OAUTH_TOKEN_URL,
        data=PAYLOAD,
        headers=HEADERS
    )
    token_info = response.json()

    print(f"Returned token info: \n {token_info}")

    payload = {
        "refresh_token": token_info.get("refresh_token", refresh_token),
        "token": token_info.get("access_token"),
        "timestamp": int(time.time())
    }

    # store tokens for later
    store_renewed_token(payload)

    return payload


# Make header for token request
def make_headers() -> dict:
    client_id = SPOTIFY_CLIENT_ID         # Spotify cliient id stored as local env. var.
    client_secret = SPOTIFY_CLIENT_SECRET # Spotify client secret stored as local env. var.

    # base64 encoded string
    client = base64.b64encode(
        six.text_type(f'{client_id}:{client_secret}').encode('ascii')
    )
    return {"Authorization": f"Basic {client.decode('ascii')}", "Content-Type": "application/x-www-form-urlencoded"}


# Store the renewed token locally 
def store_renewed_token(token_info):
    if os.path.exists(f'{ROOT}/.data'):
        with open(f'{ROOT}/.data', 'w') as f:
            json.dump(token_info, f, indent=4)
    else:
        with open('~/.data', 'w') as f:
            json.dump(token_info, f, indent=4)
    return True


# Get first token with access code
def get_token_first_time(code) -> dict:
    '''
    Steps:
        X set correct payload (refresh_token) 
        X set correct header  (client id and secret)
        X post request 
        X convert response to json
        X update token_info in FileShare cache  
        X return token info
    '''
    # parameters for post request
    OAUTH_TOKEN_URL = "https://accounts.spotify.com/api/token"
    PAYLOAD = {
        'grant_type': 'authorization_code',
        'redirect_uri': 'https://localhost:8888/callback',
        'code': code,
    }
    HEADERS = make_headers()
    
    print(
        f"""
        url: {OAUTH_TOKEN_URL}
        data: {PAYLOAD}
        header: {HEADERS}
        """
    )
    # post request
    response = requests.post(
        url=OAUTH_TOKEN_URL,
        data=PAYLOAD,
        headers=HEADERS
    )
    token_info = response.json()

    print(token_info)

    # add needed key-values to tokenn info before storing
    token_info["timestamp"] = int(time.time())
    token_info["token"] = token_info["access_token"]

    # store for later use
    store_renewed_token(token_info)

    return token_info


# Build url to generate access code (cannot use requests to call)
def get_code():
    """
    Can not call requests to get access code.
    """

    # parameters for post request
    OAUTH_TOKEN_URL = "https://accounts.spotify.com/authorize"
    PAYLOAD = {
        'client_id': '9656ff22d7604d078e98e54a1870b92d',
        'scope': 'user-read-currently-playing,user-read-recently-played',
        'redirect_uri': 'https://localhost:8888/callback',
        'state': 1111000011110000,
        'response_type': 'code'
    }
    HEADERS = make_headers()
    """
    # post request
    response = requests.post(
        url=OAUTH_TOKEN_URL,
        data=PAYLOAD,
        # headers=HEADERS
    )
    #token_info = response.json()

    #print(token_info)

    #return token_info
    return response
    """
    import urllib.parse
    return f"{OAUTH_TOKEN_URL}?{urllib.parse.urlencode(PAYLOAD)}"



if __name__ == '__main__':
    print(get_token())
