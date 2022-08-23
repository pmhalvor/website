from datetime import datetime, timedelta
try:
    from .song_history import load_df
    from .song_history import  get_durations
except:
    from song_history import load_df
    from song_history import  get_durations
import pandas as pd 
import plotly.offline as opy
pd.options.plotting.backend = "plotly"

####### being used
def to_html(figure):
    context = {}
    div = opy.plot(figure, auto_open=False, output_type='div')
    context['plot'] = div
    return context

def artist_duration(n=37):
    df, mdf = load_df()

    durations = get_durations(df.id.unique())
    df = df.merge(durations, on='id', how='left')

    df_artist_track = df.groupby(['artist', 'id'])
    duration = df_artist_track['duration'].sum()
    count = df_artist_track['count'].sum()

    total_time_artist = (count*duration).groupby('artist').sum()
    total_time_artist.sort_values(ascending=True, inplace=True)

    top_artists_ms = total_time_artist.tail(n)

    top_artists = top_artists_ms//(1000*60*60)

    top_artists = pd.DataFrame(top_artists).reset_index()
    top_artists.columns=['artist', 'time']
    top_artists.index = [f'Rank: {n-i}' for i in range(n)]
    print(top_artists)

    figure = top_artists.plot.barh(
        x = 'time',
        y = 'artist',
        color='time',
        hover_name = top_artists.index,
        template='plotly_dark')
    figure.update(layout_showlegend=False)

    return to_html(figure)

def song_plays(n=37):
    print('Downloading to df()...')
    df, mdf = load_df()

    df.rename(columns={'name':'track'}, inplace=True)
    name_artist = df.groupby(['track', 'artist'])
    _counts = name_artist.size().reset_index(name='count')
    sorted_counts = _counts.sort_values('count', ascending=True)
    top_songs = sorted_counts.tail(n)

    top_songs.index = ['Rank: '+str(n-i) for i in range(n)]
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

'''
Checklist of things to do:
    X hours per artist
    X songs plays with color 
    - genre plots?
'''

if __name__=='__main__':
    # print('Downloading to df()...')
    # df, mdf = load_df()

    # song_plays()
    artist_duration()

    print('end')




