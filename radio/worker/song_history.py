try:  # try/except to handle both local debugging and cloud running (maybe clean up?)
    from authorize import get_token #, get_fileshare_client
except:
    from worker.authorize import get_token #, get_fileshare_client # Check if this every gets called 
from datetime import datetime
import io, json, logging
import pandas as pd 
import requests as r
import os 
import pickle

real_path = os.path.realpath(__file__)
dir_path = os.path.dirname(real_path)

####### DATA WRANGLING #############
def load_df() -> pd.DataFrame:
    df = pd.read_csv("../../data/history.csv")
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
        csv_str = df.to_csv("../../data/history.csv", index=False)
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
    return r.get(url=URL, headers=HEAD, params=PARAMS).json()

def get_durations(ids = '', token=None, store=True):
    pth = os.path.join(dir_path, 'store', 'duration_df.pkl')

    # ids.pop(ids.index[3]) # TODO: delete when left on checked and working
    durations = pd.DataFrame({
        'id':ids
    })
    
    print('Looking for cached durations')
    try:
        # local_durations = pd.read_csv(os.path.join(dir_path, 'store/durations.csv'))
        local_durations = pd.read_pickle(pth)
        id_ = local_durations.index
        local_durations.reset_index(inplace = True)
        local_durations['id'] = id_
        del id_
        print('Found local durations')
    except Exception as e:
        print('Nothing stored locally. Calling API...')
        local_durations = pd.DataFrame(durations)

    # durations = durations.merge(local_durations,how='outer', on='id')
    durations = pd.concat([local_durations, durations])
    durations = durations.drop_duplicates('id', keep='first', ignore_index=True)
    durations.fillna(0, inplace=True)
    try:
        durations.drop(columns='count')
    except:
        print('No count colmun to drop.\n\
        Remove this call on line 132 in song_history.py')

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
            if i==(batches-1):
                batch_ids = ids[50*i:]  # last set of indices
            else:
                batch_ids = ids[50*i:50*(i+1)]  # forward indexing
            
            b_ids = ','.join(batch_ids)

            PARAMS = {'ids':b_ids}	
            data = r.get(url=URL, headers=HEAD, params=PARAMS).json()

            batch_dur = []

            for track in data['tracks']:
                batch_dur.append(track['duration_ms'])
            
            durations.duration[batch_ids] = batch_dur
        
            print(durations[durations.index.isin(batch_ids)])

        # this only gets stored again when new ids are added
        print(f'Storing at {pth}')
        durations.to_pickle(pth)
        print('Success!')

    return durations
#####################################

####   OTHER TOOLS    #####
# bacthes, taken from https://code.activestate.com/recipes/303279-getting-items-in-batches/
def batch(iterable, size):
    '''
    Try replacing my bacthing with something similar
    '''
    sourceiter = iter(iterable)
    while True:
        batchiter = islice(sourceiter, size)
        yield chain([batchiter.next()], batchiter)


# Run all steps from this file
def run() -> bool:
    logging.info('Running song-history run() function.')
    token = get_token()
    data = get_recents(token=token)
    csv_df, latest = load_df()
    print("End of csv df:", csv_df.tail())
    spot_df = json_to_df(data=data, latest=latest)
    print("End of recent df", spot_df.tail())
    updated_df = combine_dfs(csv_df, spot_df)
    df_to_csv(updated_df)
    return updated_df
###########################


if __name__=='__main__':
    run()
