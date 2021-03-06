"""Module that contains everything for the application UI.

Please, read documentation from the bottom of the file to the top
"""

from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.bottomnavigation import MDBottomNavigation

from config import Config
from src.ui.personaltab import PersonalTab
from src.ui.graphtab import GraphTab
from src.ui.bookstab import BooksTab
from src.ui.imagecollectiontab import ImageCollectionTab


Builder.load_file(f"{Config.TEMPLATES_DIR}/ui.kv")


class UI(MDScreen):
    """Main application screen. Contains all elements in the app."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create bottom navigaton bar that contains all tabs from our app.
        self.tabs_navigation = MDBottomNavigation()

        # List of tabs that will be displayed in the app
        self.tabs = (
            PersonalTab(),
            GraphTab(),
            BooksTab(),
            ImageCollectionTab(),
        )
        for tab in self.tabs:
            self.tabs_navigation.add_widget(tab)

        self.add_widget(self.tabs_navigation)
