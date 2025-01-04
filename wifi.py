from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.vkeyboard import VKeyboard


class KeyboardApp(App):
    def build(self):
        # Root layout
        root = BoxLayout(orientation="vertical", spacing=10, padding=10)

        # Text input for password entry
        self.text_input = TextInput(
            hint_text="Enter password",
            password=True,  # Mask input for password
            size_hint=(1, 0.2),
            multiline=False
        )
        root.add_widget(self.text_input)

        # Virtual keyboard
        self.keyboard = VKeyboard(
            size_hint=(1, 0.5),
            on_key_down=self.on_key_down
        )
        root.add_widget(self.keyboard)

        # Button layout
        button_layout = BoxLayout(size_hint=(1, 0.3), spacing=10)

        # Connect button
        connect_button = Button(text="Connect", on_press=self.on_connect)
        button_layout.add_widget(connect_button)

        # Clear button
        clear_button = Button(text="Clear", on_press=self.on_clear)
        button_layout.add_widget(clear_button)

        root.add_widget(button_layout)

        return root

    def on_key_down(self, instance, keycode, text, modifiers):
        """Handles keypress events on the virtual keyboard."""
        if text:
            self.text_input.text += text
        elif keycode[1] == 'backspace':
            self.text_input.text = self.text_input.text[:-1]

    def on_connect(self, instance):
        """Handles the Connect button press."""
        entered_text = self.text_input.text
        print(f"Entered password: {entered_text}")

    def on_clear(self, instance):
        """Handles the Clear button press."""
        self.text_input.text = ""


if __name__ == "__main__":
    KeyboardApp().run()
