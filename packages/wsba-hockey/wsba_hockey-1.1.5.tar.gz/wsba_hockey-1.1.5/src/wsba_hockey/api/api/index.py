import pandas as pd
import pyarrow.dataset as ds
import numpy as np
import requests as rs
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import pytz
import feedparser

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"WeakSide Breakout Analysis": "Welcome to the API!"}

@app.get("/articles")
def articles():
    rss = 'https://wsba.substack.com/feed'
    feed = feedparser.parse(rss)

    output = {}
    output['articles'] = []
    
    for entry in feed['entries']:
        year = entry['published_parsed'][0]
        month = entry['published_parsed'][1]
        day = entry['published_parsed'][2]

        date = f'{year}-{month:02}-{day:02}'

        if len(entry['links']) > 0:
            for link in entry['links']:
                if 'image' in link['type']:
                    image = link['href']
                else:
                    image = ''
        else:
            if 'image' in link['type']:
                image = link['href']
            else:
                image = ''

        output['articles'].append(
            {
                'title': entry['title'],
                'summary': entry['summary'],
                'link': entry['link'],
                'guid': entry['id'].replace('https://wsba.substack.com/p/',''),
                'author': entry['author'],
                'published': {'datetime': entry['published'],
                              'date': date},
                'thumbnail': image,
                'content': entry['content'][0]['value']
            }
        )

    return output

@app.get("/nhl/players/{player_id}")
def player(player_id: int):
    player = rs.get(f'https://api-web.nhle.com/v1/player/{player_id}/landing').json()

    return player

@app.get("/nhl/schedule/{date}")
def schedule_info(date: str):
    data = rs.get(f'https://api-web.nhle.com/v1/schedule/{date}').json()
    
    eastern = pytz.timezone('US/Eastern')
    for game in data['gameWeek'][0]['games']:
        game['startTimeEST'] = datetime.strptime(game['startTimeUTC'],'%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.UTC).astimezone(eastern).strftime('%I:%M %p')

    return data

@app.get("/nhl/bracket/{season}")
def schedule_info(season: int):
    year = str(season)[4:8]
    data = rs.get(f'https://api-web.nhle.com/v1/playoff-bracket/{year}').json()
    
    return data

@app.get("/nhl/games/{game_id}")
def pbp(game_id: int):
    info = rs.get(f'https://api-web.nhle.com/v1/gamecenter/{game_id}/play-by-play').json()

    season = info['season']
    dataset = ds.dataset(f's3://weakside-breakout/pbp/parquet/nhl_pbp_{season}.parquet', format='parquet')
    filter_expr = (ds.field('game_id')==game_id)

    table = dataset.to_table(use_threads=True,filter=filter_expr)
    df = table.to_pandas()

    df = df.fillna('')

    team_data = pd.read_csv('https://weakside-breakout.s3.us-east-2.amazonaws.com/info/nhl_teaminfo.csv')[['triCode','seasonId','teamName.default','teamLogo','Primary Color','Secondary Color','WSBA']]

    info = df[['season','season_type','game_id','game_date',
                'venue','venue_location']].drop_duplicates().to_dict(orient='records')[0]
    
    info.update({'notice':'All data and materials are from the National Hockey League.'})

    teams = {}
    for team in ['away','home']:
        df = pd.merge(df,team_data,how='left',left_on=[f'{team}_team_abbr','season'],right_on=['triCode','seasonId']).fillna('')
        mod = '' if team == 'away' else '_y'
        teams.update({team: df[[f'{team}_team_abbr'
                                ,f'{team}_coach',
                                f'teamName.default{mod}',
                                f'teamLogo{mod}',
                                f'Primary Color{mod}',
                                f'Secondary Color{mod}',
                                f'WSBA{mod}']].rename(columns={f'{team}_team_abbr':'team_abbr',f'{team}_coach':'coach',
                                                         f'teamName.default{mod}':'team_name',
                                                         f'teamLogo{mod}':'team_logo',
                                                         f'Primary Color{mod}':'primary_color',
                                                         f'Secondary Color{mod}':'secondary_color',
                                                         f'WSBA{mod}':'WSBA'
                                                         }).drop_duplicates().to_dict(orient='records')[0]})

    play_col = [
        'event_num','period','period_type',
        'seconds_elapsed','period_time','game_time',"strength_state","strength_state_venue","home_team_defending_side",
        "event_type_code","event_type","description","event_reason",
        "penalty_type","penalty_duration","penalty_attribution",
        "event_team_abbr","event_team_venue",
        'num_on', 'players_on','ids_on','num_off','players_off','ids_off','shift_type',
        "event_player_1_name","event_player_2_name","event_player_3_name",
        "event_player_1_id","event_player_2_id","event_player_3_id",
        "event_player_1_pos","event_player_2_pos","event_player_3_pos",
        "event_goalie_name","event_goalie_id",
        "shot_type","zone_code","x","y","x_fixed","y_fixed","x_adj","y_adj",
        "event_skaters","away_skaters","home_skaters",
        "event_distance","event_angle","event_length","seconds_since_last",
        "away_score","home_score", "away_fenwick", "home_fenwick",
        "away_on_1","away_on_2","away_on_3","away_on_4","away_on_5","away_on_6","away_goalie",
        "home_on_1","home_on_2","home_on_3","home_on_4","home_on_5","home_on_6","home_goalie",
        "away_on_1_id","away_on_2_id","away_on_3_id","away_on_4_id","away_on_5_id","away_on_6_id","away_goalie_id",
        "home_on_1_id","home_on_2_id","home_on_3_id","home_on_4_id","home_on_5_id","home_on_6_id","home_goalie_id",
        "event_coach",'xG'
    ]
    
    def sanitize(value):
        if isinstance(value, (np.generic, np.ndarray)):
            return value.item()
        return value

    plays = [
        {k: sanitize(v) for k, v in row.items() if v != ''}
        for row in df[[col for col in play_col if col in df.columns]].to_dict(orient='records')
    ]

    plays = [
        {k: sanitize(v) for k, v in row.items() if v != ''}
        for row in df[[col for col in play_col if col in df.columns]].to_dict(orient='records')
    ]

    return {'info': info,
            'teams': teams,
            'plays': plays
        }