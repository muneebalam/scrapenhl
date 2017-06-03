import scrapenhl_globals

def get_url(season, game):
    """
    Returns the NHL API url to scrape.

    Parameters
    -----------
    season : int
        The season of the game. 2007-08 would be 2007.
    game : int
        The game id. This can range from 20001 to 21230 for regular season, and 30111 to 30417 for playoffs.
        The preseason, all-star game, Olympics, and World Cup also have game IDs that can be provided.
    Returns
    --------
    str
        URL to scrape, http://statsapi.web.nhl.com/api/v1/game/[season]0[game]/feed/live
    """
    return 'http://statsapi.web.nhl.com/api/v1/game/{0:d}0{1:d}/feed/live'.format(season, game)

def get_json_save_filename(season, game):
    """
    Returns the algorithm-determined save file name of the json accessed online.

    Parameters
    -----------
    season : int
        The season of the game. 2007-08 would be 2007.
    game : int
        The game id. This can range from 20001 to 21230 for regular season, and 30111 to 30417 for playoffs.
        The preseason, all-star game, Olympics, and World Cup also have game IDs that can be provided.
    Returns
    --------
    str
        file name, SAVE_FOLDER/Season/Game.zlib
    """
    return '{0:s}/{1:d}/{2:d}.zlib'.format(scrapenhl_globals.SAVE_FOLDER, season, game)

def get_parsed_save_filename(season, game):
    """
    Returns the algorithm-determined save file name of the parsed pbp file.

    Parameters
    -----------
    season : int
        The season of the game. 2007-08 would be 2007.
    game : int
        The game id. This can range from 20001 to 21230 for regular season, and 30111 to 30417 for playoffs.
        The preseason, all-star game, Olympics, and World Cup also have game IDs that can be provided.
    Returns
    --------
    str
        file name, SAVE_FOLDER/Season/Game_parsed.zlib
    """
    return '{0:s}/{1:d}/{2:d}_parsed.zlib'.format(scrapenhl_globals.SAVE_FOLDER, season, game)

def scrape_game(season, game, force_overwrite = False):
    """
    Scrapes and saves game files in compressed (zlib) format

    Parameters
    -----------
    season : int
        The season of the game. 2007-08 would be 2007.
    game : int
        The game id. This can range from 20001 to 21230 for regular season, and 30111 to 30417 for playoffs.
        The preseason, all-star game, Olympics, and World Cup also have game IDs that can be provided.
    force_overwrite : bool
        If True, will overwrite previously raw html files. If False, will not scrape if files already found.
    """
    import os.path
    url = get_url(season, game)
    filename = get_json_save_filename(season, game)
    if force_overwrite or not os.path.exists(filename):
        import urllib.request
        try:
            with urllib.request.urlopen(url) as reader:
                page = reader.read()
        except Exception as e:
            if game < 30111:
                print('Error reading api url for', season, game, e, e.args)
                page = bytes('', encoding = 'latin-1')
        if game < 30111:
            import zlib
            page2 = zlib.compress(page, level=9)
            w = open(filename, 'wb')
            w.write(page2)
            w.close()

def parse_game(season, game, force_overwrite = False):
    """
    Reads this game's zlib file from disk and parses into a friendlier format, then saves again to disk in zlib.

    This method also updates the global player id and game log files, and writes any updates to disk.

    Parameters
    -----------
    season : int
        The season of the game. 2007-08 would be 2007.
    game : int
        The game id. This can range from 20001 to 21230 for regular season, and 30111 to 30417 for playoffs.
        The preseason, all-star game, Olympics, and World Cup also have game IDs that can be provided.
    force_overwrite : bool
        If True, will overwrite previously raw html files. If False, will not scrape if files already found.
    """
    import os.path
    import zlib
    import json
    filename = get_parsed_save_filename(season, game)
    if (force_overwrite or not os.path.exists(filename)):
        r = open(get_json_save_filename(season, game), 'rb')
        page = r.read()
        r.close()

        page = zlib.decompress(page)
        data = json.loads(page.decode('latin-1'))

        teamdata = data['liveData']['boxscore']['teams']

        update_player_ids_from_json(teamdata)
        update_quick_gamelog_from_json(data)

        events = read_events_from_json(data['liveData']['plays']['allPlays'])

def update_player_ids_from_json(teamdata):
    """
    Creates a data frame of player data from current game's json[liveData][boxscore] to update global PLAYER_IDS.

    This method reads player ids, names, handedness, team, position, and number, and full joins to PLAYER_IDS.
    If there are any changes to PLAYER_IDS, the dataframe gets written to disk again.

    Parameters
    -----------
    teamdata : dict
        A json dict that is the result of api_page['liveData']['boxscore']['teams']
    """
    teams = {'R': [teamdata['away']['team']['abbreviation'],
             teamdata['away']['team']['name']],
             'H': [teamdata['home']['team']['abbreviation'],
                 teamdata['home']['team']['name']]}

    awayplayers = teamdata['away']['players']
    homeplayers = teamdata['home']['players']

    numplayers = len(awayplayers) + len(homeplayers)
    ids = ['' for i in range(numplayers)]
    names = ['' for i in range(numplayers)]
    teams = ['' for i in range(numplayers)]
    positions = ['' for i in range(numplayers)]
    nums = [-1 for i in range(numplayers)]
    handedness = ['' for i in range(numplayers)]

    for pid, pdata in awayplayers.items():
        idnum = pid[2:]
        name = pdata['person']['fullName']
        hand = pdata['person']['shootsCatches']
        num = pdata['jerseyNumber']
        pos = pdata['position']['code']

        ids.append(idnum)
        names.append(name)
        teams.append(teams['R'][0])
        positions.append(pos)
        nums.append(num)
        handedness.append(hand)

    for pid, pdata in homeplayers.items():
        idnum = pid[2:]
        name = pdata['person']['fullName']
        hand = pdata['person']['shootsCatches']
        num = pdata['jerseyNumber']
        pos = pdata['position']['code']

        ids.append(idnum)
        names.append(name)
        teams.append(teams['H'][0])
        positions.append(pos)
        nums.append(num)
        handedness.append(hand)

    import pandas as pd
    gamedf = pd.DataFrame({'ID': ids,
                           'Name': names,
                           'Team': teams,
                           'Pos': positions,
                           '#': nums,
                           'Hand': handedness})
    ### Find change in length and join
    oldlength = len(scrapenhl_globals.PLAYER_IDS)
    scrapenhl_globals.PLAYER_IDS = scrapenhl_globals.PLAYER_IDS.merge(
        gamedf, how = 'outer', on = gamedf.columns)
    newlength = len(scrapenhl_globals.PLAYER_IDS)

    ### Write to disk again immediately in case an error later crashes script
    ### This is in feather format for quick read/write
    if newlength > oldlength:
        scrapenhl_globals.PLAYER_IDS.write_player_id_file(scrapenhl_globals.PLAYER_IDS)

def update_quick_gamelog_from_json(data):
    """
    Creates a data frame of basic game data from current game's json to update global BASIC_GAMELOG.

    This method reads the season, game, date and time, venue, and team names, coaches, anc scores, joining to
    BASIC_GAMELOG.
    If there are any changes to BASIC_GAMELOG, the dataframe gets written to disk again.

    Parameters
    -----------
    data : dict
        The full json dict from the api_page
    """
    season = int(str(data['gameData']['game']['pk'])[:4])
    game = int(str(data['gameData']['game']['pk'])[4:])
    datetime = data['gameData']['datetime']['dateTime']
    venue = data['gameData']['venue']['name']
    hname = data['gameData']['teams']['home']['triCode']
    rname = data['gameData']['teams']['away']['triCode']
    hcoach = data['liveData']['boxscore']['teams']['home']['coaches'][0]['person']['fullName']
    rcoach = data['liveData']['boxscore']['teams']['away']['coaches'][0]['person']['fullName']
    hscore = data['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['goals']
    rscore = data['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['goals']

    import pandas as pd
    gamedf = pd.DataFrame({'Season': [season], 'Game': [game], 'Datetime': [datetime], 'Venue': [venue],
                           'Home': [hname], 'HomeCoach': [hcoach], 'HomeScore': [hscore],
                           'Away': [rname], 'AwayCoach': [rcoach], 'AwayScore': [rscore]})
    oldlength = len(scrapenhl_globals.BASIC_GAMELOG)
    scrapenhl_globals.BASIC_GAMELOG = scrapenhl_globals.BASIC_GAMELOG.merge(
        gamedf, how='outer', on = gamedf.columns)
    newlength = len(scrapenhl_globals.BASIC_GAMELOG)
    if newlength > oldlength:
        scrapenhl_globals.write_player_id_file(scrapenhl_globals.BASIC_GAMELOG)

def read_events_from_json(pbp):
    """
    Returns the NHL API url to scrape.

    Parameters
    -----------
    season : int
        The season of the game. 2007-08 would be 2007.
    game : int
        The game id. This can range from 20001 to 21230 for regular season, and 30111 to 30417 for playoffs.
        The preseason, all-star game, Olympics, and World Cup also have game IDs that can be provided.
    Returns
    --------
    pandas df
        Dataframe of the game's play by play data
    """
    pass

#scrape_game(2007, 20001)