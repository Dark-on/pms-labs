from kivy.uix.screenmanager import ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from kivy.uix.image import AsyncImage
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import ILeftBody, MDList, ThreeLineAvatarListItem, ImageLeftWidget
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.spinner import MDSpinner

from src.books_provider import Book, BooksProvider
from config import Config


Builder.load_file(f"{Config.TEMPLATES_DIR}/bookstab.kv")


class AsyncImageLeftWidget(ILeftBody, AsyncImage):
    pass


class BookAdderScreen(MDScreen):
    """Contains layout with functionality for adding new books to the list.

    Also contains toolbar with buttons for getting back to the books list
    and saving new book.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = MDBoxLayout(orientation="vertical")
        self.load_content()

        self.add_widget(self.layout)

    def load_content(self):
        self.layout.clear_widgets()

        toolbar = MDToolbar(type="top")
        toolbar.left_action_items = [["arrow-left", self.go_back]]
        toolbar.right_action_items = [["plus", self.add_book]]

        title_label = MDLabel(
            text="Title: ",
            halign="left",
            valign="top",
        )
        subtitle_label = MDLabel(
            text="Subtitle: ",
            halign="left",
            valign="top",
        )
        price_label = MDLabel(
            text="Price: ",
            halign="left",
            valign="top",
        )

        self.title_input = MDTextField()
        self.subtitle_input = MDTextField()
        self.price_input = MDTextField()

        self.layout.add_widget(toolbar)
        self.layout.add_widget(title_label)
        self.layout.add_widget(self.title_input)
        self.layout.add_widget(subtitle_label)
        self.layout.add_widget(self.subtitle_input)
        self.layout.add_widget(price_label)
        self.layout.add_widget(self.price_input)

    def go_back(self, touch):
        self.layout.clear_widgets()
        self.manager.transition.direction = "right"
        self.manager.switch_to(BooksTab.screens["books_list"])

    def add_book(self, touch):
        book = Book(
            title=self.title_input.text,
            subtitle=self.subtitle_input.text,
            price=self.price_input.text
        )
        BooksTab.screens["books_list"].books.append(book)
        books_list = BooksTab.screens["books_list"].books
        BooksTab.screens["books_list"].load_books_list(books_list)
        self.go_back(touch)


class MDScrollableLabel(ScrollView):
    """Label that can be scrolled if needed.

    By default, label from kivymd can't be scrolled.
    """

    def __init__(self, **kwargs):
        super().__init__(do_scroll_x=False, do_scroll_y=True)
        # This fields are needed to make scrolling available.
        label = MDLabel(**kwargs)
        label.text_size = (label.width, None)
        label.size_hint_y = None
        label.height = label.texture_size[1]
        label.minimum_height = label.height

        self.add_widget(label)


class BookInfoContent(MDBoxLayout):
    """Layout with detailed information about books"""

    def __init__(self, book, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        # Create big string with all information about book.
        text_info = (
            f"[color=#707070]Title:[/color] {book.details.title}\n"
            f"[color=#707070]Subtitle:[/color] {book.details.subtitle}\n"
            f"[color=#707070]Descr:[/color] {book.details.description}\n\n"
            f"[color=#707070]Autors:[/color] {book.details.authors}\n"
            f"[color=#707070]Publisher:[/color] {book.details.publisher}\n\n"
            f"[color=#707070]Pages:[/color] {book.details.pages}\n"
            f"[color=#707070]Year:[/color] {book.details.year}\n"
            f"[color=#707070]Rating:[/color] {book.details.rating}/5\n"
        )
        # Create cover of the book
        cover = AsyncImage(source=book.details.image, size_hint_y=0.4)
        # Create label with text_info previously created.
        info = MDLabel(
            text=text_info,
            markup=True,
            halign="left",
            valign="top",
            size_hint_y=1
        )

        # Add book cover and detailed information to the layout
        self.add_widget(cover)
        self.add_widget(info)


class BookInfoScreen(MDScreen):
    """Contains layout with detailed information about the choosen
    book.

    Also containstoolbar with buttons for getting back to the books list
    and deleting the choosen book from the list.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        scroll_view = ScrollView()
        self.layout = MDBoxLayout(orientation="vertical", size_hint=(1, 1.2))
        scroll_view.add_widget(self.layout)
        self.add_widget(scroll_view)

    def load_screen(self, book):
        """Loads all elements for the detailed info.

        Created as separate method because on every book we need to reload the
        information.
        """
        self.book = book

        toolbar = MDToolbar(type="top")
        toolbar.left_action_items = [["arrow-left", self.go_back]]
        toolbar.right_action_items = [["delete", self.delete_item]]

        content = BookInfoContent(book)

        self.layout.add_widget(toolbar)
        self.layout.add_widget(content)

    def go_back(self, touch):
        self.layout.clear_widgets()
        self.manager.transition.direction = "right"
        self.manager.switch_to(BooksTab.screens["books_list"])

    def delete_item(self, touch):
        BooksTab.screens["books_list"].books.remove(self.book)
        books_list = BooksTab.screens["books_list"].books
        BooksTab.screens["books_list"].load_books_list(books_list)
        self.go_back(touch)


class BookListItem(ThreeLineAvatarListItem):
    """List item with the cover and short information about the book."""

    def __init__(self, book, **kwargs):
        super().__init__(text=book.title,
                         secondary_text=book.subtitle,
                         tertiary_text=f"Price: {book.price}", **kwargs)
        self.book = book

        image = AsyncImageLeftWidget(source=self.book.image)

        self.add_widget(image)

    def on_release(self):
        """Called when the user taps on the item and releases it"""
        BooksTab.screens["book_info"].load_screen(self.book)
        BooksTab.screen_manager.transition.direction = "left"
        BooksTab.screen_manager.switch_to(BooksTab.screens["book_info"])


class SearchField(MDTextField):
    """Input field that is used for searching books."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._is_first_run = True

    def make_search(self):
        """Called when user types some text."""
        # Need to skip this method for the first time, because without this
        # skip here will be an error. The first call happens on initialization
        # and not all fields are created for referencing.
        if self._is_first_run:
            self._is_first_run = False
            return
        found_books = BooksProvider.find_books(self.text)
        # Reloading books list on the screen with new filtered books
        BooksTab.screens["books_list"].load_books_list(found_books)


class BooksListScreen(MDScreen):
    """Screen, contains  the list of books with short information and the
    search bar.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # In this small block, books are generated from the json file.
        # (from the task)
        self.books = []

        add_book_button = MDFloatingActionButton(
            icon="plus",
            on_release=self.open_book_adder_screen
        )

        # Creating layout where all inner parts will be placed
        # (such as the foundation of the house)
        self.layout = MDBoxLayout(orientation="vertical")

        self.search_field = SearchField()
        self.spinner = MDSpinner(
            pos_hint={'center_x': .5, 'center_y': .5},
            size_hint=(0.03, 0.03)
        )
        self.spinner.active = False
        # ScrollView allows to scroll list that was put inside of whis view.
        # If there is no ScrollView, the user will not be able to see list
        # items that are outside of the screen.
        self.scroll_view = ScrollView()

        # Books are put in the books_list
        # (the book_list is put in the scroll_view, this is realized in the
        # `load_books_list` method)

        # Search field and scroll view are put into the layout
        self.layout.add_widget(self.search_field)
        self.layout.add_widget(self.scroll_view)

        # And the layout is put into this screen
        self.add_widget(self.layout)
        self.add_widget(add_book_button)

    def spinner_toggle(self):
        if self.spinner.active == False:
            self.layout.add_widget(self.spinner)
            self.spinner.active = True
        else:
            self.layout.remove_widget(self.spinner)
            self.spinner.active = False

    def load_books_list(self, books):
        """ Method that loads list of books to the screen.

        Separate method for loading the list is needed because when the book is
        deleted from the list, or when the user types something in searchbar,
        the list should be reloaded
        """
        self.spinner_toggle()
        # Clear all elements in the scroll view
        # (this elements are books list items)
        self.scroll_view.clear_widgets()

        # List will contain all books
        mdlist = MDList()

        # Add books to the list one by one
        for book in books:
            list_item_widget = BookListItem(book)
            mdlist.add_widget(list_item_widget)

        self.spinner_toggle()
        # Add list to the scroll view
        self.scroll_view.add_widget(mdlist)

    def open_book_adder_screen(self, touch):
        """Called when the user taps on the button and releases it"""
        BooksTab.screens["book_adder"].load_content()
        BooksTab.screen_manager.transition.direction = "left"
        BooksTab.screen_manager.switch_to(BooksTab.screens["book_adder"])


class BooksTab(MDBottomNavigationItem):
    """Tab that contains all elements related to books (from the lab task).

    It contains the screen with books list and the search bar. If you tap on
    the list item, it will open it in another screen with detailed information.
    Also this class contains screen_manager and screens fields as static fields
    because access to this fields is needed from different parts of
    the application.
    """

    screen_manager = None
    screens = None

    def __init__(self, **kwargs):
        # Giving main text and icon to this tab
        super().__init__(name="books", text="Books",
                         icon="book-multiple", **kwargs)

        # Screen manager is needed for switching between the screen with books
        # list and the screen with detailed information about choosen book.
        BooksTab.screen_manager = ScreenManager()
        # Here are created two screens that is used in BookTab.
        BooksTab.screens = {
            "books_list": BooksListScreen(name="books_list"),
            "book_info": BookInfoScreen(name="book_info"),
            "book_adder": BookAdderScreen(name="book_adder")
        }

        # Put created screens into Screen Manager.
        for screen in self.screens.values():
            BooksTab.screen_manager.add_widget(screen)

        # Put the screen manager into the our tab with books.
        self.add_widget(BooksTab.screen_manager)
