import unicodedata


def clear_text(txt):
    normalized_text = unicodedata.normalize('NFD', txt)
    non_comb = ''.join(c for c in normalized_text
                       if not unicodedata.combining(c) and c not in ['~', '´', '`', '¨', '^'])
    return unicodedata.normalize('NFC', non_comb)
