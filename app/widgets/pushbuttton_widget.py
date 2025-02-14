from kivymd.uix.button import MDButton, MDButtonText

class PushButton(MDButton):
    def __init__(self, text, id, color = (1,1,1,1), **kwargs):
        super(PushButton, self).__init__(**kwargs)
        self.text = MDButtonText(text=text)
        self.background_color = color
        self.id = id

    def on_press(self):
        message = f"{self.id},1"
        print(message)
        # if not debug_mode:
        #     ser.write(message.encode('utf-8'))
