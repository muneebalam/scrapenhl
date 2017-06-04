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
    print('Done scraping games')


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
    return '{0:s}/{1:d}/{2:s}_pbp.feather'.format(scrapenhl_globals.SAVE_FOLDER, season, team)

def get_team_toilog_filename(season, team):
    return '{0:s}/{1:d}/{2:s}_toi.feather'.format(scrapenhl_globals.SAVE_FOLDER, season, team)

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
                df = df.assign(Game = game)
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
                oppnamecolumns = [x for x in df.columns if x[:3] != team]
                oppname = x[0][:3]
                df.rename(columns={'{0:s}{1:d}'.format(oppname, i): 'Opp{0:d}'.format(i) for i in range(1, 7)},
                          inplace=True)
                df = df.assign(Game = game)
                dflist.append(df)

        import pandas as pd
        new_toi = pd.concat(dflist)
        feather.write_dataframe(new_toi, get_team_toilog_filename(season, team))

def update_playerlog():
    pass

def get_season_schedule_url(season):
    return 'https://statsapi.web.nhl.com/api/v1/schedule?startDate={0:d}-09-01&endDate={1:d}-06-25'.format(season,
                                                                                                           season + 1)

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

    for gameday in page['dates']:
        for game in gameday['games']:
            if game['status']['statusCode'] == 'Final':
                completed_games.add(game['gamePk'])

    scrape_games(season, completed_games)


for season in range(2007, 2017):
    scrape_full_season(season)