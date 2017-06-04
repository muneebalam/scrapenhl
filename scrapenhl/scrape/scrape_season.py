import scrapenhl_globals
import scrape_game

def scrape_games(season, games, force_overwrite = False, pause = 1, marker = 10):
    import time
    games = sorted(list(games))
    marker_i = [len(games)//marker * i for i in range(marker)]
    marker_i[-1] = len(games) - 1
    marker_i_set = set(marker_i)
    for i in range(len(games)):
        game = games[i]
        scrape_game.scrape_game(season, game, force_overwrite)
        time.sleep(pause)
        if i in marker_i_set:
            print('Done through', season, game, ' ~ ', round((marker_i.index(i)) * 100/marker), '%')
    print('Done scraping games')


def scrape_full_season(season, startgame = 20001, force_overwrite = False, pause = 1):
    if season != 2012:
        games = [20000 + x for x in range(1, 1231)]
    else:
        games = [20000 + x for x in range(1, 721)]
    for round in range(1, 5):
        for series in range(1, 8//round + 1):
            for game in range(1, 8):
                games.append(int('30{0:d}{1:d}{2:d}'.format(round, series, game)))
    games = [g for g in games if g >= startgame]
    scrape_games(season, games, force_overwrite, pause, 10)

def get_team_pbplog_filename(season, team):
    pass

def get_team_toilog_filename(season, team):
    pass

def update_teamlogs(season, force_overwrite = False):

    teams = set(
        scrapenhl_globals.BASIC_GAMELOG.query('Season == {0:d}'.format(season))['Team'].value_counts().index())

    ### List files in correct format
    import os
    allfiles = os.listdir(scrapenhl_globals.get_season_folder(season))

    pbpfiles = {int(x[:5]): x for x in allfiles if x[-12:] == '_parsed.zlib'}
    toifiles = {int(x[:5]): x for x in allfiles if x[-19:] == '_shifts_parsed.zlib'}

    ### If force overwrite is false, read current log and see which games are already included
    games_already_done = set()

    import feather
    import zlib

    for team in teams:
        teamgames = scrapenhl_globals.BASIC_GAMELOG.query('Season == {0:d} & (Home == "{1:s} | Away == {1:s})'.format(
            season, team))['Game']
        try:
            current_pbp = feather.read_dataframe(get_team_pbplog_filename(season, team))
            games_already_done = {x for x in current_pbp.Game}
        except FileNotFoundError:
            current_pbp = None
            games_already_done = set()

        dflist = []
        if not force_overwrite:
            dflist.append(current_pbp)
            teamgames = {g for g in teamgames if g not in games_already_done}

        if force_overwrite:
            for game in teamgames:
                r = open(scrape_game.get_parsed_save_filename(season, game), 'r')
                page = r.read()
                r.close()

                df = zlib.decompress(zlib)
                dflist.append(df)

        import pandas as pd
        new_pbp = pd.concat(dflist)
        feather.write_dataframe(new_pbp, get_team_pbplog_filename(season, team))

        try:
            current_toi = feather.read_dataframe(get_team_toilog_filename(season, team))
            games_already_done = {x for x in current_toi.Game}
        except FileNotFoundError:
            current_toi = None
            games_already_done = set()

        dflist = []
        if not force_overwrite:
            dflist.append(current_toi)
            teamgames = {g for g in teamgames if g not in games_already_done}

        if force_overwrite:
            for game in teamgames:
                r = open(scrape_game.get_parsed_shifts_save_filename(season, game), 'r')
                page = r.read()
                r.close()

                df = zlib.decompress(zlib)
                ### Columns for players are labeled [Team]1-6, [OppTeam]1-6, so changing opp team names to just 'Opp'
                df.rename(columns={x: 'Opp{0:s}'.format(x[-1]) for col in df.columns if x[:3] != team},
                          inplace=True)
                dflist.append(df)

        import pandas as pd
        new_toi = pd.concat(dflist)
        feather.write_dataframe(new_toi, get_team_toilog_filename(season, team))

def update_playerlog():
    pass

for season in range(2007, 2017):
    scrape_full_season(season)