from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.spinner import Spinner
from kivymd.uix.textfield import MDTextField
from kivy.uix.textinput import TextInput

from kivymd.uix.button import MDButton, MDButtonText
import subprocess
from utils.platform_utils import PlatformUtils
from kivy.core.window import Window

platform_utils = PlatformUtils()
debug_mode = platform_utils.debug_mode

class WiFiScreen(MDScreen):
    def __init__(self, **kwargs):
        super(WiFiScreen, self).__init__(**kwargs)
        self.name = "wifi_screen"
        
        # Keep references for keyboard and layout
        self.keyboard = None
        self.keyboard_layout = None

        # Root layout
        self.root_layout = MDBoxLayout(orientation="vertical", spacing=10, padding=10)

        # Wi-Fi network selection
        self.network_spinner = Spinner(
            text="Select Network",
            values=self.get_wifi_networks(),  # Dynamically retrieved SSIDs
            size_hint=(1, 0.1),
            background_color = (2,0,0,1)
        )
        self.root_layout.add_widget(self.network_spinner)

        # Text input for password
        self.text_input = TextInput(
            hint_text="Enter password",
            password=True,
            size_hint=(1, 0.1),
            multiline=False,
            font_size=20
        )
        # Bind focus event so we know when the user clicks/taps the text input
        self.text_input.bind(focus=self.on_text_focus)
        self.root_layout.add_widget(self.text_input)

        # Button layout
        button_layout = MDBoxLayout(size_hint=(1, 0.1), spacing=10)

        # Cancel Button
        cancel_button = MDButton(MDButtonText(text="Cancel"), on_press=self.on_cancel)
        button_layout.add_widget(cancel_button)
        # Show/hide password button
        show_pwd = MDButton(MDButtonText(text="Show Password"), on_press=self.on_show)
        button_layout.add_widget(show_pwd)

        # Clear button
        clear_button = MDButton(MDButtonText(text="Clear"), on_press=self.on_clear)
        button_layout.add_widget(clear_button)

        # Connect button
        self.connect_button = MDButton(MDButtonText(text="Connect"), on_press=self.on_connect)
        button_layout.add_widget(self.connect_button)

        # Add button layout to root
        self.root_layout.add_widget(button_layout)

        # Add everything to this screen
        self.add_widget(self.root_layout)

    def get_wifi_networks(self):
        """Scans for available Wi-Fi networks."""
        if not debug_mode:
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
        else:
            return ["Debug mode - scan not available"]
    
    def on_cancel(self, instance):
        self.manager.current = "config_screen"
    def on_show(self, instance):
        """Handle showing/hiding password."""
        # Toggle password masking
        self.text_input.password = not self.text_input.password

    def on_clear(self, instance):
        """Clear the password field."""
        self.text_input.text = ""

    def on_connect(self, instance):
        """Attempt to connect to the selected Wi-Fi network with entered password."""
        selected_network = self.network_spinner.text
        password = self.text_input.text
        print(f"Connecting to {selected_network} with password: {password}")
        # Implement actual Wi-Fi connection logic here

    def on_text_focus(self, text_input, focused):
        """
        Triggered when the TextInput gets or loses focus.
        We only show the keyboard if it becomes focused (clicked/tapped).
        """
        if focused:
            # Show the on-screen keyboard
            self.show_keyboard()
        # Optionally, hide the keyboard when focus is lost:
        # else:
        #    self.hide_keyboard()

    def show_keyboard(self):
        """Create and show the docked VKeyboard with a Hide button."""
        # If keyboard is already shown, do nothing
        if self.keyboard:
            return

        # Container for the keyboard and the hide button
        # self.keyboard_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.8))
        # print(self.keyboard_layout.width, self.keyboard_layout.height)
        # Create the VKeyboard
        self.text_input.focused = True
        self.keyboard = Window.request_keyboard(None, self.root_layout)
        #self.keyboard = VKeyboard(size_hint=(1, 1.5))

        self.keyboard.bind(on_key_up=self.on_key_up)
        
        # 'Hide Keyboard' button
        # hide_btn = Button(text="Hide Keyboard", size_hint=(1, 0.2))
        # hide_btn.bind(on_press=self.hide_keyboard)

        # Add them to the keyboard layout
        #self.keyboard_layout.add_widget(self.keyboard)
        #self.keyboard_layout.add_widget(hide_btn)

        # Add the keyboard layout to the root layout
        #self.root_layout.add_widget(self.keyboard_layout)

    def hide_keyboard(self, *args):
        """Remove the keyboard layout from the screen."""
        if self.keyboard_layout:
            self.root_layout.remove_widget(self.keyboard_layout)
            self.keyboard_layout.remove_widget(self.keyboard)
            self.keyboard_layout = None
            self.keyboard = None

    def on_key_up(self, vkeyboard, keycode, *args):
        if keycode:
            text = keycode  # Extract key name
            if text == 'backspace':
                self.text_input.text = self.text_input.text[:-1]
            elif len(text) == 1:  # Ignore non-character keys
                self.text_input.text += text

