from kivy.uix.togglebutton import ToggleButton

class ToggleButtonWidget(ToggleButton):
    def __init__(self,id,text, **kwargs):
        super(ToggleButtonWidget, self).__init__(**kwargs)
        self.state = 'normal'
        self.id = id
        self.text = text

    def on_state(self, widget, value):
        message = f"{self.id},{value}"
        print(message)
        # if not debug_mode:
        #     ser.write(message.encode('utf-8'))
