import scrapenhl_globals
import scrape_season
import scrape_game

def get_player_cf(player, seasons=None):

    player_gamelog = scrapenhl_globals.get_player_gamelog()

    #Turn seasons into a set of acceptable values
    if seasons is None:
        seasons = [x for x in range(scrapenhl_globals.MAX_SEASON - 3, scrapenhl_globals.MAX_SEASON)]
    if isinstance(seasons, int):
        seasons = {seasons}
    else:
        seasons = set(seasons)

    #Turn player name into ID if needed


def read_team_pbp(season, team, types=None, strengths=None):
    """
    Returns PBP events for all players in this season

    Parameters
    -----------
    season : ints
        The season of the game. 2007-08 would be 2007.
    team: str
        The team to consider.
    strength: str
        The strength to filter to
    actors: str or iterable of str
        The player names
    recipients: str or iterable of str
        The recipient names
    on_ice: str or iterable of str
        players on ice
    return_type: str
        The return type. Can return pandas dataframe rows with 'rows' or full dataframe with 'df'
    """
    df = scrape_season.get_team_pbplog(season, team)

    ### Filter strength

    ### Filter actor

    ### Filter recipient

    ### Filter on_ice

    ### Move this to the get_team_pbplog method

    ### Return type
    if return_type == 'rows':
        return df.iterrows()
    elif return_type == 'df':
        return df
    else:
        print('Invalid return type specification for read_team_toi; use "rows" or "df"')
        return df

def read_team_toi(season, team, strengths=None, return_type='rows'):
    """
    Returns TOI totals for all players in this season on this team

    Parameters
    -----------
    season : ints
        The season of the game. 2007-08 would be 2007.
    team: str
        The team to consider.
    strength: str
        The strength to filter to
    return_type: str
        The return type. Can return pandas dataframe rows with 'rows' or full dataframe with 'df'
    """
    df = scrape_season.get_team_toilog(season, team)

    ### Filter strength

    ### Wide to long on players

    ### Join correct names

    ### Return type
    if return_type == 'rows':
        return df.iterrows()
    elif return_type == 'df':
        return df
    else:
        print('Invalid return type specification for read_team_toi; use "rows" or "df"')
        return df

def get_toi():
    """
    Returns TOI totals for all players in this season

    Parameters
    -----------
    seasons : iterable of ints
        The seasons of the game. 2007-08 would be 2007. Can also just be an int
    teams: iterable of str
        The teams to consider. Can also be a single str.
    """
    import feather
    import pandas as pd
    import os.path

    basic_gamelog = scrapenhl_globals.get_quick_gamelog_file()

    alltoi = {}

    for season in seasons:
        teams = {x for x in \
                 basic_gamelog.query('Season == {0:d}'.format(season))['Home'].drop_duplicates()} | \
                {x for x in \
                 basic_gamelog.query('Season == {0:d}'.format(season))['Away'].drop_duplicates()}

        for team in teams:
            df = scrape_season.get_team_toilog(season, team)
            ### Melt this to be long on player IDs
            ### Group by
