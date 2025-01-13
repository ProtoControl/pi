from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle


from prog import MyApp
from wifi import KeyboardApp
keyboard_app = KeyboardApp()
my_app = MyApp()
# Style settings
Window.size = (800, 400)  # Simulate 800x400 resolution
Window.clearcolor = (1, 1, 1, 1)  # White background


class GrayBox(BoxLayout):
    """
    A simple BoxLayout that draws a gray rectangle behind its contents.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.9, 0.9, 0.9, 1)  # Slightly darker gray
            self.rect = Rectangle(size=self.size, pos=self.pos)
        # Update the rectangle whenever the layout changes size/position
        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class ConfigPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Main layout: horizontal split (left vs. right)
        self.orientation = 'horizontal'
        self.spacing = 10
        self.padding = 10

        # -------------------------------
        # LEFT SIDE: Device Info (top) + Buttons (bottom)
        # -------------------------------
        left_layout = BoxLayout(orientation='vertical', spacing=10, size_hint=(0.3, 1))

        # 1) Device Info in a GrayBox at the top
        #    We use size_hint_y=None and bind minimum_height for auto-size
        device_info_container = GrayBox(orientation='vertical', size_hint=(1, 3), padding=10, spacing=5)
        
        # Put device info in a small GridLayout inside the gray box
        device_info_box = GridLayout(cols=1, spacing=5, size_hint_y=3)
        

        device_info_box.add_widget(Label(
            text="Device Info",
            font_size="20sp",
            bold=True,
            color=(0, 0, 0, 1)
        ))
        device_info_box.add_widget(Label(text="Name: MyDevice", color=(0, 0, 0, 1)))
        device_info_box.add_widget(Label(text="Serial: 1234567890", color=(0, 0, 0, 1)))
        device_info_box.add_widget(Label(text="Firmware: v1.0.0", color=(0, 0, 0, 1)))

        device_info_container.add_widget(device_info_box)
        left_layout.add_widget(device_info_container)

        # 2) Filler to push buttons to the bottom
        filler_box = BoxLayout(size_hint=(1, 1))
        left_layout.add_widget(filler_box)

        # 3) Buttons at the bottom (Connect above Cancel)
        buttons_layout = BoxLayout(orientation='vertical', spacing=10, size_hint=(1, None))

        wifi_button = Button(
            text="Connect to Wi-Fi",
            size_hint=(1, None),
            height=50,
            background_color=(0, 0, 0, 1),
            color=(1, 1, 1, 1),
            background_down='atlas://data/images/defaulttheme/button_pressed'  # Simple press animation
        )
        wifi_button.bind(on_press=self.launch_keyboard_app)
        buttons_layout.add_widget(wifi_button)

        cancel_button = Button(
            text="Cancel",
            size_hint=(1, None),
            height=50,
            background_color=(0, 0, 0, 1),
            color=(1, 1, 1, 1),
            background_down='atlas://data/images/defaulttheme/button_pressed'  # Simple press animation
        )
        cancel_button.bind(on_press=self.exit_app)
        buttons_layout.add_widget(cancel_button)

        left_layout.add_widget(buttons_layout)

        # Add complete left_layout to the main layout
        self.add_widget(left_layout)

        # -------------------------------
        # RIGHT SIDE: Serial Console
        # -------------------------------
        right_layout = BoxLayout(orientation='vertical', spacing=10, size_hint=(0.7, 1))

        console_label = Label(
            text="Serial Console",
            font_size="20sp",
            bold=True,
            color=(0, 0, 0, 1),
            size_hint=(1, None),
            height=30
        )
        right_layout.add_widget(console_label)

        self.console_scroll = ScrollView(size_hint=(1, 5))
        self.console_output = TextInput(
            readonly=True,
            multiline=True,
            background_color=(0.9, 0.9, 0.9, 1),
            foreground_color=(0, 0, 0, 1),
            size_hint_y=None,
        )
        # Let the text input grow if needed, but remain scrollable:
        self.console_output.bind(minimum_height=self.console_output.setter('height'))
        self.console_scroll.add_widget(self.console_output)
        right_layout.add_widget(self.console_scroll)

        # Add right side to main layout
        self.add_widget(right_layout)

    def launch_keyboard_app(self, instance):
        # Launch KeyboardApp (Replace with actual app launch logic)
        keyboard_app.run()

    def exit_app(self, instance):
        App.get_running_app().stop()
        my_app.run()

class ConfigPanelApp(App):
    def build(self):
        return ConfigPanel()

if __name__ == "__main__":
    ConfigPanelApp().run()
