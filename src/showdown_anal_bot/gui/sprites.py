"""
This file contains the sprites used in the GUI.
"""
import pathlib


def get_path_to_sprite(pokemon):
    path = pathlib.Path(__file__).parent / ("sprites/pokemon/" + pokemon.lower() + ".png")
    if not path.exists():
        path = pathlib.Path(__file__).parent / "sprites/blank.png"
    print(path)
    return str(path)
