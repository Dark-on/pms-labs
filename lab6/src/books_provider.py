import json
import requests
from urllib.parse import quote, urljoin


class BooksProvider:
    __slots__ = ()

    SEARCH_URL = "https://api.itbook.store/1.0/search/"
    DETAILED_INFO_URL = "https://api.itbook.store/1.0/books/"

    @classmethod
    def find_books(cls, query):
        filtered_query = quote(query)
        url = urljoin(cls.SEARCH_URL, filtered_query)
        json_response = requests.get(url).json()
        if json_response["error"] != "0":
            return []
        books = []
        for json_book in json_response["books"]:
            books.append(Book(**json_book))
        return books

    @classmethod
    def load_details(cls, isbn13):
        json_response = requests.get(f"{cls.DETAILED_INFO_URL}{isbn13}").json()
        if json_response["error"] != "0":
            return

        return json_response


class Book:
    def __init__(self, title=None, subtitle=None, isbn13=None,
                 price=None, image=None, url=None):
        self.title = title or ""
        self.subtitle = subtitle or ""
        self.isbn13 = isbn13 or ""
        self.price = price or ""
        self.image = image
        self.url = url

        self._details_loaded = False

    @property
    def details(self):
        if not self._details_loaded:
            details_dict = BooksProvider.load_details(self.isbn13)
            if details_dict:
                self._details = self.BookDetails(**details_dict)
            else:
                self._details = self.BookDetails()
            self._details_loaded = True
        return self._details

    def reload_details(self):
        self._details_loaded = False

    class BookDetails:
        def __init__(self, title=None, subtitle=None, isbn13=None,
                     price=None, image=None, authors=None, publisher=None,
                     pages=None, year=None, rating=None, desc=None, url=None,
                     isbn10=None, language=None, **kwargs):
            self.title = title or ""
            self.subtitle = subtitle or ""
            self.isbn13 = isbn13 or ""
            self.price = price or ""
            self.authors = authors or ""
            self.publisher = publisher or ""
            self.pages = pages or ""
            self.year = year or ""
            self.rating = rating or ""
            self.description = desc or ""
            self.image = image
            self.url = url or ""
            self.language = language or ""
            self.isbn10 = isbn10 or ""

