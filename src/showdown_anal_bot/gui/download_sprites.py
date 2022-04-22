import pathlib
import re
from os import get_terminal_size

from requests import get

"""
Downloads all sprites from pokemon showdown to avoid shennanigans
Update: This thing kinda sucks.
Update 2: It's not that bad.
"""


def main():
    FILE_PATH = pathlib.Path(__file__).parent.absolute()
    FILE_PATH /= 'sprites'
    FILE_PATH.mkdir(exist_ok=True)
    (FILE_PATH / 'pokemon').mkdir(exist_ok=True)
    (FILE_PATH / 'items').mkdir(exist_ok=True)

    try:
        TERMINAL_WIDTH = get_terminal_size().columns
    except OSError:
        TERMINAL_WIDTH = 80

    POKEMON_ROOT = 'https://play.pokemonshowdown.com/sprites/dex/'
    ITEM_ROOT = 'https://play.pokemonshowdown.com/sprites/itemicons/'

    POKEMON_ROOT_DOC = get(POKEMON_ROOT).text
    ITEM_ROOT_DOC = get(ITEM_ROOT).text

    png_href_regex = re.compile(r'<a href="(.*?\.png)">')

    pokemon = png_href_regex.findall(POKEMON_ROOT_DOC)
    items = png_href_regex.findall(ITEM_ROOT_DOC)

    for i, png in enumerate(pokemon):
        s = f'[{i + 1}/{len(pokemon)}] Downloading {png}'
        print(s.ljust(TERMINAL_WIDTH - len(s) - 1), end='\r', flush=True)
        s = f'[{i + 1}/{len(pokemon)}] Retrying {png}'
        r = get(POKEMON_ROOT + png)
        while len(r.content) == 0:
            print(s, end='\r', flush=True)
            r = get(POKEMON_ROOT + png)
        with open(FILE_PATH / 'pokemon' / png, 'wb') as f:
            f.write(r.content)
    print()
    for i, png in enumerate(items):
        s = f'[{i + 1}/{len(items)}] Downloading {png}'
        print(s.ljust(TERMINAL_WIDTH - len(s) - 1), end='\r', flush=True)
        s = f'[{i + 1}/{len(pokemon)}] Retrying {png}'
        r = get(ITEM_ROOT + png)
        while len(r.content) == 0:
            print(s.ljust(TERMINAL_WIDTH - len(s) - 1), end='\r', flush=True)
            r = get(ITEM_ROOT + png)
        with open(FILE_PATH / 'items' / png, 'wb') as f:
            f.write(r.content)


if __name__ == '__main__':
    main()
