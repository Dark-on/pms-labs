from kivy.lang import Builder
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.bottomnavigation import MDBottomNavigationItem

from config import Config


Builder.load_file(f"{Config.TEMPLATES_DIR}/personaltab.kv")


class PersonalTab(MDBottomNavigationItem):
    """Tab that contains personal information."""

    def __init__(self, **kwargs):
        # Giving main text and icon to this tab
        super().__init__(name="general", text="General",
                         icon="bookmark-outline", **kwargs)

        layout = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        layout.height = layout.minimum_height

        personal_info = MDLabel(
            font_style="Body1",
            theme_text_color="Primary",
            text="Дрозд Світлана\nГрупа ІВ-81\nЗК ІВ-8111",
            halign="center"
        )

        layout.add_widget(personal_info)
        self.add_widget(layout)
