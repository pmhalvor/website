try:  # try/except to handle both local debugging and cloud running (maybe clean up?)
    from authorize import get_token 
except:
    from .authorize import get_token 
from datetime import datetime
import io, json, logging
import pandas as pd 
import requests as r
import os 
import pickle

real_path = os.path.realpath(__file__)
dir_path = os.path.dirname(real_path)
ROOT = os.environ.get("ROOT")
MAX_ID_COUNT=50

####### DATA WRANGLING #############
def load_df() -> pd.DataFrame:
    if os.path.exists(f'{ROOT}/data/history.csv'):
        df = pd.read_csv(f'{ROOT}/data/history.csv')
        print("loaded from", f'{ROOT}/data/history.csv')
    else:
        df = pd.read_csv('~/data/history.csv')
        print("loaded from", '~/data/history.csv')

    print("Max played at", max(df["played_at"]))
    return df, max(df["played_at"])

# Convert json data to dataframe
def json_to_df(data=None, latest=None) -> pd.DataFrame:
    '''
    typical josn data format:
    '''
    if not isinstance(data, dict):
        try:
            data = data.json()              # This needs to be cleaned up 
        except:
            print("Problem converting data of type {} to dict".format(type(data)))
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
                    print(f'New entry added: {new_entry}.')
                except:
                    logging.info('New entry added, but includes invalid character in name.')
                    print('New entry added, but includes invalid character in name.')
            else:
                logging.info(f'Song {name} played at {played_at} already registered.')
                print(f'Song {name} played at {played_at} already registered.')
                pass

    return new_entries


# Combine dataframes
def combine_dfs(csv_df=None, new_df=None) -> pd.DataFrame:
    if new_df.size == 0:
        return csv_df
    return csv_df.append(new_df, ignore_index=True)


# Convert dataframe to csv
def df_to_csv(df=None) -> str:
    try:
        if os.path.exists(f'{ROOT}/data/history.csv'):

            csv_str = df.to_csv(f'{ROOT}/data/history.csv', index=False)
        else:
            csv_str = df.to_csv('~/data/history.csv', index=False)

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

def get_durations(id_list = '', token=None, store=True):
    """
    Should both load the previously stored duraitons and join with new durations.

    """
    pth = os.path.join(dir_path, 'store', 'duration_df.pkl')

    # load durations pickle
    with open(pth, 'rb') as f:
        durations = pickle.load(f)

    # check if current ids have already stored durations
    for i in durations.id:
        try:
            idx = id_list.index(i)
            id_list.pop(idx)
        except:
            pass

    print(f'{len(id_list)} new ids to check')
    if len(id_list) > 0:
        # create new df 
        new_durations = pd.DataFrame({
            'id':id_list,
            'duration': 0
        })
        
        ids = new_durations.id[new_durations.duration<1]


        if not token:
            token = get_token()
        batches = (len(id_list)//MAX_ID_COUNT) + 1
        print(f'Will be executing {batches} API call(s)')

        URL = "https://api.spotify.com/v1/tracks"    # api-endpoint for recently played  
        HEAD = {'Authorization': 'Bearer '+token}    # provide auth. crendtials

        # batching the unstored indexes incase exceeds max
        for i in range(batches):
            print('Batch', i)
            if i==(batches-1):
                batch_ids = ids[MAX_ID_COUNT*i:]  # last set of indices
                print("Checking indexes: {} -> {}".format(MAX_ID_COUNT*i, MAX_ID_COUNT*(i+1)) )
            else:
                batch_ids = ids[MAX_ID_COUNT*i:MAX_ID_COUNT*(i+1)]  # forward indexing
                print("Checking indexes: {} -> {}".format(MAX_ID_COUNT*i, MAX_ID_COUNT*(i+1)) )

            b_ids = ','.join(batch_ids)

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

            batch_durations = []
            
            if data.get('tracks'):
                for track in data['tracks']:
                    batch_durations.append(track['duration_ms'])
            
                batch_dur = pd.DataFrame({"duration": batch_durations}).set_index(batch_ids.index)
                new_durations.update(batch_dur)


            else:
                print('No tracks in response')
                data["python_log"] = {
                    "message": 'No tracks in response.',
                    "input": {
                        "URL": URL, 
                        "header": HEAD, 
                        "params": PARAMS
                    },
                    "batch_ids_to_str": str(batch_ids)
                }
                with open(os.path.join(dir_path, 'store', 'error_response.json'), 'w+') as f:
                    json.dump(data, f)

            print(new_durations[new_durations.index.isin(batch_ids)])

        # this only gets stored again when new ids are added
        print(f'Storing at {pth}')
        new_durations.to_pickle(pth)
        print('Success!')


    return durations 

#####################################

####   OTHER TOOLS    #####
# bacthes, taken from https://code.activestate.com/recipes/303279-getting-items-in-batches/
""" def batch(iterable, size):
    '''
    DEPRECATED
    '''
    sourceiter = iter(iterable)
    while True:
        batchiter = islice(sourceiter, size)
        yield chain([batchiter.next()], batchiter)
 """

# Run all steps from this file
def run() -> bool:
    logging.info('Running song-history run() function.')
    token = get_token()
    data = get_recents(token=token)
    print("Recents: ", len(data))

    csv_df, latest = load_df()
    print("End of csv df:", csv_df.tail())

    spot_df = json_to_df(data=data, latest=latest)
    print("End of recent df", spot_df.tail())

    updated_df = combine_dfs(csv_df, spot_df)
    df_to_csv(updated_df)
    print("End up updated df", updated_df.tail())

    return updated_df
###########################


if __name__=='__main__':
    # run()
    # update_history_db()
    None
