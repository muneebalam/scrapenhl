def get_url(season, game, reporttype = 'pbp'):
    """
    Returns the url to scrape.

    Parameters
    -----------
    season : int
        The season of the game. 2007-08 would be 2007.
    game : int
        The game id. This can range from 20001 to 21230 for regular season, and 30111 to 30417 for playoffs.
        The preseason, all-star game, Olympics, and World Cup also have game IDs that can be provided.
    reporttype : str
        Enter 'pbp' for play by play, 'toih' for home team ice time, and 'toiv' for road team ice time
    Returns
    --------
    str
        URL to scrape
    """
    return 'www.nhl.com/scores/htmlreports/{0:d}{1:d}/{2:s}0{3:d}.HTM'.format(
        season, season + 1, {'pbp': 'PL', 'toih': 'TH', 'toiv': 'TV'}[reporttype], game
    )

def get_pbp_url(season, game):
    return get_url(season, game, 'pbp')

def get_toih_url(season, game):
    return get_url(season, game, 'toih')

def get_toiv_url(season, game):
    return get_url(season, game, 'toiv')

def get_raw_save_file(season, game, force_overwrite, save_format):
    pass

def get_parsed_save_file(season, game, force_overwrite):
    pass

def save_page(url, force_overwrite = False, save_files = 'c'):
    urlparts = url.split('/')
    savefile = '{0:s}{1:s}/{2:s}'.format(SAVE_FOLDER, urlparts[3], urlparts[4][:-4],
                                         {'c': '.pkl', 'y': '.html', 'n': ''}[save_files])

    import urllib.request
    with urllib.request.urlopen(url)


def scrape_game(season, game, force_overwrite_raw = False, force_overwrite_parsed = False, save_files = 'c'):
    """
        Scrapes and saves game files

        Parameters
        -----------
        season : int
            The season of the game. 2007-08 would be 2007.
        game : int
            The game id. This can range from 20001 to 21230 for regular season, and 30111 to 30417 for playoffs.
            The preseason, all-star game, Olympics, and World Cup also have game IDs that can be provided.
        force_overwrite_raw : bool
            If True, will overwrite previously raw html files. If False, will not scrape if files already found.
        force_overwrite_prased : bool
            If True, will parse scraped files. If False, will not scrape or parse if files already found.
        save_files : str
            Enter 'y' to save html pages. Enter 'n' to not save html pages. Enter 'c' to save compressed (pickle) pages.
        """
    url = get_pbp_url(season, game)
    pbp = save_page(url, force_overwrite_raw, save_files)

    url = get_pbp_url(season, game)
    toih = save_page(url, force_overwrite_raw, save_files)

    url = get_pbp_url(season, game)
    toiv = save_page(url, force_overwrite_raw, save_files)