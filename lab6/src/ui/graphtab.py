from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.bottomnavigation import MDBottomNavigationItem

from config import Config


Builder.load_file(f"{Config.TEMPLATES_DIR}/graphtab.kv")


class GraphTab(MDBottomNavigationItem):
    """Tab that contains personal information."""

    def __init__(self, **kwargs):
        # Giving main text and icon to this tab
        super().__init__(name="graph", text="Graph",
                         icon="graphql", **kwargs)

        layout = MDBoxLayout(orientation="vertical")

        self.add_widget(layout)
