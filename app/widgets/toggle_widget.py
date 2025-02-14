from kivymd.uix.behaviors.toggle_behavior import ToggleButtonBehavior
from kivymd.uix.button import MDFabButton

class ToggleButtonWidget(MDFabButton, ToggleButtonBehavior):
    def __init__(self,id,text, **kwargs):
        print("Test")
        print(dict(**kwargs))
        super(ToggleButtonWidget, self).__init__(**kwargs)
        self.state = 'normal'
        self.id = id
        self.text = text

    def on_state(self, widget, value):
        message = f"{self.id},{value}"
        print(message)
        # if not debug_mode:
        #     ser.write(message.encode('utf-8'))
