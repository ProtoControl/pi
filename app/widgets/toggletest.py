from kivymd.app import MDApp
from kivymd.uix.behaviors.toggle_behavior import MDToggleButtonBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.selectioncontrol.selectioncontrol import MDSwitch

class MyToggleButton(MDSwitch):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        kwargs["primaryColor"] = "red"
        kwargs["secondaryColor"] = "blue"
        self.icon_inactive = "close"
        self.icon_active_color = kwargs.get("primaryColor", [1, 1, 1, 1])
        self.icon_inactive_color = kwargs.get("secondaryColor", [1, 1, 1, 1])
        self.track_color_active = kwargs.get("primaryColor", [1, 1, 1, 1])
        self.track_color_inactive = kwargs.get("secondaryColor", [1, 1, 1, 1])
        
        self.icon_active = "check"
        self.ripple_effect = False
class Test(MDApp):
    def build(self):
        #self.theme_cls.theme_style = "Dark"
        #self.theme_cls.primary_palette = "Orange"
        return (
            MDScreen(
                MDBoxLayout(
                    MyToggleButton(

                    ),
                    adaptive_size=True,
                    spacing="12dp",
                    pos_hint={"center_x": .5, "center_y": .5},
                ),
            )
        )


Test().run()