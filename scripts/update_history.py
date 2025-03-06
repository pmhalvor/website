from radio.models import History
from radio.worker.song_history import download_to_df
from old_tools.table import add_df
from datetime import datetime
import pandas as pd

def run():
    # get data from csv (from azure)
    data, latest = download_to_df()
    dt_played_at = pd.to_datetime(data.played_at)

    # get lastest entry in db
    obj = History.objects.order_by('-played_at')[0]
    latest_db = obj.played_at

    # get only entries that are not currently in db
    new_idx = dt_played_at>latest_db
    new_data = data.loc[new_idx]

    # add new entries to db
    errors = add_df(History, new_data, columns={'id':'track_id', 'name':'track'})

    # store errors
    with open('history_errors.txt', 'a+') as f:
        f.writelines(errors)
        f.write('\n')
