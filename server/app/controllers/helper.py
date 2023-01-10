import re

"""Sanitize string"""

def sstr(info, noendl=True, noenddot=False):
    # Rewrite non-standard spaces
    res = re.sub(r'[^\S\n]', ' ', info)

    # Remove double spaces
    if noendl:
        res = re.sub(r'\n', ' ', res)
        res = re.sub(r'\s\s+', ' ', res)
    else:
        res = re.sub(r'[^\S\n][^\S\n]+', ' ', res)

    # Remove initial dots or commas
    res = re.sub(r'^[\s.,]+', '', res)

    # Remove last dot
    if noenddot:
        res = re.sub(r'\.$', '', res)

    # Strip string
    return res.strip()
