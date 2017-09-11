"""
File and folder paths, and other variables needed by all modules in this package.
"""

import os
import os.path

SAVE_FOLDER = os.path.join(os.getcwd(), "data")
PLAYER_ID_FILE = os.path.join(SAVE_FOLDER, 'reference', 'playerids.feather')
TEAM_ID_FILE = os.path.join(SAVE_FOLDER, 'reference', 'teamids.feather')
BASIC_GAMELOG_FILE = os.path.join(SAVE_FOLDER, 'reference', 'quickgamelog.feather')
PLAYER_NAMES_FILE = os.path.join(SAVE_FOLDER, 'reference', 'playerids_names.feather')

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
    folder = os.path.join(SAVE_FOLDER, str(season))
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
    return os.path.join(SAVE_FOLDER, str(season))

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
        .groupby('ID').iloc[0].reset_index()
    feather.write_dataframe(highn, PLAYER_NAMES_FILE)

def get_preferred_player_names():
    try:
        return feather.read_dataframe(PLAYER_NAMES_FILE)
    except Exception as e:
        write_preferred_player_names_file()
        return feather.read_dataframe(PLAYER_NAMES_FILE)

def player_name_to_id(pname, team_helper=None):
    """
    Matches given player name to ID. If multiple matches, prints warning and continues with most common player.

    This method first looks for exact matches. If none are found, it looks for names containing given name.
    If there are still no matches, it prints a warning and takes the closest fuzzy match.

    Parameters
    -----------
    pname : str
        The player name. Case sensitive.
    team_helper: iterable of str, or str, or None
        Can be used to help break exact matches

    Returns
    --------
    id: int
        The ID number of the player
    """
    df = get_player_id_file()
    df = df[['Name', 'ID', 'Team', 'Count']].groupby(['Name', 'ID', 'Team']).sum() \
        .reset_index().sort_values('Count', ascending=False)

    if team_helper is not None:
        if isinstance(team_helper, str):
            team_helper = {team_helper}

    ### Exact match
    exact = df[df.Name == pname]
    if len(exact.ID.unique()) == 1:
        return exact.ID.iloc[0]
    elif len(exact.ID.unique()) > 1:
        if team_helper is None:
            print('Found multiple matches for', pname)
            print(exact)
            print('Selecting', exact.iloc[0, :])
            return exact.ID.iloc[0]
        else:
            exact_team = exact[exact.Team.isin(team_helper)]
            if len(exact_team) == 1:
                return exact_team.ID.iloc[0]
            elif len(exact_team) > 1:
                print('Found multiple matches for', pname)
                print(exact_team)
                print('Selecting', exact_team.iloc[0,:])
                return exact_team.ID.iloc[0]

    ### Contains match
    contains = df[df.Name.str.contains(pname)]
    if len(contains.ID.unique()) == 1:
        return contains.ID.iloc[0]
    elif len(contains.ID.unique()) > 1:
        if team_helper is None:
            print('Found multiple matches for', pname)
            print(contains)
            print('Selecting', contains.iloc[0, :])
            return contains.ID.iloc[0]
        else:
            contains_team = contains[contains.Team.isin(team_helper)]
            if len(contains_team) == 1:
                return contains_team.ID.iloc[0]
            elif len(contains_team) > 1:
                print('Found multiple matches for', pname)
                print(contains_team)
                print('Selecting', contains_team.iloc[0,:])
                return contains_team['ID'].iloc[0]

    ### Fuzzy match
    ### TODO using fuzzywuzzy
    print('Match not found. Fuzzy matching to be implemented later')
    return None



