from datetime import datetime, timedelta
try:
    from .song_history import download_to_df, get_durations
except:
    from song_history import download_to_df, get_durations
import pandas as pd 
import plotly.offline as opy
pd.options.plotting.backend = "plotly"

def to_html(figure):
    context = {}
    div = opy.plot(figure, auto_open=False, output_type='div')
    context['plot'] = div
    return context

def artist_duration(n=37):
    df, mdf = download_to_df()

    # df_count = df.groupby(['artist', 'name'])
    # print(df_count.size().head())

    durations = get_durations(df.id.unique())
    df = df.merge(durations, on='id', how='left')

    df_artist_track = df.groupby(['artist', 'id'])
    duration = df_artist_track['duration'].sum()
    count = df_artist_track.size()

    total_time_artist = (count*duration).groupby('artist').sum()
    total_time_artist.sort_values(ascending=True, inplace=True)

    top_artists_ms = total_time_artist.tail(n)

    top_artists = top_artists_ms//(1000*60*60)

    top_artists = pd.DataFrame(top_artists).reset_index()
    top_artists.columns=['artist', 'hours']
    top_artists.index = [f'Rank: {n-i}' for i in range(n)]
    print(top_artists)

    figure = top_artists.plot.barh(
        x = 'hours',
        y = 'artist',
        color='hours',
        hover_name = top_artists.index,
        template='plotly_dark')
    figure.update(layout_showlegend=False)

    return to_html(figure)

def song_plays(n=37):
    print('Downloading to df()...')
    df, mdf = download_to_df()

    df.rename(columns={'name':'track'}, inplace=True)
    name_artist = df.groupby(['track', 'artist', 'id'])  # TODO: maybe ids in front?
    print(name_artist.size())
    _counts = name_artist.size().reset_index(name='count')
    sorted_counts = _counts.sort_values('count', ascending=True)
    top_songs = sorted_counts.tail(n)

    top_songs.index = ['Rank: '+str(n-i) for i in range(n)]
    print(top_songs.id)


    # ############# this should all be inside a duration f #############
    durations = get_durations(top_songs.id)
    df = top_songs.merge(durations, how='left', on='id')

    df_artist_track = df.groupby(['artist', 'id'])
    duration = df_artist_track['duration'].sum()
    count = df_artist_track.size()


    total_time_artist = (count*duration).groupby('artist').sum()
    total_time_artist.sort_values(ascending=True, inplace=True)
    # print(total_time_artist)

    print('\n\n\n working here\n')
    top_artists_ms = total_time_artist.tail(n) 
    top_artists_ms.rename('%', inplace=True)
    print(top_artists_ms)
    top_artists = 100*top_artists_ms/sum(top_artists_ms)
    top_songs = top_songs.merge(top_artists, how='left', on='artist')
    print('weee')

    #############HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH###################

    print()
    print()
    print('ok..')
    print()
    print()
    figure = top_songs.plot.barh(
        y = 'track',
        x = 'count',
        labels = {
            'artist':'Artist'
        },
        custom_data = ['artist'],
        color='%',
        hover_name = top_songs.index,
        hover_data=['artist', 'track'],
        template='plotly_dark')
    figure.update_layout(
        showlegend=False
    )

    return to_html(figure)

'''
Checklist of things to do:
    X hours per artist
    X songs plays with color 
    - genre plots?
'''

if __name__=='__main__':
    # print('Downloading to df()...')
    # df, mdf = download_to_df()

    # artist_duration()
    song_plays()

    print('end')




