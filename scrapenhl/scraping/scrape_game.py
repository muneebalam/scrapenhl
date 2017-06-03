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
    return '{0:s}/{1:d}/{2:d}.zlib'.format(scrapenhl_globals.SAVE_FOLDER, season, game)

def get_parsed_save_filename(season, game):
    pass

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
                page = bytes('')
        if game < 30111:
            import zlib
            page2 = zlib.compress(page, level=9)
            w = open(filename, 'wb')
            w.write(page2)
            w.close()

def parse_game(season, game, force_overwrite = False):
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

        awayplayers = data['boxscore']['teams']['away']['players']
        homeplayers = data['boxscore']['teams']['home']['players']

#scrape_game(2007, 20001)