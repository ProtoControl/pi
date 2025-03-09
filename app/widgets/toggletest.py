from kivymd.app import MDApp
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.screen import MDScreen


class MyToggleButton(MDFlatButton, MDToggleButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.background_down = self.theme_cls.primary_color


class Test(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        return (
            MDScreen(
                MDBoxLayout(
                    MyToggleButton(
                        text="Show ads",
                        group="x",
                    ),
                    MyToggleButton(
                        text="Do not show ads",
                        group="x",
                    ),
                    MyToggleButton(
                        text="Does not matter",
                        group="x",
                    ),
                    adaptive_size=True,
                    spacing="12dp",
                    pos_hint={"center_x": .5, "center_y": .5},
                ),
            )
        )


Test().run()