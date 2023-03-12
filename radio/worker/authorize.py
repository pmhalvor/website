import base64, logging, io, json, os, requests, six, time

# import environment variables
SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')         # Spotify client id stored as local env. var.
SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET') # Spotify client secret stored as local env. var.
AZURE_STORAGE = os.environ.get('AZURE_STORAGE')                 # Connection string stored as local env. var.
ROOT = os.environ.get('ROOT', os.getcwd())   # because local paths change between machines


# Authorization for Spotify
def get_token(name=".data") -> str:
    '''
    Steps:
        X get token from local file ".data"
        X check if access_token is expired:
            X it is expired:
                X call token url with correct parameters and headers
                X update .data with new tokens  
        X return access token
    '''
    cache_token = get_cache_token(name)

    if is_token_expired(cache_token):
        cache_token = refresh_access_token(cache_token['refresh_token'], name)

    return cache_token['token']


# Read cached token from FileShare
def get_cache_token(name=".data") -> dict:
    """
    Steps:
        X load local data
        X return payload
    """
        
    path = f'{ROOT}/{name}' if os.path.exists(f'{ROOT}/{name}') else f'~/{name}'
    if os.path.exists(path):
        with open(path, 'r') as f:
            data = json.load(f)
            payload = {
                "refresh_token": data.get("refresh_token", data.get("access_token")),
                "timestamp": data["timestamp"],
                "token": data["token"],
            }
    else:
        payload = {"status_code": 404}
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
    return expired


# Refresh token from cache
def refresh_access_token(refresh_token, name=".data") -> dict:
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
    store_renewed_token(payload, name)

    return payload


# Make header for token request
def make_headers(
    client_id = SPOTIFY_CLIENT_ID,         # Spotify cliient id stored as local env. var.
    client_secret = SPOTIFY_CLIENT_SECRET  # Spotify client secret stored as local env. var.
) -> dict:

    # base64 encoded string
    client = base64.b64encode(
        six.text_type(f'{client_id}:{client_secret}').encode('ascii')
    )
    return {"Authorization": f"Basic {client.decode('ascii')}", "Content-Type": "application/x-www-form-urlencoded"}


# Store the renewed token locally 
def store_renewed_token(token_info, name=".data"):
    if os.path.exists(f'{ROOT}/{name}'):
        with open(f'{ROOT}/{name}', 'w') as f:
            json.dump(token_info, f, indent=4)
    else:
        with open(f'~/{name}', 'w') as f:
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

    return token_info


# Simpler login method built for .infotrac
def get_client_token(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET) -> dict:
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
        'grant_type': 'client_credentials',
        'redirect_uri': 'https://localhost:8888/callback',
    }
    HEADERS = make_headers(client_id, client_secret)
    
    # post request
    response = requests.post(
        url=OAUTH_TOKEN_URL,
        data=PAYLOAD,
        headers=HEADERS,
    )

    if response.status_code == 200:
        token_info = transform(response)
    else: 
        token_info = response

    return token_info


# transform response from client_credentials call
def transform(response):
    data = response.json()

    access_token = data.get("access_token")
    timestamp = int(time.time())
    expires = timestamp + data.get("expires_in")

    return {
        "access_token": access_token, 
        "timestamp": timestamp, 
        "expires": expires
    }


# Build url to generate access code (cannot use requests to call)
def get_code():
    """
    Can not call requests to get access code.
    """

    # parameters for post request
    OAUTH_TOKEN_URL = "https://accounts.spotify.com/authorize"
    PAYLOAD = {
        'client_id': '9656ff22d7604d078e98e54a1870b92d',
        'scope': 'user-read-currently-playing',
        'redirect_uri': 'https://localhost:8888/callback',
        'state': 1111000011110000,
        'response_type': 'code'
    }
    HEADERS = make_headers()
    
    # post request
    response = requests.post(
        url=OAUTH_TOKEN_URL,
        data=PAYLOAD,
        # headers=HEADERS
    )
    token_info = response.json()

    print(token_info)

    return token_info


if __name__ == '__main__':
    print(get_token())
