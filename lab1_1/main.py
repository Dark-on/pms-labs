from kivymd.app import MDApp

from frontend import Frontend


class ProgrammaApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Lab1.1 IV-81 8111"

    def build(self):
        return Frontend()


if __name__ == "__main__":
    ProgrammaApp().run()
