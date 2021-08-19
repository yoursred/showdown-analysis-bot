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