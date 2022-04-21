import argparse as ap

from .bot import main as bot_main
from .cli import main as cli_main
# from .gui import main as gui_main
from .stalk import main as stalk_main
from . import cfg


gui_main = lambda *args, **kwargs: None  # WIP

MAIN_FUNCTIONS = {
    'bot': bot_main,
    'cli': cli_main,
    'gui': gui_main,
    'stalk': stalk_main,
}

parser = ap.ArgumentParser(description='Pokemon Showdown analysis tools')
subparser = parser.add_subparsers(dest='command')

# Bot subcommand
parser_bot = subparser.add_parser('bot', help='summonable pokemon bot')
parser_bot.add_argument(
    '-l', '--login', help=f'login file to use, default is {cfg.login_file_path}', default=cfg.login_file_path
)
parser_bot.add_argument('-uwl', '--enable-user-whitelist', help='enable user whitelist', action='store_true')
parser_bot.add_argument('-ubl', '--enable-user-blacklist', help='enable user blacklist', action='store_true')
parser_bot.add_argument('-fwl', '--enable-format-whitelist', help='enable format whitelist', action='store_true')
parser_bot.add_argument('-fbl', '--enable-format-blacklist', help='enable format blacklist', action='store_true')

# CLI subcommand
parser_cli = subparser.add_parser('cli', help='command line interface to bot')
parser_cli.add_argument('-u', '--username', help='fake username to use', dest='fake_username', default=cfg.fake_username)

# GUI subcommand (TODO)
parser_gui = subparser.add_parser('gui', help='graphical interface to bot')

# Stalk subcommand
parser_stalk = subparser.add_parser('stalk', help='stalk a set of users or game formats')
parser_stalk.add_argument('-u', '--users', help='users to stalk', nargs='+', dest='to_stalk',
                          default=cfg.stalk_config['to_stalk'])
parser_stalk.add_argument('-f', '--formats', help='formats to stalk', nargs='+', dest='game_modes',
                          default=cfg.stalk_config['game_modes'])
parser_stalk.add_argument('-o', '--output', help='output directory', dest='battle_log_location',
                          default=cfg.stalk_config['battle_log_location'])
parser_stalk.add_argument('-e', '--min-elo', help='minimum elo to stalk', type=int, dest='min_elo',
                          default=cfg.stalk_config['min_elo'])
parser_stalk.add_argument('-m', '--max-battle-count', help='maximum battle count to stalk', type=int,
                          dest='max_battle_count', default=cfg.stalk_config['max_battles'])
parser_stalk.add_argument('-q', '--query-interval', help='query interval in seconds', type=int, dest='query_interval',
                          default=cfg.stalk_config['query_interval'])


if __name__ == '__main__':
    args = parser.parse_args()
    kwargs = vars(args)
    command = kwargs.pop('command')
    if command in MAIN_FUNCTIONS:
        MAIN_FUNCTIONS[command](**kwargs)
    else:
        parser.print_help()
