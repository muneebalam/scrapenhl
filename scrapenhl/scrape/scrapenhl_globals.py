"""
File and folder paths, and other variables needed by all modules in this package.
"""

SAVE_FOLDER = "/Users/muneebalam/PycharmProjects/scrapenhl/scrapenhl/scrape/"
PLAYER_ID_FILE = "{0:s}playerids.feather".format(SAVE_FOLDER)
BASIC_GAMELOG_FILE = "{0:s}quickgamelog.feather".format(SAVE_FOLDER)
MAX_SEASON = 2016

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

def get_season_folder(season):
    """
    Returns season folder in SAVE_FOLDER

    Parameters
    -----------
    season : int
        The season of the game. 2007-08 would be 2007.

    Returns
    -------
    str
        The folder path
    """
    return '{0:s}{1:d}/'.format(SAVE_FOLDER, season)

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

    Parameters
    -----------
    df : Pandas dataframe
        The player ID dataframe
    """
    import feather
    df.sort_values(by = "ID", inplace = True)
    feather.write_dataframe(df, PLAYER_ID_FILE)

def get_quick_gamelog_file():
    """
    Returns the game log file

    This file contains basic information on games: season, game, date, venue, and home and road names, scores, and
    coaches. A new blank file is created if necessary.

    Returns
    --------
    Pandas df
        The game log dataframe
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
    Writes the game log dataframe to disk in feather format

    Parameters
    -----------
    df : Pandas dataframe
        The basic game log dataframe
    """
    import feather
    df.sort_values(by = ['Season', 'Game'], inplace = True)
    feather.write_dataframe(df, BASIC_GAMELOG_FILE)


PLAYER_IDS = get_player_id_file()
BASIC_GAMELOG = get_quick_gamelog_file()

