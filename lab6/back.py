from random import random
from kivy.app import App 
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle
from kivy.uix.filechooser import FileChooserListView, FileChooserIconView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image


class MyBackground(Widget):
    def __init__(self, **kwargs):
        super(MyBackground, self).__init__(**kwargs)
        with self.canvas:
            self.bg = Rectangle(source='water.png', pos=self.pos, size=self.size)

        self.bind(pos=self.update_bg)
        self.bind(size=self.update_bg)

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size


class MyPaintWidget(Widget):
    def on_touch_down(self, touch):
        color = (random(), random(), random())
        with self.canvas:
            Color(*color)
            d = 30.
            touch.ud['line'] = Line(points=(touch.x, touch.y))

    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]

class MyPaintApp(App):
    def build(self):
        parent = MyBackground()
        painter = MyPaintWidget()
        parent.add_widget(painter)
        return parent

if __name__ == '__main__':
    MyPaintApp().run()

class MyPaintApp(App):
    def build(self):
        return MyPaintWidget()