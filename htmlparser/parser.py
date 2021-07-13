import requests
from bs4 import BeautifulSoup as bs
import re


class HtmlParser:
    """
    HtmlParser parse a 'h' 1-3 tags and 'a' tags then prettify links.
    You can get data as attributes of instance.
    """
    def __init__(self, url):
        self.url = url
        self.headers = {"user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 "
                                      "(KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36"}
        self.status_code = None
        self.h1 = None
        self.h2 = None
        self.h3 = None
        self.links = []
        self.status = True
        self._get_data()

    def _get_data(self):
        """
        This method calls other methods to get and record data
        """
        page = self._get_page()
        if not page:
            return False
        soup = bs(page, 'html.parser')
        self._get_h_tags(soup)
        self._get_a_tags(soup)

    def _get_page(self):
        """
        This method initially check url validation, then it get url page. If an exception arises it send status code
        or false.
        """
        page = self._validate_url()
        if not type(page) == requests.Response:
            self.status = False
            return
        if page.status_code == 200:
            self.status_code = page.status_code
            return page.text
        else:
            self.status_code = page.status_code
            return "Can not get page. Error code is {}".format(page.status_code)

    def _get_h_tags(self, soup) -> None:
        self.h1 = len(soup.find_all('h1'))
        self.h2 = len(soup.find_all('h2'))
        self.h3 = len(soup.find_all('h3'))

    def _get_a_tags(self, soup) -> None:
        links = soup.find_all("a")
        self.links = [link['href'] for link in links if link.has_attr('href')]
        self._normalize_links()

    def _normalize_links(self) -> None:
        """
        This method checks links to regular expression 'http' or 'https'
        """
        clean_links = []
        for i in self.links:
            if re.match(r'http', i):
                clean_links.append(i)
        self.links = clean_links

    def _validate_url(self):
        try:
            page = requests.get(self.url, headers=self.headers)
            return page
        except:
            return False
