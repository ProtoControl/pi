from kivymd.uix.button import MDButton, MDButtonText

class PushButton(MDButton):
    def __init__(self, text, id, size_hint, scolor, color, **kwargs):
        super(PushButton, self).__init__(**kwargs)
        self.button_text = MDButtonText(text=text, text_color = color,theme_text_color = "Custom")
        self.add_widget(self.button_text)
        self.line_color = color
        #self.shadow_color = color
        self.theme_bg_color = "Custom"
        self.md_bg_color = scolor
        self.id = id
        #self.style = "filled"
        self.size_hint = size_hint
        self.theme_color = "Custom"  

    def on_press(self):
        message = f"{self.id},1"
        print(message)
        # if not debug_mode:
        #     ser.write(message.encode('utf-8'))
