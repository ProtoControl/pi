import subprocess
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.vkeyboard import VKeyboard
from kivy.core.window import Window

Window.size = (800, 480)

class KeyboardApp(App):
    def build(self):
        # Root layout
        root = BoxLayout(orientation="vertical", spacing=10, padding=10)

        # Wi-Fi network selection
        self.network_spinner = Spinner(
            text="Select Network",
            values=self.get_wifi_networks(),
            size_hint=(1, 0.2)
        )
        root.add_widget(self.network_spinner)

        # Text input for password entry
        self.text_input = TextInput(
            hint_text="Enter password",
            password=True,  # Mask input for password
            size_hint=(1, 0.1),
            multiline=False,
            font_size=30
        )
        root.add_widget(self.text_input)

        # Virtual keyboard
        self.keyboard = VKeyboard(size_hint=(1, 0.5))
        self.keyboard.bind(on_key_up=self.on_key_up)
        root.add_widget(self.keyboard)

        # Button layout
        button_layout = BoxLayout(size_hint=(1, 0.1), spacing=10)

        # Show password button
        show_pwd = Button(text="Show Password", on_press=self.on_show)
        button_layout.add_widget(show_pwd)

        # Clear button
        clear_button = Button(text="Clear", on_press=self.on_clear)
        button_layout.add_widget(clear_button)

        # Connect button
        self.connect_button = Button(text="Connect", on_press=self.on_connect)
        button_layout.add_widget(self.connect_button)

        root.add_widget(button_layout)

        return root

    def get_wifi_networks(self):
        """Scans for available Wi-Fi networks."""
        try:
            # Run the iwlist command to scan for networks
            result = subprocess.run(
                ["sudo", "iwlist", "wlan0", "scan"],
                capture_output=True,
                text=True,
                check=True
            )
            # Parse output to extract unique SSIDs
            networks = set()  # Use a set to avoid duplicates
            for line in result.stdout.splitlines():
                if "ESSID" in line:
                    ssid = line.split(":")[1].strip('"')
                    if ssid:  # Ignore empty SSIDs
                        networks.add(ssid)
            return list(networks) if networks else ["No networks found"]
        except subprocess.CalledProcessError as e:
            print(f"Error scanning networks: {e}")
            return ["Error scanning"]

    def on_key_up(self, instance, keycode, *args):
        """Handles key release events from the virtual keyboard."""
        if keycode:
            text = keycode  # Extract key name
            if text == 'backspace':
                self.text_input.text = self.text_input.text[:-1]
            elif len(text) == 1:  # Ignore non-character keys
                self.text_input.text += text

    def on_connect(self, instance):
        """Handles the Connect button press."""
        selected_network = self.network_spinner.text
        entered_password = self.text_input.text

        if selected_network == "Select Network" or not selected_network:
            print("Please select a network.")
            return

        if not entered_password:
            print("Please enter a password.")
            return

        # Indicate that connection is in progress
        self.connect_button.text = "Connecting..."
        self.connect_button.disabled = True

        def connect():
            # Connect to Wi-Fi using nmcli
            try:
                result = subprocess.run(
                    ["sudo", "nmcli", "dev", "wifi", "connect", selected_network, "password", entered_password],
                    capture_output=True,
                    text=True,
                    check=True
                )
                print(f"Connected to {selected_network}: {result.stdout}")
                self.stop()
            except subprocess.CalledProcessError as e:
                print(f"Failed to connect to {selected_network}: {e.stderr}")
            finally:
                # Reset the button state
                self.connect_button.text = "Connect"
                self.connect_button.disabled = False

        # Run the connection process in a background thread to avoid blocking the UI
        from threading import Thread
        Thread(target=connect).start()

    def on_clear(self, instance):
        """Handles the Clear button press."""
        self.text_input.text = ""

    def on_show(self, instance):
        """Toggles password visibility."""
        self.text_input.password = not self.text_input.password


if __name__ == "__main__":
    KeyboardApp().run()
