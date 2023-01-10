import re
import requests
from bs4 import BeautifulSoup
from .info import Info

"""Parse paper no."""


def parse_paper_no(info: Info):
    no = int(info.no_td.text) if len(
        info.no_td.text.strip()) > 0 else None
    
    # HOT FIXES
    if info.issue == '37-3' and no == 108:
        no = 10

    info.no = no
    # print(info.no)

    return 1
