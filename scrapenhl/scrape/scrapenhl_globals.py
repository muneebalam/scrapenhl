"""
File and folder paths, and other variables needed by all modules in this package.
"""

SAVE_FOLDER = "../data/"
PLAYER_ID_FILE = "{0:s}reference/playerids.feather".format(SAVE_FOLDER)
TEAM_ID_FILE = "{0:s}reference/teamids.feather".format(SAVE_FOLDER)
BASIC_GAMELOG_FILE = "{0:s}reference/quickgamelog.feather".format(SAVE_FOLDER)
PLAYER_NAMES_FILE = "{0:s}reference/playerids_names.feather".format(SAVE_FOLDER)

import datetime
MAX_SEASON = datetime.datetime.now().year - 1
if datetime.datetime.now().month >= 9:
    MAX_SEASON += 1
import feather
import pandas as pd
import os.path

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
    if not os.path.exists(PLAYER_ID_FILE):
        print('Creating blank player ID file for future use')
        df = pd.DataFrame({'ID': [], 'Name': [], 'Team': [], 'Pos': [], '#': [], 'Hand': [], 'Count': []})
        #write_player_id_file()
        return df
    else:
        return feather.read_dataframe(PLAYER_ID_FILE)

def write_player_id_file(df):
    """
    Writes the player id file to disk in feather format

    This file maps player IDs to names, positions, handedness, teams, and jersey numbers. Using IDs is a way to avoid
    having to correct the numerous spelling inconsistencies in the data.
    """
    df.sort_values(by = "ID", inplace = True)
    df['#'] = df['#'].astype(int)
    df['ID'] = df['ID'].astype(str)
    df['Name'] = df['Name'].astype(str)
    df['Pos'] = df['Pos'].astype(str)
    df['Team'] = df['Team'].astype(str)
    df['Hand'] = df['Hand'].astype(str)
    df['Count'] = df['Count'].astype(int)
    feather.write_dataframe(df, PLAYER_ID_FILE)

def get_team_id_file():
    """
    Returns the team id file

    This file maps team IDs to names and abbreviations.

    If the team ID file is not found, a blank one is created

    Returns
    --------
    Pandas df
        The team id dataframe
    """
    if not os.path.exists(TEAM_ID_FILE):
        print('Creating blank team ID file for future use')
        TEAM_IDS = pd.DataFrame({'ID': [], 'Name': [], 'Abbreviation': []})
        # write_player_id_file()
        return TEAM_IDS
    else:
        return feather.read_dataframe(TEAM_ID_FILE)

def write_team_id_file(df):
    """
    Writes the team id file to disk in feather format

    This file maps team IDs to names and abbreviations.
    """
    df.sort_values(by="ID", inplace=True)
    feather.write_dataframe(df, TEAM_ID_FILE)

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
    if not os.path.exists(BASIC_GAMELOG_FILE):
        print('Creating blank game log file for future use')
        df = pd.DataFrame({'Season': [], 'Game': [], 'Datetime': [], 'Venue': [],
                           'Home': [], 'HomeCoach': [], 'HomeScore': [],
                           'Away': [], 'AwayCoach': [], 'AwayScore': []})
        return df
    else:
        return feather.read_dataframe(BASIC_GAMELOG_FILE)

def write_quick_gamelog_file(df):
    """
    Writes the game log dataframe (in global namespace) to disk in feather format
    """
    df.sort_values(by = ['Season', 'Game'], inplace = True)
    df = df.drop_duplicates()
    feather.write_dataframe(df, BASIC_GAMELOG_FILE)

def write_preferred_player_names_file():
    """
    Uses player_ids file, assigns most common spelling of name to each ID
    """
    df = get_player_id_file()
    highn = df[['ID', 'Name', 'Count']].groupby(['ID', 'Name']).sum() \
        .reset_index() \
        .sort_values(by='Count', ascending=False) \
        .groupby('ID').first().reset_index()
    feather.write_dataframe(highn, PLAYER_NAMES_FILE)



