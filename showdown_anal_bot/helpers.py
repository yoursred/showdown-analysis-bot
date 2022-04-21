import datetime as dt
from difflib import SequenceMatcher as SM
from types import UnionType


def filter_from_bwlists(item, b, w):
    if b and item in b:
        return False
    if w and item in w:
        return True
    return True


def filter_user_from_bwlists(item, b, w):
    if b and item.name_matches(b):
        return False
    if w and item.name_matches(w):
        return True
    return True


def format_from_roomid(rid):
    rid.replace('battle-', '')
    return rid.split('-')[1]


def now():
    return dt.datetime.now().strftime('%H:%M:%S %d/%m/%Y')


def log(msg):
    print(f'[{now()}] {msg}')


def did_you_mean(word, possibilities):
    possibilities = [(p, SM(None, word, p).ratio()) for p in possibilities]
    m = max(possibilities, key=lambda x: x[1])
    if m[1] > 0.5:
        return m[0]
    return None


def insert_into_deepest_list(l, item):
    if len(l) == 0:
        l.append(item)
    elif isinstance(l[-1], list):
        insert_into_deepest_list(l[-1], item)
    else:
        l.append(item)


def better_match_case(to_match, to_match_against):
    if len(to_match) != len(to_match_against):
        return False
    for i in range(len(to_match)):
        if isinstance(to_match_against[i], (type, UnionType)):
            if not isinstance(to_match[i], to_match_against[i]):
                return False
        elif to_match_against[i] != to_match[i]:
            return False
    return True


def syntax_string(syntax):
    sl = [f'<{s}>' for s in syntax if isinstance(s, str)]
    string = ' '.join(sl)
    if len(syntax) > len(sl):
        string += ' ['
        string += syntax_string(syntax[-1])
        string += ']'
    return string
