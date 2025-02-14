from kivymd.uix.button import MDButton, MDButtonText

class PushButton(MDButton):
    def __init__(self, text, id, size_hint, color = (1,1,1,1), **kwargs):
        super(PushButton, self).__init__(**kwargs)
        self.button_text = MDButtonText(text=text)
        self.add_widget(self.button_text)
        self.background_color = color
        self.id = id
        #self.style = "filled"
        self.size_hint = size_hint

    def on_press(self):
        message = f"{self.id},1"
        print(message)
        # if not debug_mode:
        #     ser.write(message.encode('utf-8'))
