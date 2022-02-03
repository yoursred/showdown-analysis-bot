import PySimpleGUI as sg
from team_extractor import  get_team_from_replays, team2str

sg.theme('System Default 1')

formats = [
    'gen8vgc2021series10',
    'gen8ou',
    'gen8uu',
    'gen8lc'
    'gen8ubers'
]

layout = [
    [
        sg.T('Username:'),
        sg.InputText(key='username', size=20),
        sg.T('Depth:'),
        sg.Spin([*range(1, 50)], initial_value=5, key='depth')
    ],
    [
        sg.T('Required:'),
        sg.InputText(key='pokes', size=20),
        sg.T('Format:'),
        sg.Combo(formats, key='format')
    ],
    [sg.Button('Find')],
    [sg.Multiline('Hmm', key='out', disabled=True, size=(48, 12), no_scrollbar=True, font=('helvetica', 14))]
]

window = sg.Window('walhex', layout, font=('helvetica', 12))

while True:
    e, v = window.read()
    if e == sg.WIN_CLOSED:  # if user closes window or clicks cancel
        break
    elif e == 'Find':
        team, th, c = get_team_from_replays(
            v['username'],
            v['format'],
            c=v['depth'],
            pokes=v['pokes'].split(';') if v['pokes'] else None
        )

        team = team2str(team)

        window['out'].update(team)
    print(v)