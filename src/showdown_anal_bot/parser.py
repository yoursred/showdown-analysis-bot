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
        args = [  # This the default token parsing routine
            int(token) if token.isnumeric() else  # If it's a number, make it an int
            token.split(';') if ';' in token  # If it's a list, split it
            else token  # Otherwise, just return it
            for token in args
            if token.strip() != ''  # As long as it's not an empty string
        ]
    else:
        args = [
            token_parser(token, n, len(args))
            for n, token in enumerate(args)
        ]
    matched = False
    for f in fs:
        fk = []
        ft = []
        matched = False
        lens = [len(f)]
        while f is not None:
            fk += [*f.get('args', {}).keys()]
            ft += [*f.get('args', {}).values()]
            lens.append(len(f))
            f = f.get('optional')
            if better_match_case(args, ft):
                matched = True
                final = dict(zip(fk, args))
                break
        if matched:
            break

    return s[0], final, matched


def generate_syntax_strings(formats: list, cmd: str) -> str:
    pre = []
    for f in formats:
        current = [*f.get('args', {}).keys()]
        f = f.get('optional')
        while f is not None:
            insert_into_deepest_list(current, [*f.get('args', {}).keys()])
            f = f.get('optional')
        pre.append(current)
    pre = [syntax_string(p) for p in pre]
    pre = [cmd + (' ' if p.startswith('<') else '') + p for p in pre]
    return ' || '.join(pre)
