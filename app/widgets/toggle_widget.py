from kivymd.uix.behaviors.toggle_behavior import ToggleButtonBehavior, MDToggleButton
from kivymd.uix.button import MDFabButton, MDButtonText
from utils.helpers import hex_to_rgba
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout

from kivymd.uix.selectioncontrol.selectioncontrol import MDSwitch

#box layout pulling from toggletest

class ToggleButtonWidget(MDBoxLayout):
    def __init__(self,id,text,color,scolor, **kwargs):
        super(ToggleButtonWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.value_label = MDLabel(
            text=text,  # Initial value
            size_hint=(1, None),
            height='40dp',  # Set a fixed height for the label
            halign="center"  # Center-align the text
        )
        self.switch = MDSwitch(
            icon_inactive = "close",
            icon_active = "check",
            icon_active_color = color,
            icon_inactive_color = scolor,
            track_color_active = color,
            track_color_inactive = scolor
        )
        self.state = 'normal'
        self.add_widget(self.value_label)
        self.add_widget(self.switch)
        # self.button_text = MDButtonText(text = text)
        # self.add_widget(self.button_text)
        # self.background_down = scolor
        # self.background_normal = color
        # self.id = id
        
    def on_state(self, widget, value):
        message = f"{self.id},{value}"
        print(message)
        # if not debug_mode:
        #     ser.write(message.encode('utf-8'))
