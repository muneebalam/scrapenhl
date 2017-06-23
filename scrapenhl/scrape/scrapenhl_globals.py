"""
File and folder paths, and other variables needed by all modules in this package.
"""

SAVE_FOLDER = "/Users/muneebalam/PycharmProjects/scrapenhl/scrapenhl/scrape/"
PLAYER_ID_FILE = "{0:s}playerids.feather".format(SAVE_FOLDER)
CORRECTED_PLAYERNAMES_FILE = "{0:s}playernames.csv".format(SAVE_FOLDER)
TEAM_ID_FILE = "{0:s}teamids.feather".format(SAVE_FOLDER)
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
        PLAYER_IDS = pd.DataFrame({'ID': [], 'Name': [], 'Team': [], 'Pos': [], '#': [], 'Hand': []})
        #write_player_id_file()
        return PLAYER_IDS
    else:
        return feather.read_dataframe(PLAYER_ID_FILE)

def write_player_id_file():
    """
    Writes the player id file to disk in feather format

    This file maps player IDs to names, positions, handedness, teams, and jersey numbers. Using IDs is a way to avoid
    having to correct the numerous spelling inconsistencies in the data.
    """
    import feather
    try:
        PLAYER_IDS.sort_values(by = "ID", inplace = True)
    except UnboundLocalError:
        PLAYER_IDS = get_player_id_file()
        PLAYER_IDS.sort_values(by="ID", inplace=True)
    PLAYER_IDS['#'] = PLAYER_IDS['#'].astype(int)
    PLAYER_IDS['ID'] = PLAYER_IDS['ID'].astype(str)
    PLAYER_IDS['Name'] = PLAYER_IDS['Name'].astype(str)
    PLAYER_IDS['Pos'] = PLAYER_IDS['Pos'].astype(str)
    PLAYER_IDS['Team'] = PLAYER_IDS['Team'].astype(str)
    PLAYER_IDS['Hand'] = PLAYER_IDS['Hand'].astype(str)
    PLAYER_IDS = PLAYER_IDS.drop_duplicates()
    feather.write_dataframe(PLAYER_IDS, PLAYER_ID_FILE)

def write_correct_playername_file():
    import pandas as pd
    import os.path

    # Find duplicate names in player id df
    counts = PLAYER_IDS.drop_duplicates(subset = ['ID', 'Name'])
    counts = counts.groupby('ID').count()

    singles = counts.query('Name == 1')
    singles.reset_index(inplace=True)
    singles.drop({'Name'}, axis=1, inplace=True)

    dupnames = dupnames.query('Name >= 2')
    dupnames.reset_index(inplace = True)
    dupnames.drop({'Name'}, axis = 1, inplace = True)

    if len(dupnames.index) == 0:
        PLAYER_IDS[['ID', 'Name']].to_csv(CORRECTED_PLAYERNAMES_FILE, index = False, encoding = 'latin-1')

    # Filter to those not in the corrected playernames file.
    if os.path.exists(CORRECTED_PLAYERNAMES_FILE):
        correct_names = pd.read_csv(CORRECTED_PLAYERNAMES_FILE)
        # Identify what values are in TableB and not in TableA
        key_diff = set(dupnames.ID).difference(correct_names.Key)
        where_diff = dupnames.ID.isin(key_diff)

        dupnames = dupnames[where_diff]
        if len(dupnames.index) == 0:
            fulldf = pd.concat([correct_names, PLAYER_IDS[['ID', 'Name']]]).drop_duplicates()
            fulldf.to_csv(CORRECTED_PLAYERNAMES_FILE, index=False, encoding='latin-1')
    else:
        correct_names = singles.merge(PLAYER_IDS[['ID', 'Name']], how = 'inner', on = 'ID')

    # Ask user to resolve remaining cases
    ids = [x for x in dupnames.ID]
    for i in range(len(ids)):
        temp = PLAYER_IDS.query('ID == "{0:s}"'.format(ids[i]))
        print(temp)
        preferred = input("Enter the row number (1 to {0:d}) of the preferred name\t".format(len(temp.index)))
        correct_names = pd.concat([correct_names, temp.iloc[preferred, :]])

    # Write uniques of this df, player id singles, and player_ids to file
    ### TODO also remake this method to work more intelligently

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
    import feather
    import os.path
    if not os.path.exists(TEAM_ID_FILE):
        print('Creating blank team ID file for future use')
        import pandas as pd
        TEAM_IDS = pd.DataFrame({'ID': [], 'Name': [], 'Abbreviation': []})
        # write_player_id_file()
        return TEAM_IDS
    else:
        return feather.read_dataframe(TEAM_ID_FILE)

def write_team_id_file():
    """
    Writes the team id file to disk in feather format

    This file maps team IDs to names and abbreviations.
    """
    import feather
    TEAM_IDS.sort_values(by="ID", inplace=True)
    TEAM_IDS.drop_duplicates(inplace = True)
    feather.write_dataframe(TEAM_IDS, TEAM_ID_FILE)

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
        write_quick_gamelog_file()
        return df
    else:
        return feather.read_dataframe(BASIC_GAMELOG_FILE)

def write_quick_gamelog_file():
    """
    Writes the game log dataframe (in global namespace) to disk in feather format
    """
    import feather
    try:
        BASIC_GAMELOG.sort_values(by = ['Season', 'Game'], inplace = True)
    except UnboundLocalError:
        BASIC_GAMELOG = get_quick_gamelog_file()
        BASIC_GAMELOG.sort_values(by=['Season', 'Game'], inplace=True)
    BASIC_GAMELOG = BASIC_GAMELOG.drop_duplicates()
    feather.write_dataframe(BASIC_GAMELOG, BASIC_GAMELOG_FILE)


PLAYER_IDS = get_player_id_file()
BASIC_GAMELOG = get_quick_gamelog_file()
TEAM_IDS = get_team_id_file()
#print(PLAYER_IDS.head())

