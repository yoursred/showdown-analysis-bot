"""Parse replay and extract team and top heavy data from it"""
import pathlib
import gzip

from requests import get
from showdown import utils

from .cfg import battle_log_location, cache_battle_logs


# TODO: iron out all edge cases
# TODO: add risk analysis


last_ltm = {}


def get_last_replays(user, format_, c=5):
    user = utils.name_to_id(user)
    replays = get(f'https://replay.pokemonshowdown.com/search.json?user={user}&format={format_}').json()

    replay_ids = []

    for replay in replays:
        r = (
            replay['id'],
            replay['uploadtime'],
            'p1' if utils.name_to_id(replay['p1']) == user else 'p2',
        )
        replay_ids.append(r)

    return replay_ids[:c]


def get_teams(replay_id):
    # This function parses a battle replay and gets all revealed info about the teams
    if (battle_log_location / f'{replay_id}.gz').exists():
        cached = True
        with gzip.open(battle_log_location / f'{replay_id}.gz', 'rb') as f:
            battle_log = f.read().decode('utf-8')
    else:
        cached = False
        battle_log = get(f'https://replay.pokemonshowdown.com/{replay_id}.log').text

    if cache_battle_logs and not cached:
        with open(battle_log_location / (replay_id + '.gz'), 'wb') as f:
            f.write(gzip.compress(battle_log.encode('utf-8')))

    p1 = ''
    p2 = ''

    p1_pokes = {}
    p1_nicks = {}
    p2_pokes = {}
    p2_nicks = {}

    for line in battle_log.splitlines():
        if line.startswith('|poke|p1'):
            data = line.split('|')[3].split(', ')
            form = data[0]
            base_species = form.split('-')[0].lower()
            # level = '100' if 'L' not in data[1] else data[1].lstrip('L')

            p1_pokes[base_species] = {
                'form': form,
                # 'level': level,
                'moves': set(),
                'revealed': False
            }
        if line.startswith('|poke|p2'):
            data = line.split('|')[3].split(', ')
            form = data[0]
            base_species = form.split('-')[0].lower()
            # level = data[1].lstrip('L')

            p2_pokes[base_species] = {
                'form': form,
                # 'level': level,
                'moves': set(),
                'revealed': False
            }
        if line.startswith('|switch|p1') or line.startswith('|drag|p1') or line.startswith('|repalce|p1'):
            nick = line.split('|')[2].split(': ')[1]
            form = line.split('|')[3].split(', ')[0]
            base_species = form.split('-')[0].lower()
            p1_pokes[base_species]['nick'] = nick
            p1_nicks[nick] = base_species
            p1_pokes[base_species]['form'] = form
            p1_pokes[base_species]['revealed'] = True
        if line.startswith('|switch|p2') or line.startswith('|drag|p2') or line.startswith('|replace|p2'):
            nick = line.split('|')[2].split(': ')[1]
            form = line.split('|')[3].split(', ')[0]
            base_species = form.split('-')[0].lower()
            p2_pokes[base_species]['nick'] = nick
            p2_nicks[nick] = base_species
            p2_pokes[base_species]['form'] = form
            p2_pokes[base_species]['revealed'] = True
        if line.startswith('|move|p1') and not line.endswith('|[from]Metronome'):
            user = line.split('|')[2].split(': ')[1]
            move = line.split('|')[3]
            p1_pokes[p1_nicks[user]]['moves'].add(move)
        if line.startswith('|move|p2') and not line.endswith('|[from]Metronome'):
            user = line.split('|')[2].split(': ')[1]
            move = line.split('|')[3]
            p2_pokes[p2_nicks[user]]['moves'].add(move)
        if line.startswith('|-ability|p1'):
            user = line.split('|')[2].split(': ')[1]
            ability = line.split('|')[3]
            p1_pokes[p1_nicks[user]].setdefault('ability', ability)
        if line.startswith('|-ability|p2'):
            user = line.split('|')[2].split(': ')[1]
            ability = line.split('|')[3]
            p2_pokes[p2_nicks[user]].setdefault('ability', ability)
        if '|[from] ability' in line and '|[of] p1' in line:
            data = line.split('|[from] ability: ')
            ability = data[1].split('|[of]')[0]
            user = data[1].split(': ')[1].split('|')[0]
            p1_pokes[p1_nicks[user]].setdefault('ability', ability)
        if '|[from] ability' in line and '|[of] p2' in line:
            data = line.split('|[from] ability: ')
            ability = data[1].split('|[of]')[0]
            user = data[1].split(': ')[1].split('|')[0]
            p2_pokes[p2_nicks[user]].setdefault('ability', ability)
        if line.startswith('|player|p1'):
            p1 = utils.name_to_id(line.split('|')[3])
        if line.startswith('|player|p2'):
            p2 = utils.name_to_id(line.split('|')[3])
        if line.startswith('|-enditem|p1'):
            data = line.split(': ')[1].split('|')
            item = data[1]
            user = data[0]
            p1_pokes[p1_nicks[user]].setdefault('item', item)
        if line.startswith('|-enditem|p2'):
            data = line.split(': ')[1].split('|')
            item = data[1]
            user = data[0]
            p2_pokes[p2_nicks[user]].setdefault('item', item)
        if line.startswith('|-item|p1'):
            data = line.split(': ')[1].split('|')
            # print(data)
            item = data[1]
            user = data[0]
            p1_pokes[p1_nicks[user]].setdefault('item', item)
        if line.startswith('|-item|p2'):
            data = line.split(': ')[1].split('|')
            # print(data)
            item = data[1]
            user = data[0]
            p2_pokes[p2_nicks[user]].setdefault('item', item)
        if '|[from] item' in line and '|p1' in line:
            data = line.split(': ')
            item = data[2]
            user = data[1].split('|')[0]
            p1_pokes[p1_nicks[user]].setdefault('item', item)
        if '|[from] item' in line and '|p2' in line:
            data = line.split(': ')
            item = data[2]
            user = data[1].split('|')[0]
            p2_pokes[p2_nicks[user]].setdefault('item', item)
        if line.startswith('|-activate') and 'move: Poltergeist' in line and '|p1' in line:
            item = line.split('|')[-1]
            user = line.split(': ')[1].split('|')[0]
            p1_pokes[p1_nicks[user]].setdefault('item', item)
        if line.startswith('|-activate') and 'move: Poltergeist' in line and '|p2' in line:
            item = line.split('|')[-1]
            user = line.split(': ')[1].split('|')[0]
            p2_pokes[p2_nicks[user]].setdefault('item', item)
        if line.startswith('|-start|p1') and '|Dynamax|' in line:
            user = line.split('|')[2].split(': ')[1]
            p1_pokes[p1_nicks[user]]['dynamax'] = True
            if 'Gmax' in line:
                p1_pokes[p1_nicks[user]]['gmax'] = True
        if line.startswith('|-start|p2') and '|Dynamax|' in line:
            user = line.split('|')[2].split(': ')[1]
            p2_pokes[p2_nicks[user]]['dynamax'] = True
            if 'Gmax' in line:
                p2_pokes[p2_nicks[user]]['gmax'] = True


    return p1_pokes, p2_pokes


def get_team_from_replays(user, format_, c=5, t=1, required_pokes=None, pokes=None):
    """
    Get a team from replays. "top-heavy" here means pokemon that are used in the most
    :param user:
    :param format_:
    :param c:
    :param t:
    :param required_pokes:
    :param pokes:
    :return:
    """
    if pokes is None:
        pokes = []

    replays = get_last_replays(user, format_, c)
    replays.sort(key=lambda x: x[1])  # sort from oldest to newest

    team = {}
    battles = 0
    useful_samples = 0
    top_heavy = {}
    likely_team_mates = {}
    global last_ltm
    teams = []

    for replay in replays:
        i = 0
        teams = get_teams(replay[0])  # get both teams from replay id
        if replay[2] == 'p1':  # get the team of the user we're after
            team_snippet = teams[0]
        else:
            team_snippet = teams[1]
        if required_pokes:
            b = all(map(lambda x: x in team_snippet, required_pokes))
        else:
            b = True
        if (len(set(team_snippet) - set(team)) < t or (not team)) and b:
            battles += 1
            for k, v in team_snippet.items():
                if k in team:
                    m0 = team[k]['moves']
                    team[k].update(v)
                    team[k]['moves'].update(m0)
                else:
                    team[k] = v
                if v['revealed']:
                    i += 1
                    if k in top_heavy:
                        top_heavy[k] += 1
                    else:
                        top_heavy[k] = 1

                    for k_, v_ in team_snippet.items():
                        if v_['revealed'] and k_ != k:
                            if k in likely_team_mates:
                                if k_ in likely_team_mates[k]:
                                    likely_team_mates[k][k_] += 1
                                else:
                                    likely_team_mates[k][k_] = 1
                            else:
                                likely_team_mates[k] = {k_: 1}
        if i > 3:
            useful_samples += 1

    last_ltm = likely_team_mates

    return team, {k: v / battles for k, v in top_heavy.items()}, likely_team_mates, battles


def get_likely_back(lead_pokes):
    # This does the same thing as top_heavy, but one level deeper.
    l = {}
    for p in lead_pokes:
        for k, v in last_ltm.get(p, {}).items():
            if k not in lead_pokes:
                if k in l:
                    l[k] += v
                else:
                    l[k] = v
    return l


def team2str(team, th, ltm):
    teamstr = ''
    for base_species, poke in team.items():
        if (nick := poke.get('nick', base_species.capitalize())) == base_species.capitalize():
            teamstr += poke['form'] + ' '
        else:
            teamstr += f"{poke['nick']} ({poke['form']}) "

        teamstr += f"@ {poke.get('item', 'Unknown')}, "
        teamstr += f"Ability: {poke.get('ability', 'Unknown')}"
        teamstr += ', G' if poke.get('gmax') else (', X' if poke.get('dynamax') else '')
        teamstr += f"\n {nick} moves: [ "
        for move in poke.get('moves', ()):
            teamstr += f"{move}, "

        teamstr += ']\n'

    return teamstr.strip()
