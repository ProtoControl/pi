from kivymd.uix.behaviors.toggle_behavior import ToggleButtonBehavior
from kivymd.uix.button import MDFabButton
from utils.helpers import hex_to_rgba


class ToggleButtonWidget(MDFabButton, ToggleButtonBehavior):
    def __init__(self,id,text, **kwargs):
        print("Test")
        print(dict(**kwargs))
        super(ToggleButtonWidget, self).__init__(**kwargs)
        self.state = 'normal'
        self.background_down = hex_to_rgba(kwargs.get("primaryColor","#00FF00"))
        self.background_normal = hex_to_rgba(kwargs.get("secondaryColor","#FF0000"))  
        self.id = id
        self.text = text

    def on_state(self, widget, value):
        message = f"{self.id},{value}"
        print(message)
        # if not debug_mode:
        #     ser.write(message.encode('utf-8'))
