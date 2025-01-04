from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window

class WifiLoginScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(WifiLoginScreen, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 20
        self.spacing = 10

        # Add a label
        self.add_widget(Label(text="Enter Wi-Fi Password", font_size=24, size_hint=(1, 0.2)))

        # TextInput for password entry
        self.password_input = TextInput(
            password=True,
            multiline=False,
            size_hint=(1, 0.2),
            font_size=20,
        )
        self.add_widget(self.password_input)

        # Submit button
        submit_btn = Button(
            text="Connect",
            size_hint=(1, 0.2),
            font_size=20,
        )
        submit_btn.bind(on_release=self.submit_password)
        self.add_widget(submit_btn)

        # Add a button to clear the input
        clear_btn = Button(
            text="Clear",
            size_hint=(1, 0.2),
            font_size=20,
        )
        clear_btn.bind(on_release=self.clear_input)
        self.add_widget(clear_btn)

    def submit_password(self, instance):
        # Handle the submitted password
        password = self.password_input.text
        print(f"Password entered: {password}")
        # Logic to connect to Wi-Fi can be added here

    def clear_input(self, instance):
        self.password_input.text = ""


class WifiLoginApp(App):
    def build(self):
        # Enable the virtual keyboard for the app
        Window.softinput_mode = "pan"
        return WifiLoginScreen()


if __name__ == "__main__":
    WifiLoginApp().run()
