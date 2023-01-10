class Issue:
    """Issue parser."""

    def __init__(self, href):
        page = href[0:href.index('.html')]

        if "og" in page:
            full_title = page[0:page.index('og')]
        else:
            full_title = page

        title = full_title[full_title.index('KO')+2:]

        if title[-1] == '_':
            title = title[0:-1]

        if title[0] == '0':
            title = title[1:]

        self.title = title
        self.ru_href = f'http://computeroptics.ru/KO/{page}.html'

        vol = title[0:title.index('-')] if '-' in title else title
        vol = int(vol)
        no = int(title[title.index('-') + 1:]) if '-' in title else 0

        self.vol = vol
        self.no = no

        if vol > 43 or (vol == 43 and no > 2):
            self.en_href = f'http://computeroptics.ru/eng/KO/{full_title}Eog.html'
        elif vol == 41 and no == 4:
            self.ru_href = None
            self.en_href = f'http://computeroptics.ru/eng/KO/KO41-4og.html'
        elif vol == 40 and no == 5:
            self.ru_href = None
            self.en_href = f'http://computeroptics.ru/eng/KO/ENG/KO40-5og.html'
        elif vol > 30:
            self.en_href = f'http://computeroptics.ru/eng/KO/{full_title}og.html'
        elif vol > 27:
            self.en_href = f'http://computeroptics.ru/eng/KO/{full_title}ogl.html'
        elif vol > 21:
            self.en_href = f'http://computeroptics.ru/eng/KO/{full_title}Eogl.html'
        elif vol > 4:
            self.en_href = None
        elif vol == 4:
            self.en_href = 'http://computeroptics.ru/eng/KO/KO_02_2-og.html'
        elif vol == 3:
            self.en_href = 'http://computeroptics.ru/eng/KO/KO_02_1-og.html'
        elif vol > 1:
            self.en_href = None
        else:
            self.en_href = f'http://computeroptics.ru/eng/KO/KO01ogl.html'

        # # Check pages
        # if (self.en_href is not None):
        #     r = requests.get(self.en_href)
        #     if r.status_code != 200:
        #         print(r.status_code)
        #         print(r.content)
        #         print(self.en_href)
        #         raise Exception('Stop')

    def __repr__(self):
        return f'{self.title} {self.ru_href} {self.en_href}'
