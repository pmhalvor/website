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

def to_html(figure):
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

def get_duration_plot(top=37):
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

    total_time_artist = (count*duration).groupby('artist').sum()
    total_time_artist.sort_values(ascending=True, inplace=True)

    top_artists_ms = total_time_artist.tail(top)

    top_artists = top_artists_ms/(1000*60*60)

    print(top_artists)

    figure = top_artists.plot.barh(labels={
                     'value':'hours',
                     'artist':'artists',
                     'variable':'hours'
                 }, color='value',
                 template='plotly_dark')
    figure.update(layout_showlegend=False)

    return to_html(figure)

def artist_duration(n=37):
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

    total_time_artist = (count*duration).groupby('artist').sum()
    total_time_artist.sort_values(ascending=True, inplace=True)

    top_artists_ms = total_time_artist.tail(n)

    top_artists = top_artists_ms//(1000*60*60)

    print(top_artists)

    figure = top_artists.plot.barh(labels={
                     'value':'hours',
                     'artist':'artists',
                     'variable':'hours'
                 }, color='value',
                 template='plotly_dark')
    figure.update(layout_showlegend=False)

    return to_html(figure)

def song_plays(n=37):
    print('Downloading to df()...')
    df, mdf = download_to_df()

    df.rename(columns={'name':'track'}, inplace=True)
    name_artist = df.groupby(['track', 'artist'])
    _counts = name_artist.size().reset_index(name='count')
    sorted_counts = _counts.sort_values('count', ascending=True)
    top_songs = sorted_counts.tail(n)

    top_songs.index = [n-i for i in range(n)]
    print(top_songs)

    figure = top_songs.plot.barh(
        y = 'track',
        x = 'count',
        custom_data = ['artist'],
        color='count',
        hover_name = top_songs.index,
        hover_data=['artist', 'track'],
        template='plotly_dark')
    figure.update_layout(
        showlegend=False
    )

    return to_html(figure)

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
    # print('Downloading to df()...')
    # df, mdf = download_to_df()

    # print('Get durations(df)... ')
    # durations = get_durations(df.id.unique())
    # df = df.merge(durations, on='id', how='left')
    # print(df.head(1))

    # print('Find artist with longest sum duration')
    # df_artist_track = df.groupby(['artist', 'id'])
    # duration = df_artist_track['duration'].sum()
    # count = df_artist_track['count'].sum()

    # (count*duration).hist()

    song_plays()

    print('end')

    # fig = df.plot.



