import base64
import datetime 
import os 
import requests
import time 


def cd_up_dir(n=1, symbol="/"):
    current_dir = os.getcwd()

    split_dir = current_dir.split(symbol)

    to_dir = symbol.join(split_dir[:-n])

    print("Moving to {}...".format(to_dir))
    os.chdir(to_dir)
    print("Current working directory: {}".format(os.getcwd()))


def cd_to(subdir="", full_path=None):
    if full_path is None:
        current_dir = os.cwd()
        to_dir = os.path.join(current_dir, subdir)
    else:
        to_dir = full_path
    

    print("Moving to {}...".format(to_dir))
    os.chdir(to_dir)
    print("Current working directory: {}".format(os.getcwd()))


# Refresh token from cache
def refresh_access_token(
        client_id,
        client_secret,
        refresh_token, 
        name=".data",
        url="https://www.strava.com/api/v3/oauth/token",
    ) -> dict:
    '''
    Request Parameters
    client_id
    required integer, in query	The application’s ID, obtained during registration.
    client_secret
    required string, in query	The application’s secret, obtained during registration.
    grant_type
    required string, in query	The grant type for the request. When refreshing an access token, must always be "refresh_token".
    refresh_token
    required string, in query	The refresh token for this user, to be used to get the next access token for this user. Please expect that this value can change anytime you retrieve a new access token. Once a new refresh token code has been returned, the older code will no longer work.

    Steps:
        X set correct payload (refresh_token) 
        X set correct header  (client id and secret)
        X post request 
        X convert response to json
        X update token_info in FileShare cache  
        X return token info
    '''
    # parameters for post request
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token',
        'scope': 'read'
    }
    headers = {}
    
    # post request
    response = requests.post(
        url=url,
        data=payload,
        headers=headers,
    )
    token_info = response.json()

    print(f"Returned token info: \n {token_info}")

    payload = token_info
    # payload = {
    #     # "refresh_token": token_info.get("refresh_token", refresh_token),
    #     # "token": token_info.get("access_token"),
    #     # "timestamp": int(time.time())
    # }

    # store tokens for later
    # store_renewed_token(payload, name)

    return payload


# Make header for token request
# def make_headers(
#     client_id,          # Spotify cliient id stored as local env. var.
#     client_secret,      # Spotify client secret stored as local env. var.
# ) -> dict:

#     # base64 encoded string
#     client = base64.b64encode(
#         # six.text_type(f'{client_id}:{client_secret}').encode('ascii')
#         # f'{client_id}:{client_secret}'.encode('ascii')
#     )
#     return {"Authorization": f"Basic {client.decode('ascii')}", "Content-Type": "application/x-www-form-urlencoded"}


# # Store the renewed token locally 
# def store_renewed_token(token_info, name=".data"):
#     if os.path.exists(f'{ROOT}/{name}'):
#         with open(f'{ROOT}/{name}', 'w') as f:
#             json.dump(token_info, f, indent=4)
#     else:
#         with open(f'~/{name}', 'w') as f:
#             json.dump(token_info, f, indent=4)
#     return True


# # Get first token with access code
# def get_token_first_time(code) -> dict:
#     '''
#     Steps:
#         X set correct payload (refresh_token) 
#         X set correct header  (client id and secret)
#         X post request 
#         X convert response to json
#         X update token_info in FileShare cache  
#         X return token info
#     '''
#     # parameters for post request
#     OAUTH_TOKEN_URL = "https://accounts.spotify.com/api/token"
#     PAYLOAD = {
#         'grant_type': 'authorization_code',
#         'redirect_uri': 'https://localhost:8888/callback',
#         'code': code,
#     }
#     HEADERS = make_headers()
    
#     print(
#         f"""
#         url: {OAUTH_TOKEN_URL}
#         data: {PAYLOAD}
#         header: {HEADERS}
#         """
#     )
#     # post request
#     response = requests.post(
#         url=OAUTH_TOKEN_URL,
#         data=PAYLOAD,
#         headers=HEADERS
#     )
#     token_info = response.json()

#     print(token_info)

#     return token_info


# # Simpler login method built for .infotrac
# def get_client_token(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET) -> dict:
#     '''
#     Steps:
#         X set correct payload (refresh_token) 
#         X set correct header  (client id and secret)
#         X post request 
#         X convert response to json
#         X update token_info in FileShare cache  
#         X return token info
#     '''
#     # parameters for post request
#     OAUTH_TOKEN_URL = "https://accounts.spotify.com/api/token"
#     PAYLOAD = {
#         'grant_type': 'client_credentials',
#         'redirect_uri': 'https://localhost:8888/callback',
#     }
#     HEADERS = make_headers(client_id, client_secret)
    
#     # post request
#     response = requests.post(
#         url=OAUTH_TOKEN_URL,
#         data=PAYLOAD,
#         headers=HEADERS,
#     )

#     if response.status_code == 200:
#         token_info = transform(response)
#     else: 
#         token_info = response

#     return token_info

# # transform response from client_credentials call
# def transform(response):
#     data = response.json()

#     access_token = data.get("access_token")
#     timestamp = int(time.time())
#     expires = timestamp + data.get("expires_in")

#     return {
#         "access_token": access_token, 
#         "timestamp": timestamp, 
#         "expires": expires
#     }



