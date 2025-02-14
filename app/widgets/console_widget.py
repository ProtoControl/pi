from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField

class ConsoleWidget(BoxLayout):
    def __init__(self, text, id, **kwargs):
        super(ConsoleWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'
        
        self.label = MDLabel(text=text, size_hint=(1, 0.1), font_size='18sp')
        self.id = id

        self.content = MDTextField(
            multiline=True,
            readonly=True,
            font_size='16sp',
            size_hint=(1, 0.9),
            background_color=[0, 0, 0, 1],
            foreground_color=[1, 1, 1, 1]
        )
        
        self.add_widget(self.label)
        self.add_widget(self.content)

    def write_to_console(self, text):
        self.content.text = f"{text}\n"
