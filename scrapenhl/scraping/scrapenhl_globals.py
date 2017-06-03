"""
File and folder paths, and other variables needed by all modules in this package.
"""

SAVE_FOLDER = "/Users/muneebalam/PycharmProjects/scrapenhl/scrapenhl/scraping/"
PLAYER_ID_FILE = "{0:s}playerids.feather".format(SAVE_FOLDER)

def create_season_folder(season):
    import os
    folder = '{0:s}{1:d}/'.format(SAVE_FOLDER, season)
    os.mkdir(folder)

def get_player_id_file():
    import feather
    import os.path
    if not os.path.exists(PLAYER_ID_FILE):
        print('Creating blank player ID file for future use')
        import pandas as pd
        df = pd.DataFrame({'ID': [], 'First': [], 'Last': [], 'Team': [], 'Pos': [], 'DOB': []})
        write_player_id_file(df)
        return df
    else:
        return feather.read_dataframe(PLAYER_ID_FILE)

def write_player_id_file(df):
    import feather
    df.sort_values(by = "ID", inplace = True)
    feather.write_dataframe(df, PLAYER_ID_FILE)


PLAYER_IDS = get_player_id_file()

