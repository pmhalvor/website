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

def artist_duration(model=None, n=37):
    if model:
        df = pd.DataFrame(list(model.objects.all().values(
            'artist',
            'track',
            'played_at',
            'track_id'
        )))
        df.rename(columns={'track_id':'id'}, inplace=True)
    else:
        df, mdf = download_to_df()

    print(df.shape)
    durations = get_durations(df.id.unique())
    print(durations.shape)
    df = df.merge(durations, on='id', how='left')

    df_artist_track = df.groupby(['artist', 'id'])
    duration = df_artist_track['duration'].sum()
    count = df_artist_track.size()

    total_time_artist = (count*duration).groupby('artist').sum()
    total_time_artist.sort_values(ascending=True, inplace=True)

    top_artists_ms = total_time_artist.tail(n)

    top_artists = top_artists_ms//(1000*60)

    top_artists = pd.DataFrame(top_artists).reset_index()
    top_artists.columns=['artist', 'hours']
    top_artists.index = [f'Rank: {n-i}' for i in range(n)]

    figure = top_artists.plot.barh(
        x = 'hours',
        y = 'artist',
        color='hours',
        hover_name = top_artists.index,
        template='plotly_dark')
    figure.update(layout_showlegend=False)

    return to_html(figure)

def song_plays(model=None, n=37):
    if model:
        df = pd.DataFrame(list(model.objects.all().values(
            'artist',
            'track',
            'played_at',
            'track_id'
        )))
        df.rename(columns={'track_id':'id'}, inplace=True)
    else:
        print('Downloading to df()...')
        df, mdf = download_to_df()
        df.rename(columns={'name':'track'}, inplace=True)

    name_artist = df.groupby(['track', 'artist', 'id'])  # TODO: maybe ids in front?
    _counts = name_artist.size().reset_index(name='count')
    sorted_counts = _counts.sort_values('count', ascending=True)
    top_songs = sorted_counts.tail(n)



    # ############# this should all be inside a duration f #############
    durations = get_durations(top_songs.id.unique())
    df = top_songs.merge(durations, how='left', on='id')

    df_artist_track = df.groupby(['artist', 'id'])
    duration = df_artist_track['duration'].sum()
    count = df_artist_track.size()


    total_time_artist = (count*duration).groupby('artist').sum()
    total_time_artist.sort_values(ascending=True, inplace=True)

    top_artists_ms = total_time_artist.tail(n) 
    top_artists_ms.rename('%', inplace=True)
    top_artists = 100*top_artists_ms/sum(top_artists_ms)
    top_songs = top_songs.merge(top_artists, how='left', on='artist')
    print(top_songs.head())
    print('LOOK AT MY HEAD!!')
    top_songs.index = ['Rank: '+str(n-i) for i in range(n)]


    #############HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH###################

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
    print(figure)
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




