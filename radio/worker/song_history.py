try:  # try/except to handle both local debugging and cloud running (maybe clean up?)
    from authorize import get_token, get_fileshare_client
except:
    from .authorize import get_token, get_fileshare_client # Check if this every gets called 
from datetime import datetime
import io, json, logging
import pandas as pd 
import requests as r
import os, sys
import numpy as np
import time

real_path = os.path.realpath(__file__)
dir_path = os.path.dirname(real_path)


####### CLOUD HANDLING #############
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
    '''
    typical josn data format:
    '''
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
#####################################


#####    API CALLS     ##############
# Get currently playing
def get_current(token=None) -> dict:
    if not token:
        token = get_token()
    URL = "https://api.spotify.com/v1/me/player"                    # api-endpoint for current playback
    HEAD = {'Authorization': 'Bearer '+token}                       # provide auth. crendtials
    content = r.get(url=URL, headers=HEAD)
    if content.status_code == 200:
        return content.json()
    else:
        return {}


# Request recently played
def get_recents(token=None) -> dict:
    if not token:
        token = get_token()
    URL = "https://api.spotify.com/v1/me/player/recently-played"    # api-endpoint for recently played
    HEAD = {'Authorization': 'Bearer '+token}                       # provide auth. crendtials
    PARAMS = {'limit':50}	                                        # default here is 20
    content = r.get(url=URL, headers=HEAD, params=PARAMS)
    if content.status_code == 200:
        return content.json()
    return {}


def get_durations(ids = '', token=None, store=True) -> pd.DataFrame:
    '''
    API call with built-in cache reader to return
        df (id, artist, duration) 
    '''

    pth = os.path.join(dir_path, 'store', 'duration_df.pkl')

    # ids.pop(ids.index[3]) # TODO: delete when left on checked and working
    durations = pd.DataFrame({
        'id':ids,
        'duration':0
    })
    durations.set_index('id', inplace=True)
    
    print('Looking for cached durations')
    try:
        local_durations = pd.read_pickle(pth)
        durations = durations.merge(local_durations, on='id', left_index=True, right_index=True)
        durations.drop(columns='duration_x', inplace=True)
        durations.rename(columns={'duration_y':'duration'}, inplace=True)
    except Exception as e:
        print('\n\n\n EXCEPTION CODE HERE \n', e)
        print('Nothing stored locally. Calling API...')

    durations.fillna(0, inplace=True)

    ids = durations.index[durations.duration<1]

    if len(ids) > 0:
        print(f'{len(ids)} new ids to check')

        if not token:
            token = get_token()
        batches = (len(ids)//50) + 1
        print(f'Will be executing {batches} API call(s)')

        URL = "https://api.spotify.com/v1/tracks"    # api-endpoint for recently played  
        HEAD = {'Authorization': 'Bearer '+token}                       # provide auth. crendtials

        # batching the unstored indexes incase exceeds max
        for i in range(batches):
            print('Batch', i)
            if i==(batches-1):
                batch_ids = ids[50*i:]  # last set of indices
            else:
                batch_ids = ids[50*i:50*(i+1)]  # forward indexing
            
            print(','.join(batch_ids))
            try:
                b_ids = ','.join(batch_ids)
            except:
                print('Fix song_history line 162') # TODO: make sure new songs are being batched correctly
                break

            PARAMS = {'ids':b_ids}
            tracks = None 
            cnt = 0
            while tracks is None:
                data = r.get(url=URL, headers=HEAD, params=PARAMS).json()
                try:
                    tracks = data['tracks']
                except:
                    print('Bad response. Trying again...')
                    cnt += 1
                    if cnt > 20:
                        return {}
                    time.sleep(2)

            batch_dur = []

            for track in data['tracks']:
                batch_dur.append(track['duration_ms'])
            print(batch_dur)
            durations.duration[batch_ids] = batch_dur
        

        # this only gets stored again when new ids are added
        print(f'Storing at {pth}')
        print(durations.head(3))
        durations.to_pickle(pth)
        print('Success!')

    return durations

#####################################

####   OTHER TOOLS    #####

def update_history_db(model):
    logging.info('Running song-history run() funciton.')
    token = get_token()
    data = get_recents(token=token)
    csv_df, latest = download_to_df()
    csv_df.rename(columns={'name':'track'}, inplace=True)

    # get the largest datetime in db

    # check for entries the have datetimes higher than largest dt

    # only add these entires

    # add for loop
    for f in model._meta.get_fields():
        print(f.name)


# Run
def run() -> bool:
    logging.info('Running song-history run() funciton.')
    token = get_token()
    data = get_recents(token=token)
    csv_df, latest = download_to_df()
    print(csv_df.tail())
    print(latest)
    # spot_df = json_to_df(data=data, latest=latest)
    return csv_df
###########################


if __name__=='__main__':
    # run()
    # update_history_db()
    None
