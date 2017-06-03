"""
File and folder paths, and other variables needed by all modules in this package.
"""

SAVE_FOLDER = "/Users/muneebalam/PycharmProjects/scrapenhl/scrapenhl/scraping/"
PLAYER_ID_FILE = "{0:s}playerids.feather".format(SAVE_FOLDER)
BASIC_GAMELOG_FILE = "{0:s}quickgamelog.feather".format(SAVE_FOLDER)

def create_season_folder(season):
    """
    Creates a season folder in SAVE_FOLDER

    Parameters
    -----------
    season : int
        The season of the game. 2007-08 would be 2007.
    """
    import os
    folder = '{0:s}{1:d}/'.format(SAVE_FOLDER, season)
    os.mkdir(folder)

def get_player_id_file():
    """
    Returns the player id file

    This file maps player IDs to names, positions, handedness, teams, and jersey numbers. Using IDs is a way to avoid
    having to correct the numerous spelling inconsistencies in the data.

    If the player ID file is not found, a blank one is created

    Returns
    --------
    Pandas df
        The player id dataframe
    """
    import feather
    import os.path
    if not os.path.exists(PLAYER_ID_FILE):
        print('Creating blank player ID file for future use')
        import pandas as pd
        df = pd.DataFrame({'ID': [], 'Name': [], 'Team': [], 'Pos': [], '#': [], 'Hand': []})
        write_player_id_file(df)
        return df
    else:
        return feather.read_dataframe(PLAYER_ID_FILE)

def write_player_id_file(df):
    """
    Writes the player id file to disk in feather format

    This file maps player IDs to names, positions, handedness, teams, and jersey numbers. Using IDs is a way to avoid
    having to correct the numerous spelling inconsistencies in the data.
    """
    import feather
    df.sort_values(by = "ID", inplace = True)
    feather.write_dataframe(df, PLAYER_ID_FILE)

def get_quick_gamelog_file():
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
    import feather
    import os.path
    if not os.path.exists(BASIC_GAMELOG_FILE):
        print('Creating blank game log file for future use')
        import pandas as pd
        df = pd.DataFrame({'Season': [], 'Game': [], 'Datetime': [], 'Venue': [],
                           'Home': [], 'HomeCoach': [], 'HomeScore': [],
                           'Away': [], 'AwayCoach': [], 'AwayScore': []})
        write_quick_gamelog_file(df)
        return df
    else:
        return feather.read_dataframe(BASIC_GAMELOG_FILE)

def write_quick_gamelog_file(df):
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
    import feather
    df.sort_values(by = ['Season', 'Game'], inplace = True)
    feather.write_dataframe(df, BASIC_GAMELOG_FILE)


PLAYER_IDS = get_player_id_file()
BASIC_GAMELOG = get_quick_gamelog_file()

