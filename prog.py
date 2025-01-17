#!/usr/bin/env python

import sys
import platform
import subprocess
import requests

# Kivy imports
import kivy
kivy.require('2.1.0')
from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'dock')
# More config settings to explore
#https://kivy.org/doc/stable/api-kivy.config.html
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.slider import Slider
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Rectangle, Color
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.spinner import Spinner
from kivy.uix.vkeyboard import VKeyboard
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition

from code import generate_alphanumeric_code

from PushButton import PushButton

debug_mode = '-d' in sys.argv
Window.size = (800, 480)

if platform.system() == 'Windows' or platform.system() == 'Darwin':
    print("Running on Windows or stupid stupid mac")
    debug_mode = True  # Automatically enable debug mode on Windows
else:
    print("Running on a non-Windows system")
    print(debug_mode)
    print(sys.argv)

# If you need RPi GPIO and serial in production:
if not debug_mode and platform.system() == 'Linux':
    import serial
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# ---- Shared Functions and Classes ----
def hex_to_rgba(hex_color):
    # Remove the '#' if present
    hex_color = hex_color.lstrip('#')
    
    if len(hex_color) not in (6, 8):
        raise ValueError("Hex color must be in the format '#RRGGBB' or '#RRGGBBAA'")
    
    r = int(hex_color[0:2], 16) / 255
    g = int(hex_color[2:4], 16) / 255
    b = int(hex_color[4:6], 16) / 255
    a = int(hex_color[6:8], 16) / 255 if len(hex_color) == 8 else 1
    return (r, g, b, a)


class ToggleButtonWidget(ToggleButton):
    def __init__(self,id,text, **kwargs):
        super(ToggleButtonWidget, self).__init__(**kwargs)
        self.state = 'normal'
        self.id = id
        self.text = text

    def on_state(self, widget, value):
        message = f"{self.id},{value}"
        print(message)
        # if not debug_mode:
        #     ser.write(message.encode('utf-8'))

class SliderWidget(BoxLayout):
    def __init__(self, text, min, max, id,**kwargs):
        super(SliderWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'

        self.slider = Slider(min=min, max=max, value=min)
        self.slider.orientation = 'horizontal'
        self.slider.value_track = True
        self.slider.value_track_color = [1, 0, 0, 1]
        self.slider.text = text
        self.slider.min = min
        self.slider.max = max
        self.slider.id = id

        self.value_label = Label(text=f"{text}", size_hint=(1, 0.2), font_size='40sp')
        self.slider.bind(value=self.on_value_change)

        self.add_widget(self.value_label)
        self.add_widget(self.slider)

    def on_value_change(self, instance, value):
        rounded_value = round(value, 2)
        message = f"{self.slider.id},{rounded_value}"
        print(message)
        # if not debug_mode:
        #     ser.write(message.encode('utf-8'))
        self.value_label.text = f"{self.slider.text}: {rounded_value}"

class ConsoleWidget(BoxLayout):
    def __init__(self, text, id, **kwargs):
        super(ConsoleWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'
        
        self.label = Label(text=text, size_hint=(1, 0.1), font_size='18sp')
        self.id = id

        self.content = TextInput(
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

# ---- Screen 1: Config Panel ----
class GrayBox(BoxLayout):
    """A simple BoxLayout that draws a gray rectangle behind its contents."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.9, 0.9, 0.9, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class ConfigScreen(Screen):
    def __init__(self, **kwargs):
        super(ConfigScreen, self).__init__(**kwargs)
        self.name = "config_screen"  # ScreenManager reference name

        main_layout = BoxLayout(orientation='horizontal', spacing=10, padding=10)

        # LEFT SIDE
        left_layout = BoxLayout(orientation='vertical', spacing=10, size_hint=(0.3, 1))
        
        # Device Info
        device_info_container = GrayBox(orientation='vertical', size_hint=(1, 3), padding=10, spacing=5)
        device_info_box = GridLayout(cols=1, spacing=5, size_hint_y=3)

        #Code generation
        self.code = generate_alphanumeric_code()
        device_info_box.add_widget(Label(
            text="Device Info",
            font_size="20sp",
            bold=True,
            color=(0, 0, 0, 1)
        ))
        device_info_box.add_widget(Label(text="Name: MyDevice", color=(0, 0, 0, 1)))
        device_info_box.add_widget(Label(text=f"Registration Code: {self.code}", color=(0, 0, 0, 1)))
        device_info_box.add_widget(Label(text="Firmware: v1.0.0", color=(0, 0, 0, 1)))

        device_info_container.add_widget(device_info_box)
        left_layout.add_widget(device_info_container)

        filler_box = BoxLayout(size_hint=(1, 1))
        left_layout.add_widget(filler_box)

        # Buttons
        buttons_layout = BoxLayout(orientation='vertical', spacing=10, size_hint=(1, None))

        wifi_button = Button(
            text="Connect to Wi-Fi",
            size_hint=(1, None),
            height=50,
            background_color=(0, 0, 0, 1),
            color=(1, 1, 1, 1),
        )
        wifi_button.bind(on_press=self.launch_wifi_screen)
        buttons_layout.add_widget(wifi_button)

        cancel_button = Button(
            text="Cancel",
            size_hint=(1, None),
            height=50,
            #background_color=(0, 0, 0, 1),
            color=(1, 1, 1, 1),
        )
        cancel_button.bind(on_press=self.launch_my_app_screen)
        buttons_layout.add_widget(cancel_button)

        left_layout.add_widget(buttons_layout)

        main_layout.add_widget(left_layout)

        # RIGHT SIDE: Serial Console
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
            size_hint_y=None
        )
        self.console_output.bind(minimum_height=self.console_output.setter('height'))
        self.console_scroll.add_widget(self.console_output)

        right_layout.add_widget(self.console_scroll)
        main_layout.add_widget(right_layout)

        self.add_widget(main_layout)

    def launch_wifi_screen(self, instance):
        # Switch to the WiFiScreen
        self.manager.current = "wifi_screen"

    def launch_my_app_screen(self, instance):
        # Switch to the MyAppScreen
        self.manager.current = "myapp_screen"


# ---- Screen 2: WiFi Config (old KeyboardApp) ----

class WiFiScreen(Screen):
    def __init__(self, **kwargs):
        super(WiFiScreen, self).__init__(**kwargs)
        self.name = "wifi_screen"
        
        # Keep references for keyboard and layout
        self.keyboard = None
        self.keyboard_layout = None

        # Root layout
        self.root_layout = BoxLayout(orientation="vertical", spacing=10, padding=10)

        # Wi-Fi network selection
        self.network_spinner = Spinner(
            text="Select Network",
            values=self.get_wifi_networks(),  # Dynamically retrieved SSIDs
            size_hint=(1, 0.15),
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
        button_layout = BoxLayout(size_hint=(1, 0.1), spacing=10)

        # Cancel Button
        cancel_button = Button(text = "Cancel", on_press=self.on_cancel)
        button_layout.add_widget(cancel_button)
        # Show/hide password button
        show_pwd = Button(text="Show Password", on_press=self.on_show)
        button_layout.add_widget(show_pwd)

        # Clear button
        clear_button = Button(text="Clear", on_press=self.on_clear)
        button_layout.add_widget(clear_button)

        # Connect button
        self.connect_button = Button(text="Connect", on_press=self.on_connect)
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
        if self.keyboard_layout:
            return

        # Container for the keyboard and the hide button
        self.keyboard_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.8))
        print(self.keyboard_layout.width, self.keyboard_layout.height)
        # Create the VKeyboard
        self.keyboard = Window.request_keyboard(None, self.keyboard_layout)
        #self.keyboard = VKeyboard(size_hint=(1, 1.5))

        self.keyboard.bind(on_key_up=self.on_key_up)
        
        # 'Hide Keyboard' button
        hide_btn = Button(text="Hide Keyboard", size_hint=(1, 0.2))
        hide_btn.bind(on_press=self.hide_keyboard)

        # Add them to the keyboard layout
        #self.keyboard_layout.add_widget(self.keyboard)
        self.keyboard_layout.add_widget(hide_btn)

        # Add the keyboard layout to the root layout
        self.root_layout.add_widget(self.keyboard_layout)

    def hide_keyboard(self, *args):
        """Remove the keyboard layout from the screen."""
        if self.keyboard_layout:
            self.root_layout.remove_widget(self.keyboard_layout)
            self.keyboard_layout = None
            self.keyboard = None

    def on_key_up(self, vkeyboard, keycode, *args):
        if keycode:
            text = keycode  # Extract key name
            if text == 'backspace':
                self.text_input.text = self.text_input.text[:-1]
            elif len(text) == 1:  # Ignore non-character keys
                self.text_input.text += text


# ---- Screen 3: MyApp (FloatLayout, dynamic components) ----
class MyAppScreen(Screen):
    def __init__(self, **kwargs):
        super(MyAppScreen, self).__init__(**kwargs)
        self.name = "myapp_screen"
        self.polling_interval = 0.1
        self.main_layout = FloatLayout()
        Window.clearcolor = (0.7, 0.7, 0.7, 1)
        self.add_widget(self.main_layout)

    def on_enter(self, *args):
        """Called automatically when entering the screen."""
        print("MyAppScreen on_enter")
        # Start scheduled tasks if needed:
        Clock.schedule_interval(self.poll_gpio_button, self.polling_interval)
        self.fetch_data_and_build_ui()

    def on_leave(self, *args):
        """Called automatically when leaving the screen."""
        print("MyAppScreen on_leave")
        Clock.unschedule(self.poll_gpio_button)

    def fetch_data_and_build_ui(self):
        # Example GET request to fetch layout
        url = "https://protocontrol.dev/api/get-most-recent-layout"
        self.main_layout.clear_widgets()

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            print(data)
            # Build dynamic components
            self.create_components(data, self.main_layout)
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    @classmethod
    def create_components(cls, input_data, main_layout, grid_width=12, grid_height=7):
        for component_data in input_data:
            x = component_data.get('x', 0)
            y = component_data.get('y', 0)
            w = component_data.get('w', 1)
            h = component_data.get('h', 1)
            compType = component_data.get('type')
            comp_id = component_data.get('id')
            text = component_data.get('label', "")

            pos_hint_x = x / grid_width
            pos_hint_y = 1 - ((y + 1) / grid_height)
            size_hint_w = max(w / grid_width, 1 / grid_width)
            size_hint_h = max(h / grid_height, 1 / grid_height)

            pos_hint = {'x': pos_hint_x, 'y': pos_hint_y}
            size_hint = (size_hint_w, size_hint_h)
            color = hex_to_rgba(component_data.get('primaryColor', '#ffffff'))

            widget = None
            if compType == "Button":
                widget = PushButton(
                    text=str(text),
                    id=str(comp_id),
                    color=color,
                    size_hint=size_hint,
                    pos_hint=pos_hint
                )
            elif compType == "Toggle":
                widget = ToggleButtonWidget(
                    text=str(text),
                    id=str(comp_id),
                    size_hint=size_hint,
                    pos_hint=pos_hint
                )
            elif compType == "Slider":
                min_v = component_data.get("min", 0)
                max_v = component_data.get("max", 100)
                widget = SliderWidget(
                    text=str(text),
                    min=min_v,
                    max=max_v,
                    id=str(comp_id),
                    size_hint=size_hint,
                    pos_hint=pos_hint
                )
            elif compType == "Console":
                widget = ConsoleWidget(
                    text=str(text),
                    id=str(comp_id),
                    size_hint=size_hint,
                    pos_hint=pos_hint
                )

            if widget:
                main_layout.add_widget(widget)

    def poll_gpio_button(self, dt):
        """Poll GPIO pin 11 for button press."""
        if not debug_mode and platform.system() == 'Linux':
            if GPIO.input(11) == GPIO.HIGH:
                print("Button was pushed!")
                # For example, fetch new data and rebuild
                self.fetch_data_and_build_ui()

# ---- The Main App with ScreenManager ----
class CombinedApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())

        # Add screens
        sm.add_widget(ConfigScreen())
        sm.add_widget(WiFiScreen())
        sm.add_widget(MyAppScreen())

        sm.current = "config_screen"  # Start on config screen
        return sm

if __name__ == '__main__':
    CombinedApp().run()
