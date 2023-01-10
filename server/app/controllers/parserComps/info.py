class Info:
    """Paper info."""

    no = None

    def __init__(self, issue, pdf_td, no_td, info_td):
        self.pdf_td = pdf_td
        self.no_td = no_td
        self.info_td = info_td

        self.no = None

        self.title_ru = None
        self.authors_ru = None
        self.keywords_ru = None
        self.citation_ru = None
        self.abstract_ru = None

        self.title_en = None
        self.authors_en = None
        self.keywords_en = None
        self.citation_en = None
        self.abstract_en = None

        self.issue = issue.title
        self.pdf = None
        
        self.page_ru = None
        self.page_en = None

        self._issue = issue


