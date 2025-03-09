from kivymd.uix.behaviors.toggle_behavior import ToggleButtonBehavior, MDToggleButton
from kivymd.uix.button import MDFabButton, MDButtonText
from utils.helpers import hex_to_rgba
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton




class ToggleButtonWidget(MDFabButton,MDToggleButton):
    def __init__(self,id,text,color,scolor, **kwargs):
        print("Test")
        print(dict(**kwargs))
        super(ToggleButtonWidget, self).__init__(**kwargs)
        self.theme_bg_color = "Custom"
        self.md_bg_color = color
        self.state = 'normal'
        self.button_text = MDButtonText(text = text)
        self.add_widget(self.button_text)
        self.background_down = scolor
        self.background_normal = color
        self.id = id
        
    def on_state(self, widget, value):
        message = f"{self.id},{value}"
        print(message)
        # if not debug_mode:
        #     ser.write(message.encode('utf-8'))
