import json


class BooksProvider:
    __slots__ = ()

    BOOKS_FILE = "data/books_info/books_list.json"
    DETAILS_FOLDER = "data/books_info/details/"
    IMAGES_FOLDER = "data/books_info/images/"

    @staticmethod
    def load_books_from_json():
        with open(BooksProvider.BOOKS_FILE, 'r') as bf:
            books_json = json.load(bf)
        return books_json["books"]

    @staticmethod
    def load_details_from_json(isbn13):
        try:
            with open(f"{BooksProvider.DETAILS_FOLDER}/{isbn13}.txt") as df:
                details_json = json.load(df)
        except FileNotFoundError:
            return
        return details_json


class Book:
    def __init__(self, title=None, subtitle=None, isbn13=None,
                 price=None, image=None):
        self.title = title or ""
        self.subtitle = subtitle or ""
        self.isbn13 = isbn13 or ""
        self.price = price or ""
        self.image_path = "data/books_info/images/default.png"
        if image:
            self.image_path = f"data/books_info/images/{image}"

        self._details_loaded = False

    @property
    def details(self):
        if not self._details_loaded:
            details_dict = BooksProvider.load_details_from_json(self.isbn13)
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
                     pages=None, year=None, rating=None, desc=None):
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
            self.image_path = "data/books_info/images/default.png"
            if image:
                self.image_path = f"data/books_info/images/{image}"
