import datetime as dt


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
