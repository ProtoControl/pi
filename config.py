from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.core.window import Window

# Style settings
Window.size = (800, 400)  # Simulate 800x400 resolution
Window.clearcolor = (1, 1, 1, 1)  # White background


class ConfigPanel(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.spacing = 10
        self.padding = 10

        # Top Section: Device Info
        device_info_layout = GridLayout(cols=2, size_hint=(1, 0.3), spacing=5)
        device_info_layout.add_widget(Label(text="Device Info", font_size="20sp", bold=True, color=(0, 0, 0, 1)))
        device_info_layout.add_widget(Label(text=""))  # Empty for alignment
        device_info_layout.add_widget(Label(text="Name:", color=(0, 0, 0, 1)))
        device_info_layout.add_widget(Label(text="MyDevice", color=(0, 0, 0, 1)))
        device_info_layout.add_widget(Label(text="Serial Number:", color=(0, 0, 0, 1)))
        device_info_layout.add_widget(Label(text="1234567890", color=(0, 0, 0, 1)))
        device_info_layout.add_widget(Label(text="Firmware:", color=(0, 0, 0, 1)))
        device_info_layout.add_widget(Label(text="v1.0.0", color=(0, 0, 0, 1)))
        self.add_widget(device_info_layout)

        # Middle Section: Buttons
        button_layout = GridLayout(cols=2, size_hint=(1, 0.3), spacing=10)
        wifi_button = Button(text="Connect to Wi-Fi", background_color=(0, 0, 0, 1), color=(1, 1, 1, 1))
        wifi_button.bind(on_press=self.launch_keyboard_app)
        button_layout.add_widget(wifi_button)

        cancel_button = Button(text="Cancel", background_color=(0, 0, 0, 1), color=(1, 1, 1, 1))
        cancel_button.bind(on_press=self.exit_app)
        button_layout.add_widget(cancel_button)
        self.add_widget(button_layout)

        # Bottom Section: Serial Console
        console_layout = GridLayout(cols=1, size_hint=(1, 0.4))
        console_label = Label(text="Serial Console", font_size="20sp", bold=True, color=(0, 0, 0, 1))
        console_layout.add_widget(console_label)

        self.console_scroll = ScrollView(size_hint=(0.25, 1), size=(200, 100), pos_hint={"x": 0.75, "y": 0})
        self.console_output = TextInput(size_hint=(None, None), size=(200, 100),
                                        readonly=True, multiline=True,
                                        background_color=(0.9, 0.9, 0.9, 1), foreground_color=(0, 0, 0, 1))
        self.console_scroll.add_widget(self.console_output)
        console_layout.add_widget(self.console_scroll)
        self.add_widget(console_layout)

        # Simulate UART Traffic
        Clock.schedule_interval(self.simulate_uart, 2)

    def launch_keyboard_app(self, instance):
        # Launch KeyboardApp (Replace with actual app launch logic)
        print("Launching KeyboardApp...")

    def exit_app(self, instance):
        App.get_running_app().stop()

    def simulate_uart(self, dt):
        # Simulate UART traffic by appending random messages
        self.console_output.text += "UART Message: Hello, UART!\n"
        self.console_output.cursor = (len(self.console_output.text), 0)  # Keep scroll at the bottom


class ConfigPanelApp(App):
    def build(self):
        return ConfigPanel()


if __name__ == "__main__":
    ConfigPanelApp().run()
