try:  # try/except to handle both local debugging and cloud running (maybe clean up?)
    from authorize import get_token, get_fileshare_client
except:
    from .authorize import get_token, get_fileshare_client # Check if this every gets called 
from datetime import datetime
import io, json, logging
import pandas as pd 
import requests as r

# Request recently played
def get_recents(token) -> dict:
    URL = "https://api.spotify.com/v1/me/player/recently-played"    # api-endpoint for current playback
    HEAD = {'Authorization': 'Bearer '+token}                       # provide auth. crendtials
    PARAMS = {'limit':50}	                                        # default here is 20
    return r.get(url=URL, headers=HEAD, params=PARAMS).json()

# Download csv from FileShare to dataframe
def download_to_df() -> pd.DataFrame:
    file_client = get_fileshare_client('history.csv')                # create FileShareClient
    stream_downloader = file_client.download_file()     # download file as stream
    cloud_text = stream_downloader.content_as_text()    # convert stream to string
    stream = io.StringIO(cloud_text)                    # convert string to stream (is this needed?)
    df = pd.read_csv(stream)                            # convert stream to dataframe
    return df, max(df['played_at'])

# Convert json data to dataframe
def json_to_df(data=None, latest=None) -> pd.DataFrame:
    if not isinstance(data, dict):
        try:
            data = data.json()              # This needs to be cleaned up 
        except:
            return None

    new_entries = pd.DataFrame(columns=['id','played_at','artist','name'])
    if data:
        for song in reversed(data['items']):
            played_at = song['played_at']
            name = song['track']['name'].replace(',','')

            if latest<played_at: #datetime.strptime(played_at, '%Y-%m-%dT%H:%M:%S.%fZ'):
                song_id = song['track']['id']
                artist = song['track']['artists'][0]['name'].replace(',','')

                # Build new entry as dictionary
                new_entry = {
                    'played_at': played_at,
                    'id': song_id,
                    'artist': artist,
                    'name': name 
                    }

                
                new_entries = new_entries.append(new_entry, ignore_index=True) # add entry to df
                try:
                    logging.info(f'New entry added: {new_entry}.')
                except:
                    logging.info('New entry added, but includes invalid character in name.')
            else:
                logging.info(f'Song {name} played at {played_at} already registered.')
                pass

    return new_entries

# Combine dataframes
def combine_dfs(csv_df=None, new_df=None) -> pd.DataFrame:
    if new_df.size == 0:
        return None
    return csv_df.append(new_df, ignore_index=True)

# Convert dataframe to csv
def df_to_csv(df=None) -> str:
    try:
        csv_str = df.to_csv(index=False)
        return csv_str
    except:
        return df

# Upload csv to FileShare
def upload(csv_file=None) -> bool:
    if csv_file:
        try:
            file_share_client = get_fileshare_client('history.csv')
            file_share_client.upload_file(csv_file)
            return True
        except:
            return False
    else:
        return csv_file

# Run
def run() -> bool:
    logging.info('Running song-history run() funciton.')
    token = get_token()
    data = get_recents(token=token)
    csv_df, latest = download_to_df()
    spot_df = json_to_df(data=data, latest=latest)
    if spot_df.size > 0:
        updated_df = combine_dfs(csv_df, spot_df)
        logging.info(updated_df)
        print(updated_df)
        csv_file = df_to_csv(updated_df)
        return upload(csv_file)
    else:
        return None


if __name__=='__main__':
    run()
