from azure.storage.fileshare import ShareFileClient
import base64, logging, io, json, os, requests, six, time

# import environment varaibles
SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')         # Spotify cliient id stored as local env. var.
SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET') # Spotify client secret stored as local env. var.
AZURE_STORAGE = os.environ.get('AZURE_STORAGE')                 # Connection string stored as local env. var.


# Authorization for Spotify
def get_token() -> str:
    '''
    Steps:
        X get token from fileshare
        X check if access_token is expired:
            X it is expired:
                X call token url with correct parameters and headers
                X update token_info in FileShare cache  
        X return access token
    '''
    cache_token = get_cache_token()

    if is_token_expired(cache_token):
        cache_token = refresh_access_token(cache_token['refresh_token'])

    return cache_token['access_token']

# Read cached token from FileShare
def get_cache_token() -> dict:
    file_client = get_fileshare_client('.cache-pmhalvor')
    stream_downloader = file_client.download_file()     # download file as stream
    cloud_text = stream_downloader.content_as_text()    # convert stream to string
    return json.loads(cloud_text)                # convert string to dictionary
    
# Check if cached token is still valid 
def is_token_expired(token_info) -> bool:
    now = int(time.time())

    try:
        expired = token_info["expires_in"] - now < 60
    except:
        expired = True  # TODO: clean this up
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

    # response do not include refresh_token, must be added manually
    if 'refresh_token' not in token_info:
        token_info['refresh_token'] = refresh_token

    # Make sure FileShare stays up to date
    upload_renewed_token(token=token_info)

    return token_info

# Make header for token request
def make_headers() -> dict:
    client_id = SPOTIFY_CLIENT_ID         # Spotify cliient id stored as local env. var.
    client_secret = SPOTIFY_CLIENT_SECRET # Spotify client secret stored as local env. var.

    # base64 encoded string
    client = base64.b64encode(
        six.text_type(f'{client_id}:{client_secret}').encode('ascii')
    )
    return {"Authorization": f"Basic {client.decode('ascii')}"}

# Update cache in FileShare
def upload_renewed_token(token):
    if not isinstance(token, str):
        token = json.dumps(token)
    file_client = get_fileshare_client('.cache-pmhalvor')
    file_client.upload_file(token)

# Get FileShare clients
def get_fileshare_client(file_path) -> ShareFileClient:
    conn_str = AZURE_STORAGE  # Connection string stored as local env. var.
    return ShareFileClient.from_connection_string(conn_str=conn_str, share_name='history', file_path=file_path)
    

if __name__ == '__main__':
    print(get_token())
