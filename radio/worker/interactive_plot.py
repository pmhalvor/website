import os
import numpy as np
import pandas as pd
import plotly.express as px

from dash import (
    Dash,
    dcc, 
    html, 
    Input, 
    Output, 
    callback
)
from django_plotly_dash import DjangoDash
from datetime import date 
from typing import List

# config
pd.options.plotting.backend = "plotly"
ROOT = os.environ["ROOT"]
STYLE = {
    "font-family": "sans-serif",
    "font-size": "16px",
    "font-weight": "bold",
    "className":"ag-theme-alpine-dark",
    "border-radius": "5px",
    "backgroundColor": "#1b1c22",
    "padding": "10px",
}

def preprocess_features(filename="data/history_features_f23-03-16_t23-12-21.csv", limit=10000):
    """Repeat the lines above to preprocess the full history"""
    # read history file
    history_features = pd.read_csv(filename).tail(limit)
    # time features
    history_features["timestamp"] = pd.to_datetime(history_features["played_at"], format='mixed').dt.tz_convert("Europe/Oslo")
    history_features = history_features.sort_values("timestamp")
    history_features["hour"] = history_features["timestamp"].dt.hour
    history_features["month"] = history_features["timestamp"].dt.month
    # add play count
    play_count = history_features.groupby(["id"]).size().rename("play_count")
    history_features.drop(columns=["play_count"], inplace=True) if "play_count" in history_features.columns else None
    history_features = history_features.merge(play_count, on="id", how="left")
    history_features = history_features.sort_values("timestamp").drop_duplicates(subset=["timestamp"], keep="last")  # clean up after join
    # session id
    history_features["session_id"] = history_features["timestamp"].diff().dt.total_seconds().gt(1800).cumsum()
    return history_features


def scatter(df, labels={}):
    """Copy paste from above"""
    return px.scatter(
        df.reset_index(drop=True), 
        x="valence", 
        range_x=[0, 1.1],

        y="energy", 
        range_y=[0, 1.1],
        
        color="tempo",
        # range_color=[0, 1.1],

        size="danceability",
        
        hover_name="track", 
        hover_data=[*labels.keys()],
        template="plotly_dark",

        title="Audio Features (scatter)",
        labels={label:label.upper() for label in df.columns} if not labels else labels
    )


def replace(d:dict, **kwargs):
    d = d.copy()
    d.update(kwargs)
    return d


def interative_scatter_per_session(app, df, max_sessions=25):
    # instead of month and hour, we use session id dropdown
    app.layout = html.Div([
        dcc.Graph(id='graph-with-slider'),

        dcc.Markdown("Date range and session id", style=replace(STYLE,color="white")),
        html.Div([
            # date picker range
            dcc.DatePickerRange(
                id='date-picker-range',
                min_date_allowed=df['timestamp'].min().date(),
                max_date_allowed=df['timestamp'].max().date(),
                initial_visible_month=df['timestamp'].max().date(),
                start_date=df['timestamp'].min().date(),
                end_date=df['timestamp'].max().date(),
                style=replace(STYLE, float="left"),
            ),

            # session id dropdown
            dcc.Dropdown(
                id='session-id-dropdown',
                options=[{'label': str(session_id), 'value': session_id} for session_id in df['session_id'].unique()],
                value=[df['session_id'].unique()[0]],
                multi=True,
                placeholder="Select session id from current date range",
                style=replace(STYLE, float="left")
            ),

        ], style={"display":"inline-block", "padding": "10px"}),           

        # play count slider
        dcc.Markdown("Play count", style=replace(STYLE,color="white")),
        dcc.RangeSlider(
            id='play-count-range-slider', 
            marks=None, 
            # marks={str(play_count): str(play_count) for play_count in df['play_count'].unique()},
            max=df['play_count'].max(),
            min=1,
            step=1,
            tooltip={"placement": "bottom", "always_visible": True},
            value=[0, df['play_count'].max()],
        ),

    ], style=replace(STYLE, backgroundColor="black"))

    @app.callback(
        Output('session-id-dropdown', 'value'),
        Output('session-id-dropdown', 'options'),
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date'),
    )
    def update_session_id_dropdown(start_date, end_date):
        filtered_df = df.copy()
        filtered_df = filtered_df[filtered_df.timestamp.between(
            start_date,
            end_date
        )]

        return (
            filtered_df['session_id'].unique()[:max_sessions],  # values default to first 'max_sessions' session ids
            [{'label': str(session_id), 'value': session_id} for session_id in filtered_df['session_id'].unique()] # options for all session ids within date range
        )
    

    @app.callback(
        Output('play-count-range-slider', 'max'),
        Output('play-count-range-slider', 'value'),
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date'),
    )
    def update_play_count_range(start_date, end_date):
        filtered_df = df.copy()
        filtered_df = filtered_df[filtered_df.timestamp.between(
            start_date,
            end_date
        )]

        # play count should be recalculated based on filtered data
        play_count = filtered_df.groupby(["id"]).size().rename("play_count")
        max_play_count = play_count.max() if play_count.any() else 1

        return (
            max_play_count,
            [0, max_play_count],
        )
    

    @app.callback(
        Output('graph-with-slider', 'figure'),
        Input('session-id-dropdown', 'value'),
        Input('play-count-range-slider', 'value'),
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date'),
    )
    def update_figure(
        session_ids_dropdown,
        play_count_range,
        start_date, 
        end_date
        ):
        filtered_df = df.copy()

        # filter by date range
        filtered_df = filtered_df[filtered_df.timestamp.between(
            start_date, 
            end_date
        )]

        # play count should be recalculated based on filtered data (before session, since session ids can be truncated)
        play_count = filtered_df.groupby(["id"]).size().rename("play_count")
        if play_count.any():
            filtered_df.drop(columns=["play_count"], inplace=True) if "play_count" in filtered_df.columns else None
            filtered_df = filtered_df.merge(play_count, on="id")
            filtered_df = filtered_df[filtered_df.play_count.between(play_count_range[0], play_count_range[1])]
        else:
            filtered_df = filtered_df[filtered_df.play_count.between(0, 1)]

        # default to first session id if none selected
        session_ids_dropdown = session_ids_dropdown if session_ids_dropdown else filtered_df['session_id'].unique()[:1]
        filtered_df = filtered_df[filtered_df.session_id.isin(session_ids_dropdown)]

        # clean labels 
        labels={
            "valence": "Positivity",
            "energy": "Energy",
            "tempo": "Tempo",
            "danceability": "Danceability",
            "track": "Track",
            "play_count": "Play count",
            "session_id": "Session id",
        }

        return scatter(filtered_df, labels).update_layout(
            transition_duration=500, 
            title="Audio Features (scatter) <br>" \
                "<sup>Session IDs {session_ids} - Play counts {play_counts} - Dates {dates}</sup>".format(
                session_ids=str([session_ids_dropdown[0], session_ids_dropdown[-1]]).replace("'", ""),
                play_counts=str(play_count_range),
                dates=str([
                    filtered_df[filtered_df["session_id"].isin(session_ids_dropdown)]["timestamp"].min().date().strftime('%d %B %Y'),
                    filtered_df[filtered_df["session_id"].isin(session_ids_dropdown)]["timestamp"].max().date().strftime('%d %B %Y'),
                ]).replace("'", ""),
            ),
        )
     
    return app


if __name__ == "__main__":
    # init app
    app = DjangoDash("AudioFeatures", add_bootstrap_links=True)

    # load data
    history_features = pd.read_csv(f"{ROOT}/data/history_features.csv", parse_dates=["timestamp"])

    app = interative_scatter_per_session(app, history_features, max_sessions=25)
    app.ext
    app.run_server(debug=True, use_reloader=False)