import re
import requests
from bs4 import BeautifulSoup
from .issue import Issue

"""Parse list of all issues"""


def parse_issues(endpoint):
    r = requests.get(endpoint)
    soup = BeautifulSoup(r.content, 'html.parser')

    # Skip actual number link
    links = soup.select(
        'tr:not(:first-of-type):not(:nth-of-type(2))>td a')

    # Parse issues (skip fake link)
    issues = [Issue(link['href']) for link in filter(
        lambda link: len(link.text) < 20 and link['href'], links)]

    # Reverse order
    return issues[::-1]
    # return issues
