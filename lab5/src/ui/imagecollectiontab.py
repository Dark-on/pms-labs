import os

from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.imagelist import SmartTile
from kivy.uix.scrollview import ScrollView
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.filemanager import MDFileManager
from config import Config


Builder.load_file(f"{Config.TEMPLATES_DIR}/imagecollectiontab.kv")


class ImageCell(SmartTile):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.box_color = (0, 0, 0, 0)


class ImageGrid(MDGridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.padding = (dp(0), dp(0))
        self.spacing = dp(4)

    def get_free_cell(self):
        for image in self.images:
            if not image.source:
                return image
        return

    def add_image_cells(self):
        for image in self.images:
            self.add_widget(image)


class ThreeVerticalImagesGrid(ImageGrid):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.rows = 3
        self.size_hint = (0.2, 0.67)
        self.images = (ImageCell(), ImageCell(), ImageCell())
        self.add_image_cells()


class BigImageGrid(ImageGrid):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.rows = 1
        self.size_hint = (0.6, 0.67)
        self.images = (ImageCell(),)
        self.add_image_cells()


class BlockOfImages(ImageGrid):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._current_grid = None

        self._first_col_grid = None
        self._middle_block_grid = None
        self._last_col_grid = None

        self.rows = 1
        self.size_hint = (1, 0.5)

        self.images = []
        self.padding = (dp(2), dp(2))
        self._make_new_grid()

    def _to_next_grid(self):
        if self._current_grid == self._first_col_grid:
            self._current_grid = self._middle_block_grid
        elif self._current_grid == self._middle_block_grid:
            self._current_grid = self._last_col_grid
        elif self._current_grid == self._last_col_grid:
            self._make_new_grid()

    def get_free_cell(self):
        if self._last_col_grid.children[0].source:
            return
        image = self._current_grid.get_free_cell()
        if not image:
            self._to_next_grid()
            image = self._current_grid.get_free_cell()
        return image

    def _make_new_grid(self):
        self._first_col_grid = ThreeVerticalImagesGrid()
        self._middle_block_grid = BigImageGrid()
        self._last_col_grid = ThreeVerticalImagesGrid()

        self.add_widget(self._first_col_grid)
        self.add_widget(self._middle_block_grid)
        self.add_widget(self._last_col_grid)

        self._current_grid = self._first_col_grid


class ImageGridBuilder(MDGridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.blocks = [BlockOfImages(), BlockOfImages(), BlockOfImages()]
        self._idx = 0
        self._current_block = self.blocks[self._idx]
        self.cols = 1
        self.size_hint = (1, 1.5)

        for block in self.blocks:
            self.add_widget(block)

    def _to_next_block(self):
        self._idx += 1
        self._current_block = self.blocks[self._idx]

    def add_image(self, source):
        image = self._current_block.get_free_cell()
        if not image:
            self._to_next_block()
            image = self._current_block.get_free_cell()
        image.source = source


class ImageChooser(MDFileManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.exit_manager = self.exit
        self.preview = False
        self.external_storage = os.getenv('EXTERNAL_STORAGE')
        self.images_folder = f"{self.external_storage}/Pictures"

    def select_path(self, path):
        ImageCollectionTab.image_collection.builder.add_image(path)
        self.exit()

    def exit(self, *args):
        self.close()

    def open(self):
        self.show(self.images_folder)


class ImageCollection(MDGridLayout):
    def __init__(self, **kwargs):
        super().__init__(cols=1, **kwargs)

        self.__next_image_index = 0

        self.add_image_button = MDFloatingActionButton(
            icon="plus",
            on_release=self.open_image_chooser
        )

        self.scroll_view = ScrollView(size_hint=(1, 1))

        self.builder = ImageGridBuilder()

        self.scroll_view.add_widget(self.builder)
        self.add_widget(self.scroll_view)
        self.add_widget(self.add_image_button)

    def open_image_chooser(self, touch):
        ImageCollectionTab.image_chooser.open()


class ImageCollectionTab(MDBottomNavigationItem):
    """Tab that contains personal information."""

    image_chooser = None
    image_collection = None
    x_size = None

    def __init__(self, **kwargs):
        super().__init__(name="img_collection", text="Images",
                         icon="image-frame", **kwargs)

        ImageCollectionTab.x_size = self.size[0]
        ImageCollectionTab.image_collection = ImageCollection()
        ImageCollectionTab.image_chooser = ImageChooser()

        self.add_widget(ImageCollectionTab.image_collection)
