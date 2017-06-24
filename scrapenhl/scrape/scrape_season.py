import scrapenhl_globals
import scrape_game

def scrape_games(season, games, force_overwrite = False, pause = 1, marker = 10):
    """
    Scrapes the specified games.

    Parameters
    -----------
    season : int
        The season of the game. 2007-08 would be 2007.
    games : iterable of ints (e.g. list)
        The game id. This can range from 20001 to 21230 for regular season, and 30111 to 30417 for playoffs.
        The preseason, all-star game, Olympics, and World Cup also have game IDs that can be provided.
    force_overwrite : bool
        If True, will overwrite previously raw html files. If False, will not scrape if files already found.
    pause : float or int
        The time to pause between requests to the NHL API. Defaults to 1 second
    marker : float or int
        The number of times to print progress. 10 will print every 10%; 20 every 5%.
    """
    import time
    games = sorted(list(games))
    marker_i = [len(games)//marker * i for i in range(marker)]
    marker_i[-1] = len(games) - 1
    marker_i_set = set(marker_i)
    for i in range(len(games)):
        game = games[i]
        newscrape = scrape_game.scrape_game(season, game, force_overwrite)
        if newscrape: #only sleep if had to scrape a new game
            time.sleep(pause)
        if i in marker_i_set:
            print('Done through', season, game, ' ~ ', round((marker_i.index(i)) * 100/marker), '%')
    print('Done scraping games in', season)


def scrape_season(season, startgame = None, endgame = None, force_overwrite = False, pause = 1):
    """
    Scrapes games for the specified season.

    Parameters
    -----------
    season : int
        The season of the game. 2007-08 would be 2007.
    startgame : int
        The game id at which scraping will start. For example, midway through a season, this can be the last game
        scraped.
        This can range from 20001 to 21230 for regular season, and 30111 to 30417 for playoffs.
        The preseason, all-star game, Olympics, and World Cup also have game IDs that can be provided.
    force_overwrite : bool
        If True, will overwrite previously raw html files. If False, will not scrape if files already found.
    pause : float or int
        The time to pause between requests to the NHL API. Defaults to 1 second
    """
    if season != 2012:
        games = [20000 + x for x in range(1, 1231)]
    else:
        games = [20000 + x for x in range(1, 721)]
    for round in range(1, 5):
        for series in range(1, 8//round + 1):
            for game in range(1, 8):
                games.append(int('30{0:d}{1:d}{2:d}'.format(round, series, game)))
    if startgame is not None:
        games = [g for g in games if g >= startgame]
    if endgame is not None:
        games = [g for g in games if g <= endgame]
    scrape_games(season, games, force_overwrite, pause, 10)

def get_team_pbplog_filename(season, team):
    return '{0:s}/Team logs/{2:s}_pbp.feather'.format(scrapenhl_globals.SAVE_FOLDER, season, team)

def get_team_toilog_filename(season, team):
    return '{0:s}/Team logs/{2:s}_toi.feather'.format(scrapenhl_globals.SAVE_FOLDER, season, team)

def update_teamlogs(season, force_overwrite = False):

    teams = {x for x in \
        scrapenhl_globals.BASIC_GAMELOG.query('Season == {0:d}'.format(season))['Home'].drop_duplicates()} | \
            {x for x in \
             scrapenhl_globals.BASIC_GAMELOG.query('Season == {0:d}'.format(season))['Away'].drop_duplicates()}
    temp = scrapenhl_globals.BASIC_GAMELOG
    ### List files in correct format
    import os
    allfiles = os.listdir(scrapenhl_globals.get_season_folder(season))

    pbpfiles = {int(x[:5]): x for x in allfiles if x[-12:] == '_parsed.zlib'}
    toifiles = {int(x[:5]): x for x in allfiles if x[-19:] == '_shifts_parsed.zlib'}

    import feather
    import pandas as pd
    import os.path

    for team in teams:
        teamgames = scrapenhl_globals.BASIC_GAMELOG.query('Season == {0:d} & (Home == "{1:s}" | Away == "{1:s}")'.format(
            season, team))['Game']
        current_pbp = None
        games_already_done = set()
        if os.path.exists(get_team_pbplog_filename(season, team)):
            current_pbp = feather.read_dataframe(get_team_pbplog_filename(season, team))
            games_already_done = {x for x in current_pbp.Game}

        dflist = []
        if not force_overwrite and current_pbp is not None:
            dflist.append(current_pbp)
            teamgames = {g for g in teamgames if g not in games_already_done}
        ### TODO do I need to flip any columns?
        #if force_overwrite:
        for game in teamgames:
            try:
                df = pd.read_hdf(scrape_game.get_parsed_save_filename(season, game))
                df = df.assign(Game = game)
                if df is not None:
                    dflist.append(df)
            except FileNotFoundError:
                pass
        if len(dflist) > 0:
            new_pbp = pd.concat(dflist)
            for col in new_pbp.columns:
                if new_pbp[col].dtype == 'object':
                    new_pbp[col] = new_pbp[col].astype(str)
            feather.write_dataframe(new_pbp, get_team_pbplog_filename(season, team))

        current_toi = None
        games_already_done = set()
        if os.path.exists(get_team_toilog_filename(season, team)):
            current_toi = feather.read_dataframe(get_team_toilog_filename(season, team))
            games_already_done = {x for x in current_toi.Game}
        ### TODO issues here
        dflist = []
        if not force_overwrite:
            dflist.append(current_toi)
            teamgames = {g for g in teamgames if g not in games_already_done}

        #if force_overwrite:
        for game in teamgames:
            try:
                df = pd.read_hdf(scrape_game.get_parsed_shifts_save_filename(season, game))
                df = df.assign(Game = game)
                cols_to_replace = {col for col in df.columns if str.isdigit(col[-1]) if col[:3] != team}
                df.rename(columns = {col: 'Opp' + col[-1] for col in cols_to_replace}, inplace = True)
                if df is not None:
                    dflist.append(df)
            except FileNotFoundError:
                pass

        import pandas as pd
        if len(dflist) > 0:
            new_toi = pd.concat(dflist)
            for col in new_toi.columns:
                if new_toi[col].dtype == 'object':
                    new_toi[col] = new_toi[col].astype(str)
            feather.write_dataframe(new_toi, get_team_toilog_filename(season, team))

def update_playerlog():
    pass

def get_season_schedule_url(season):
    return 'https://statsapi.web.nhl.com/api/v1/schedule?startDate={0:d}-09-01&endDate={1:d}-06-25'.format(season,
                                                                                                           season + 1)

def parse_games(season, games, force_overwrite = False, marker = 10):
    """
    Parses the specified games.

    Parameters
    -----------
    season : int
        The season of the game. 2007-08 would be 2007.
    games : iterable of ints (e.g. list)
        The game id. This can range from 20001 to 21230 for regular season, and 30111 to 30417 for playoffs.
        The preseason, all-star game, Olympics, and World Cup also have game IDs that can be provided.
    force_overwrite : bool
        If True, will overwrite previously parsed files. If False, will not parise if files already found.
    marker : float or int
        The number of times to print progress. 10 will print every 10%; 20 every 5%.
    """
    games = sorted(list(games))
    marker_i = [len(games) // marker * i for i in range(marker)]
    marker_i[-1] = len(games) - 1
    marker_i_set = set(marker_i)
    for i in range(len(games)):
        game = games[i]
        scrape_game.parse_game(season, game, force_overwrite)
        if i in marker_i_set:
            print('Done through', season, game, ' ~ ', round((marker_i.index(i)) * 100 / marker), '%')
    print('Done parsing games in', season)

def autoupdate(season = scrapenhl_globals.MAX_SEASON):
    """
    Scrapes unscraped games for the specified season.

    This is a convenience function that finds the highest completed game in a year and scrapes up to that point only.
    This reduces unnecessary requests for unplayed games.

    Parameters
    -----------
    season : int
        The season of the game. 2007-08 would be 2007.
    """
    import urllib.request
    url = get_season_schedule_url(season)
    with urllib.request.urlopen(url) as reader:
        page = reader.read().decode('latin-1')

    import json
    jsonpage = json.loads(page)
    completed_games = set()

    for gameday in jsonpage['dates']:
        for game in gameday['games']:
            if game['status']['abstractGameState'] == 'Final':
                completed_games.add(int(str(game['gamePk'])[-5:]))

    scrape_games(season, completed_games)
    parse_games(season, completed_games)

def reparse_season(season = scrapenhl_globals.MAX_SEASON):
    """
    Re-parses entire season.
    :param season: int
        The season of the game. 2007-08 would be 2007.
    :return:
    """
    import urllib.request
    url = get_season_schedule_url(season)
    with urllib.request.urlopen(url) as reader:
        page = reader.read().decode('latin-1')

    import json
    jsonpage = json.loads(page)
    completed_games = set()

    for gameday in jsonpage['dates']:
        for game in gameday['games']:
            if game['status']['abstractGameState'] == 'Final':
                completed_games.add(int(str(game['gamePk'])[-5:]))

    parse_games(season, completed_games, True)

reparse_season(2016)
update_teamlogs(2016)

#from urllib.error import URLError
#for season in range(2016, 2017):
#    while True:
#        try:
#            autoupdate(season)
#            break
#        except URLError as e:
#            print(season, e, e.args)
#scrapenhl_globals.write_correct_playername_file()