import scrape_game

def scrape_games(season, games, force_overwrite = False, pause = 1, marker = 10):
    import time
    games = sorted(list(games))
    marker_i = [len(games)//marker * i for i in range(marker)]
    marker_i[-1] = len(games) - 1
    marker_i_set = set(marker_i)
    for i in range(len(games)):
        game = games[i]
        scrape_game.scrape_game(season, game, force_overwrite)
        time.sleep(pause)
        if i in marker_i_set:
            print('Done through', season, game, ' ~ ', round((marker_i.index(i)) * 100/marker), '%')
    print('Done scraping games')


def scrape_full_season(season, startgame = 20001, force_overwrite = False, pause = 1):
    if season != 2012:
        games = [20000 + x for x in range(1, 1231)]
    else:
        games = [20000 + x for x in range(1, 721)]
    for round in range(1, 5):
        for series in range(1, 8//round + 1):
            for game in range(1, 8):
                games.append(int('30{0:d}{1:d}{2:d}'.format(round, series, game)))
    games = [g for g in games if g >= startgame]
    scrape_games(season, games, force_overwrite, pause, 10)

def update_playerlog():
    pass

for season in range(2010, 2017):
    scrape_full_season(2010)