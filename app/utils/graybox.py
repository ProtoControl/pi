from kivymd.uix.boxlayout import MDBoxLayout
from kivy.graphics import Color, Rectangle

class GrayBox(MDBoxLayout):
    """A simple BoxLayout that draws a gray rectangle behind its contents."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.9, 0.9, 0.9, 1)
            #self.rect = Rectangle(size=self.size, pos=self.pos)
        #self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
