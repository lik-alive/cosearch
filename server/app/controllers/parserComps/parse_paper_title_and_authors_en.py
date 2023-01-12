import re
import requests
from bs4 import BeautifulSoup
from .info import Info
from app.actions.helper import sstr

"""Parse paper title and authors in English."""


def parse_paper_title_and_authors_en(info: Info):
    # Find by link (1-5, 22+)
    if info._issue.vol <= 5 or info._issue.vol >= 22:
        links = info.info_td.select('a')

        i = 0
        while i < len(links):
            link = links[i]
            i += 1

            # Skip staff links
            if 'staff' in link['href'].lower():
                continue
            # Skip empty links
            if len(link.text.strip()) == 0:
                continue
            if 'kotlyar' in link['href'].lower():
                continue
            if 'index.html' in link['href'].lower():
                continue

            title = link.text

            # Sanitize
            title = sstr(title, True, True)

            # HOT FIXES
            if info.issue == '22' and info.no == 15:
                title = 'P' + title
            elif info.issue == '24' and info.no == 2:
                title = sstr(
                    'Diffraction calculation of focusators into focal curves within the framework of electromagnetic theory')
            elif info.issue == '28' and info.no == 1:
                title = sstr(
                    'Rotation of microparticles in light fields')
            elif info.issue == '28' and info.no == 24:
                title = sstr(
                    'Image compression using discrete orthogonal transforms defined on the evolvements of two-dimensional fields')
            elif info.issue == '33-3' and info.no == 12:
                title = title.replace('А', 'A')
            elif info.issue == '37-2' and info.no == 18:
                title = sstr(
                    "Object identification in labyrinthine domain structures")
            elif info.issue == '39-1' and info.no == 5:
                title = title.replace('с', 'c')
            elif info.issue == '39-2' and info.no == 14:
                title = title.replace('с', 'c')
            if info.issue == '39-3' and info.no == 4:
                title = title.replace('с', 'c')
            elif info.issue == '39-5' and info.no == 14:
                title = title.replace('с', 'c')
            elif info.issue == '41-2' and info.no == 9:
                title = title.replace('е', 'e')
            elif info.issue == '42-3' and info.no == 3:
                title = title.replace('с', 'c')
            elif info.issue == '44-4' and info.no == 20:
                title = title.replace('а', 'a')

            # Check locale
            rus = re.findall(r'[А-ЯЁа-яё]', title)
            if len(rus) > 0:
                print('!!!Russian letters in title', info.issue, info.no, rus)
                return

            info.title_en = title

            # Parse authors
            info_str = sstr(info.info_td.text)

            # Fix dots
            info_str = re.sub(r'\.([A-ZА-ЯЁ])', r'. \1', info_str)

            # Fix quote
            info_str = info_str.replace('’', '\'')

            # Merge initials (three and two initials in separate cases since re.sub looks only once)
            info_str = re.sub(
                r'([A-ZА-ЯЁ][a-zа-яё]?\.) ([A-ZА-ЯЁ][a-zа-яё]?\.) ([A-ZА-ЯЁ][a-zа-яё]?\.)', r'\1\2\3', info_str)
            info_str = re.sub(
                r'([A-ZА-ЯЁ][a-zа-яё]?\.) ([A-ZА-ЯЁ][a-zа-яё]?\.)', r'\1\2', info_str)

            # Insert dots between initials
            info_str = re.sub(
                r"([A-ZА-ЯЁ][\w'-]+ [A-ZА-ЯЁ])([A-ZА-ЯЁ])[.]", r'\1.\2.', info_str)
            info_str = re.sub(
                r"([A-ZА-ЯЁ][\w'-]+ [A-ZА-ЯЁ])([A-ZА-ЯЁ])([, ])", r'\1.\2.\3', info_str)

            # Remove 'and' between authors
            info_str = re.sub(
                r"([A-ZА-ЯЁ]\.[A-ZА-ЯЁ]\. [A-ZА-ЯЁ][\w'-]+),? and ([A-ZА-ЯЁ]\.[A-ZА-ЯЁ]\. [A-ZА-ЯЁ][\w'-]+)", r'\1, \2', info_str)

            # Remove space before comma
            info_str = info_str.replace(' ,', ',')

            # Separate comma and the following letter
            info_str = re.sub(r",(\w)", r', \1', info_str)

            # Get first 'word' of the title
            word = title[0:5]

            # Initials last
            if (info.issue == '22') or (info.issue == '23') or (info.issue == '25' and info.no == 15) or (info.issue == '30' and info.no == 10) or (info.issue == '30' and info.no == 11) or (info.issue == '34-2' and info.no == 4) or (info.issue == '34-4' and info.no == 12) or (info.issue == '35-3' and info.no == 17) or (info.issue == '35-4' and info.no == 13) or (info.issue == '37-1' and info.no == 8) or (info.issue == '39-1') or (info.issue == '39-2' and info.no == 15) or (info.issue == '41-5') or (info.issue == '41-6') or (info._issue.vol >= 42):
                items = re.findall(
                    r"^(([A-ZА-ЯЁ][\w'-]+ [A-ZА-ЯЁ][a-zа-яё]?\.(-?[A-ZА-ЯЁ][a-zа-яё]?\.)*,? ?)+)\.? ?" + word, info_str)
            # Initials first
            else:
                items = re.findall(
                    r"^(([A-ZА-ЯЁ][a-zа-яё]?\.(-?[A-ZА-ЯЁ][a-zа-яё]?\.)* [A-ZА-ЯЁ][\w'-]+,? ?)+)\.? ?" + word, info_str)

            # HOT FIXES
            # if info.issue == '1' and info.no == 5:
            #     info.authors_en = sstr(
            #         'V.A. Danilov, B.E. Kinber, A.V. Shishlov')
            #     break
            # if info.issue == '24' and info.no == 15:
            #     info.authors_en = sstr(
            #         'A.N. Malov, I.V. Bogdan, S.N. Malov, Y.N. Vigovsky, A.G. Konop, S.P. Konop')
            #     break

            if len(items) > 0 and len(items[0]) > 2:
                authors = sstr(items[0][0])

                # HOT FIX
                if info.issue == '1' and info.no == 3:
                    authors = sstr('B.E. Kinber, S.N. Kaptsov')

                # HOT FIX (Russian letters)
                if info.issue == '1' and info.no == 5:
                    authors = authors.replace('В', 'B')
                    authors = authors.replace('Е', 'E')
                elif info.issue == '24' and info.no == 15:
                    authors = authors.replace('К', 'K')
                elif info.issue == '31-3' and info.no == 4:
                    authors = authors.replace('А', 'A')
                elif info.issue == '31-4' and info.no == 4:
                    authors = authors.replace('А', 'A')
                elif info.issue == '32-4' and info.no == 1:
                    authors = authors.replace('Т', 'T')
                elif info.issue == '34-3' and info.no == 9:
                    authors = authors.replace('О', 'O')
                elif info.issue == '35-2' and info.no == 13:
                    authors = authors.replace('О', 'O')
                elif info.issue == '36-4' and info.no == 1:
                    authors = authors.replace('Е', 'E')
                    authors = authors.replace('К', 'K')
                elif info.issue == '37-1' and info.no == 6:
                    authors = authors.replace('Е', 'E')
                elif info.issue == '38-4' and info.no == 1:
                    authors = authors.replace('А', 'A')
                elif info.issue == '38-4' and info.no == 3:
                    authors = authors.replace('А', 'A')
                elif info.issue == '38-4' and info.no == 36:
                    authors = authors.replace('А', 'A')
                    authors = authors.replace('М', 'M')
                elif info.issue == '39-5' and info.no == 11:
                    authors = authors.replace('А', 'A')
                elif info.issue == '39-5' and info.no == 24:
                    authors = authors.replace('К', 'K')
                elif info.issue == '40-2' and info.no == 8:
                    authors = authors.replace('А', 'A')
                elif info.issue == '43-3' and info.no == 14:
                    authors = authors.replace('А', 'A')
                    authors = authors.replace('М', 'M')
                elif info.issue == '43-5' and info.no == 13:
                    authors = authors.replace('А', 'A')
                    authors = authors.replace('М', 'M')
                elif info.issue == '44-4' and info.no == 6:
                    authors = authors.replace('А', 'A')
                    authors = authors.replace('М', 'M')
                elif info.issue == '45-2' and info.no == 12:
                    authors = authors.replace('А', 'A')
                elif info.issue == '46-5' and info.no == 6:
                    authors = authors.replace('А', 'A')
                elif info.issue == '46-6' and info.no == 11:
                    authors = authors.replace('с', 'c')
                elif info.issue == '46-6' and info.no == 16:
                    authors = authors.replace('М', 'M')
                    authors = authors.replace('Т', 'T')
                    authors = authors.replace('а', 'a')
                    authors = authors.replace('А', 'A')
                    authors = authors.replace('К', 'K')

                rus = re.findall(r'[А-ЯЁа-яё]', authors)
                if len(rus) > 0:
                    print('!!!Russian letters in authors',
                          info.issue, info.no, rus)
                    return

                info.authors_en = authors
                # print(authors)
            else:
                if info.issue == '1' and info.no == 3:
                    info.authors_en = "B.E. Kinber, S.N. Kaptsov"
                elif info.issue == '1' and info.no == 19:
                    info.authors_en = "M.A. Man'ko, B.I. Makhsudov, Pham Van Hoi"
                elif info.issue == '3' and info.no == 15:
                    info.authors_en = "I.N. Sisakyan, V.P. Shorin, V.A. Soifer, V.I. Mordasov, V.V. Popov"
                elif info.issue == '22' and info.no == 1:
                    info.authors_en = None
                elif info.issue == '25' and info.no == 6:
                    info.authors_en = "A.A. Belousov, A.V. Gavrilov, A.A. Degtyarev"
                elif info.issue == '26' and info.no == 1:
                    info.authors_en = None
                elif info.issue == '26' and info.no == 14:
                    info.authors_en = "A.O. Korepanov, N.Y. Ilyasova, A.V. Kupriyanov, A.G. Khramov, A.V. Ustinov, A.A. Kovalev"
                elif info.issue == '31-3' and info.no == 12:
                    info.authors_en = "P.I. Mikhailov, R.T. Faizullin"
                elif info.issue == '31-4' and info.no == 12:
                    info.authors_en = "P.I. Mikhailov, R.T. Faizullin"
                elif info.issue == '32-1' and info.no == 1:
                    info.authors_en = None
                elif info.issue == '32-1' and info.no == 2:
                    info.authors_en = None
                elif info.issue == '33-3' and info.no == 12:
                    info.authors_en = "D.L. Golovashkin, N.N. Zhuravleva"
                elif info.issue == '34-2' and info.no == 2:
                    info.authors_en = "V.L. Derbov, V.V. Serov, N.I. Teper"
                elif info.issue == '35-1' and info.no == 4:
                    info.authors_en = "G.I. Greysukh, E.G. Ezhov, I.A. Levin, S.A. Stepanov"
                elif info.issue == '35-2' and info.no == 4:
                    info.authors_en = "A.I. Plastinin, A.G. Khramov, V.A. Soifer"
                elif info.issue == '36-2' and info.no == 2:
                    info.authors_en = "N.V. Golovastikov, D.A. Bykov, L.L. Doskolovich, V.A. Soifer"
                elif info.issue == '37-3' and info.no == 3:
                    info.authors_en = "I.V. Alimenkov, Yu.G. Pchelkina"
                elif info.issue == '37-4' and "In the memory" in title:
                    info.authors_en = None
                elif info.issue == '40-2' and info.no == 5:
                    info.authors_en = "E.N. Vorontsov, N.N. Losevsky, D.V. Prokopova, E.V. Razueva, S.A. Samagin"
                elif info.issue == '40-4' and info.no == 1:
                    info.authors_en = "D.A. Kozlov, E.S. Kozlova, V.V. Kotlyar"
                elif info.issue == '42-5' and info.no == 2:
                    info.authors_en = "Volyar A.V., Bretsko M.V., Akimova Ya.E., Egorov Yu.A."
                elif info.issue == '43-3' and info.no == 13:
                    info.authors_en = "Bettaieb A., Filali N., Filali T., Ben Aissia H."
                elif info.issue == '44-3' and info.no == 7:
                    info.authors_en = "Bettaieb A., Filali N., Filali T., Ben Aissia H."
                elif info.issue == '44-4' and info.no == 5:
                    info.authors_en = "Burdin V.A., Bourdine A.V., Gubareva O.Yu."
                elif info.issue == '45-4' and 'Editorial' in title:
                    info.authors_en = None
                elif info.issue == '45-5' and info.no == 4:
                    info.authors_en = "Akimov A.A., Guzairov S.A., Ivakhnik V.V."
                elif info.issue == '45-6' and info.no == 10:
                    info.authors_en = "Rodiah, Madenda S., Susetianingtias D.T., Fitrianingsih, Adlina D., Arianty R."
                elif info.issue == '46-1' and info.no == 4:
                    info.authors_en = "Correa-Rojas N.A., Gallego-Ruiz R.D., Álvarez-Castaño M.I."
                elif info.issue == '46-2' and info.no == 20:
                    info.authors_en = None
                elif info.issue == '47-1' and info.no == 11:
                    info.authors_en = "Bibikov S., Petrov M., Alekseev A., Aliev M., Paringer R., Goshin Y., Serafimovich P., Nikonorov A."
                else:
                    print("!!!Parsing failed", info.issue,
                          info.no, info_str, word)

            break

    # # Parse by regex (22-30)
    # else:
    #     info_str = sstr(info.info_td.text)

    #     # HOT FIXES
    #     # if info._issue.vol == 24 and info.no == 2:
    #     #     info_str = re.sub(r'С\..?И Харитонов', 'С.И. Харитонов', info_str)

    #     # Fix dots
    #     info_str = re.sub(r'\.([A-ZА-ЯЁ])', r'. \1', info_str)

    #     # Separate initials with dots
    #     info_str = re.sub(
    #         r'([A-ZА-ЯЁ]\w+) ([A-ZА-ЯЁ])([A-ZА-ЯЁ])([A-ZА-ЯЁ])', r'\1 \2.\3.\4.', info_str)
    #     info_str = re.sub(
    #         r'([A-ZА-ЯЁ]\w+) ([A-ZА-ЯЁ])([A-ZА-ЯЁ])', r'\1 \2.\3.', info_str)

    #     # Merge initials (three and two initials in separate cases since re.sub looks only once)
    #     info_str = re.sub(
    #         r'([A-ZА-ЯЁ][a-zа-яё]?\.) ([A-ZА-ЯЁ][a-zа-яё]?\.) ([A-ZА-ЯЁ][a-zа-яё]?\.)', r'\1\2\3', info_str)
    #     info_str = re.sub(
    #         r'([A-ZА-ЯЁ][a-zа-яё]?\.) ([A-ZА-ЯЁ][a-zа-яё]?\.)', r'\1\2', info_str)

    #     # Initials last
    #     if info._issue.vol == 22 or info._issue.vol == 23 or info._issue.vol > 24:
    #         items = re.findall(
    #             r"^(([A-ZА-ЯЁ]\w+ [A-ZА-ЯЁ][a-zа-яё]?\.([A-ZА-ЯЁ]\.)?,? ?)+)\.? ?(.+)$", info_str)
    #     # Initials first
    #     else:
    #         items = re.findall(
    #             r"^(([A-ZА-ЯЁ][a-zа-яё]?\.([A-ZА-ЯЁ][a-zа-яё]?\.)? [A-ZА-ЯЁ]\w+,? ?)+)\.? ?(.+)$", info_str)

    #     if len(items) > 0 and len(items[0]) > 3:
    #         title = sstr(items[0][3], True, True)
    #         authors = sstr(items[0][0])

    #         # HOT FIX (Russian letters)
    #         if info.issue == '24' and info.no == 15:
    #             authors = authors.replace('К', 'K')

    #         # Check locale
    #         rus = re.findall(r'[А-ЯЁа-яё]', title)
    #         if len(rus) > 0:
    #             print('!!!Russian letters in title',
    #                   info.issue, info.no, rus)
    #             return
    #         rus = re.findall(r'[А-ЯЁа-яё]', authors)
    #         if len(rus) > 0:
    #             print('!!!Russian letters in authors',
    #                   info.issue, info.no, rus)
    #             return

    #         info.title_en = title
    #         info.authors_en = authors
    #         print(title)
    #     else:
    #         if info.issue == '22' and info.no == 1:
    #             info.title_en = info_str
    #         else:
    #             print('!!!Not parsed', info.issue, info.no, info_str)

        # HOT FIXES
        # if info.issue == '27' and info.no == 1:
        #     info.title_ru = sstr(
        #         'Микаэляну А.Л. - 80 лет')
        #     info.authors_ru = None

    return 1
