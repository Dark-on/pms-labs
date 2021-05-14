from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.tab import MDTabsBase
# from kivy.properties import ObjectProperty

from src.data_provider import calculate_pos, calculate_size, calc_angle


Builder.load_file('templates/ui.kv')


class GraphScreen(MDBoxLayout, MDTabsBase):
    pass


class PieScreen(MDBoxLayout, MDTabsBase):

    def __init__(self, **kwargs):
        self.angles = calc_angle()
        super().__init__(**kwargs)


class UI(MDBoxLayout):
    def on_tab_switch(
        self, instance_tabs, instance_tab, instance_tab_label, tab_text
    ):
        '''
        Called when switching tabs.

        :type instance_tabs: <kivymd.uix.tab.MDTabs object>;
        :param instance_tab: <__main__.Tab object>;
        :param instance_tab_label: <kivymd.uix.tab.MDTabsLabel object>;
        :param tab_text: text or name icon of tab;
        '''
        # get the tab icon.
        count_icon = instance_tab.icon
        # print it on shell/bash.
        print(f"Welcome to {count_icon}' tab'")
