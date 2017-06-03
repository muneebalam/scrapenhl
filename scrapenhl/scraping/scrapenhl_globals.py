"""
File and folder paths, and other variables needed by all modules in this package.
"""

SAVE_FOLDER = "/Users/muneebalam/PycharmProjects/scrapenhl/scrapenhl/scraping/"
from os import mkdir
from os.path import exists

for season in range(2007, 2017):
    folder = '{0:s}{1:d}/'.format(SAVE_FOLDER, season)
    if not exists(folder):
        mkdir(folder)