import base64, json, os, requests, six, time

# import environment variables
SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')         # Spotify client id stored as local env. var.
SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET') # Spotify client secret stored as local env. var.
SPOTIFY_REDIRECT_URI = os.environ.get('SPOTIFY_REDIRECT_URI', "https://localhost:8888/callback")  #  Redirect uri stored as local env. var.
ROOT = os.environ.get('ROOT')   # because local paths change between machines

assert SPOTIFY_CLIENT_ID
assert SPOTIFY_CLIENT_SECRET
assert ROOT


# Authorization for Spotify
def get_token(code = None) -> str:
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

    if cache_token.get("access_token"): 
        if is_token_expired(cache_token):
            cache_token = refresh_access_token(cache_token['refresh_token'])
    elif code:
        cache_token = get_token_first_time(code)
        store_renewed_token(cache_token)
    else:
        login_to_authorize()
        return None

    return cache_token.get("access_token", cache_token.get("token"))  # keep default return value as before to not break prod code


# Read cached token from FileShare
def get_cache_token() -> dict:
    """
    Steps:
        X load local data
        X return data as dict
    """
        
    path = f'{ROOT}/.data' 
    if os.path.exists(f'{ROOT}/.data'):
        with open(path, 'r') as f:
            data = json.load(f)
            print(f"Loaded cache_token data: \n {data}")
    else:
        data = {}
    return data      
    

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

    time_difference = now - int(token_info.get("timestamp", 0))
    print(f"Time difference: {time_difference}")
    expired = time_difference > 3600

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
    with open(f'{ROOT}/.data', 'w+') as f:
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
        'redirect_uri': SPOTIFY_REDIRECT_URI,
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


# Build url to generate access code (cannot use requests to call)
def login_to_authorize():
    """
    Can not call requests to get access code.
    """

    # parameters for post request
    OAUTH_TOKEN_URL = "https://accounts.spotify.com/authorize"
    PAYLOAD = {
        'client_id': SPOTIFY_CLIENT_ID,
        'scope': 'user-read-currently-playing',
        'redirect_uri': SPOTIFY_REDIRECT_URI,
        'state': 1337,
        'response_type': 'code'
    }
    
    # get request to authoirize urtl
    response = requests.get(
        url=OAUTH_TOKEN_URL,
        params=PAYLOAD,
    )

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    
    print("You need to log in using this url: ")
    print(response.url)
    
    print("After logging in, you will be redirected to a url that looks like this: ")
    print("https://localhost:8888/callback?code=<SOME_LONG_HASH_CODE>&state=1337")
    print("Copy the url and feed it into the get_code_from_url function to get the code.")


def get_code_from_url(url):
    """
    Get code from url
    """
    code = url.split("code=")[1].split("&state")[0]
    return code


if __name__ == '__main__':
    print(get_token())
