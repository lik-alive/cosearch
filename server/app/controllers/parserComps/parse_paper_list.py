import re
import requests
from bs4 import BeautifulSoup
from .info import Info

"""Parse paper list."""


def parse_paper_list(issue, english=False):
    if english:
        if issue.en_href is None:
            return []

        issue_href = issue.en_href
    else:
        issue_href = issue.ru_href if issue.ru_href is not None else issue.en_href

    r = requests.get(issue_href)
    soup = BeautifulSoup(r.content, 'html.parser')

    infos = []
    ulinks = []

    # HOT FIXES
    no = 1
    if english and issue.title == '1':
        no = -1

    # Parse by pdf-images
    if (not english and issue.vol > 24 or issue.vol < 19) or (english and issue.vol > 22 or issue.vol < 19):
        file_imgs = soup.select('img')

        for file_img in file_imgs:
            # Skip journal covers
            if (file_img['height'] != '31'):
                continue

            pdf_td = file_img.find_previous('td')
            no_td = pdf_td.find_next_sibling('td')
            info_td = no_td.find_next_sibling('td')

            # HOT FIXES (empty numbering)
            if english and (issue.title == '1' or issue.title == '3' or issue.title == '4'):
                info_td = no_td
                # Skip intro papers
                if no > 0:
                    no_td = BeautifulSoup(f"<td>{no}</td>", 'html.parser')
                else:
                    no_td = BeautifulSoup(f"<td></td>", 'html.parser')

                no += 1

            infos.append(Info(issue, pdf_td, no_td, info_td))

    # Parse by links
    else:
        links = soup.select('a')
        i = 0
        while (i < len(links)):
            link = links[i]
            i += 1

            # Skip empty links
            if not link.has_attr('href'):
                continue
            if len(link.text) == 0:
                continue

            # Skip mailto
            if 'mailto' in link['href']:
                break

            pdf_td = None
            info_td = link.find_previous('td')
            no_td = info_td.find_previous_sibling('td')

            # Check links duplication
            if link['href'] in ulinks:
                pass
            else:
                ulinks.append(link['href'])
                infos.append(Info(issue, pdf_td, no_td, info_td))

    return infos
