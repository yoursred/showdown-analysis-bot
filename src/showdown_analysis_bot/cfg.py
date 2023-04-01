import pathlib

user_wl = [

]

user_bl = [

]

format_wl = [

]

format_bl = [

]

login_file_path = "login.txt"

command_prefix = '.'

battle_log_location = pathlib.Path.cwd() / pathlib.Path('./battles/')  # TODO: make less ugly
battle_log_location.mkdir(parents=True, exist_ok=True)

stalk_config = {
    'to_stalk': None,
    'game_modes': [
        'gen8ou',
    ],
    'min_elo': 0,
    'max_battles': 5,
    'query_interval': 5,
    'battle_log_location': battle_log_location,
}

fake_username = 'fake_username'


cache_battle_logs = True
