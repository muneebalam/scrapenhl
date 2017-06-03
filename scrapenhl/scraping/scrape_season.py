import scrape_game

def scrape_season(season):
    pass

def scrape_full_season(season, pause = 1):
    import time
    if season == 2012:
        games = [20000 + x for x in range(1, 1231)]
    else:
        games = [20000 + x for x in range(1, 721)]
    for round in range(1, 5):
        for series in range(1, 8//round + 1):
            for game in range(1, 8):
                games.append(int('30{0:d}{1:d}{2:d}'.format(round, series, game)))
    games = games + [30]
    for game in games:
        scrape_game.scrape_game(season, game, True)
        time.sleep(1)
        if game % 100 == 0:
            print('Done through', season, game)

scrape_full_season(2007)