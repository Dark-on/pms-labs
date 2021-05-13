from kivymd.app import MDApp

from frontend import Frontend

class Lab1_2App(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Drozd Svitlana IV-81"

    def build(self):
        return Frontend()


if __name__ == "__main__":
    Lab1_2App().run()
