"""
This thing parses and handles commands
"""

from .helpers import insert_into_deepest_list, better_match_case, syntax_string


def split_command(cmd: str, fs: list, fallback: dict = None, token_parser: callable = None):
    if fallback is None:
        fallback = dict()
    final = fallback
    s = cmd.split(' ')
    args = ' '.join(s[1:]).split(', ')

    if token_parser is None:
        args = [
            int(token) if token.isnumeric() else
            token.split(';') if ';' in token
            else token
            for token in args
        ]
    else:
        args = [
            token_parser(token, n, len(args))
            for n, token in enumerate(args)
        ]

    for f in fs:
        fk = [*f.get('args', {}).keys()]
        ft = [*f.get('args', {}).values()]
        f = f.get('optional')
        while f is not None:
            fk += [*f.get('args', {}).keys()]
            ft += [*f.get('args', {}).values()]
            f = f.get('optional')
        if better_match_case(args, ft):
            final = dict(zip(fk, args))
            break

    return s[0], final


def generate_syntax_strings(formats: list, cmd: str) -> str:
    pre = []
    for f in formats:
        current = [*f.get('args', {}).keys()]
        f = f.get('optional')
        while f is not None:
            insert_into_deepest_list(current, [*f.get('args', {}).keys()])
            f = f.get('optional')
        pre.append(current)
    return ' || '.join([cmd + ' ' + syntax_string(p) for p in pre])
