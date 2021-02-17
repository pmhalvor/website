from datetime import datetime, timedelta
try:
    from .song_history import download_to_df, get_durations
except:
    from song_history import download_to_df, get_durations
import pandas as pd 
import plotly.offline as opy
pd.options.plotting.backend = "plotly"

####### being used
def top(df, n=25, show=False):
    artists = df['artist'].value_counts()
    songs = df['name'].value_counts()
    return artists[:n],  songs[:n]

def past_months(df, number_of_months=1):
    then_dt = datetime.now()
    prior = then_dt.month - number_of_months
    if prior < 1: 
        prior += 12
        then_dt = then_dt.replace(year = then_dt.year-1) 
    then_dt = then_dt.replace(month = prior)
    then = then_dt.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'Z'
    return df[df['played_at']>then]

def to_html(figures):
    context = {}
    div = opy.plot(figure, auto_open=False, output_type='div')
    context['plot'] = div
    return context

def get_plot():
    df, mdf = download_to_df()

    past_6_months = past_months(df, 6)

    top_25_artists, top_25_songs = top(past_6_months)

    fig_artist = top_25_artists.plot.barh()
    fig_song   = top_25_songs.plot.barh()
    figure = [fig_artist, fig_song]

    return to_html(fig_artist)

######################

# def unzip(df):
#     return df.index, df.values

# def plot(df):
#     context = {}
#     figure = df.plot.barh()
#     div = opy.plot(figure, auto_open=False, output_type='div')
#     context['plot'] = div
#     return context


'''
Checklist of things to do:

    - hours per artist
    - songs as color variables 
    - genre plots?

'''

if __name__=='__main__':
    print('Downloading to df()...')
    df, mdf = download_to_df()

    print('Get durations(df)... ')
    durations = get_durations(df.id.unique())
    df = df.merge(durations, on='id', how='left')
    print(df.head(1))

    print('Find artist with longest sum duration')
    df_artist_track = df.groupby(['artist', 'id'])
    duration = df_artist_track['duration'].sum()
    count = df_artist_track['count'].sum()

    (count*duration).hist()


    print('end')

    # fig = df.plot.



