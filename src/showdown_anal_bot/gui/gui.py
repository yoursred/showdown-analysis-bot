import PySimpleGUIQt as sg

from src.showdown_anal_bot.gui.sprites import get_path_to_sprite as get_sprite

# TODO: wait for PySimpleGUIWx to be usable
# TODO: flesh out the GUI, figure out what to add


# I have given up on getting a native looking GUI.
# Update: I am giving up on a GUI.

def create_pokemon_layout(pokemon: dict):
    # Allegedly, pysimpleguiwx doesn't support images, so we're using background images instead
    layout = [
        [sg.Image(filename=get_sprite(pokemon['name']), size=(120, 120)),
         sg.Frame('', [[sg.Text(move)] for move in pokemon['moves']])],
        [sg.Text(pokemon['name'])]
    ]
    return layout


def test_layout(layout):
    sg.Window('Test Window', layout).read()


TABS = {
    'Analyzer': [
        []
    ],
    'Stalker': [],
    'Settings': [],
    'About': [],
}


def main(**kwargs):
    pokemon = {
        'name': 'Pikachu',
        'moves': ['Thunderbolt', 'Thunder Wave', 'Quick Attack', 'Thunder']
    }

    test_layout(create_pokemon_layout(pokemon))


if __name__ == '__main__':
    main()
