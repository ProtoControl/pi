import sys
import platform
import requests
import json
import re
import ast
import random
import string

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.slider import Slider
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

try:
    import RPi.GPIO as GPIO
    import serial
except ImportError:
    GPIO = None
    serial = None

# -------------------------------------------------------------------
# Global Settings
# -------------------------------------------------------------------
URL = "https://protocontrol.dev/api/get-most-recent-layout"

# Adjust window size if desired. Remove for normal full window usage.
Window.size = (800, 480)

# Determine debug mode from CLI argument or OS
DEBUG_MODE = '-d' in sys.argv or platform.system() == 'Windows'
if DEBUG_MODE:
    print("DEBUG MODE ACTIVE: No hardware / UART connection will be made.")

# -------------------------------------------------------------------
# Utility Functions
# -------------------------------------------------------------------
def hex_to_rgba(hex_color):
    """
    Convert a hex color string (e.g., '#AABBCC' or '#AABBCCDD') to an RGBA tuple.
    """
    hex_color = hex_color.lstrip('#')
    if len(hex_color) not in (6, 8):
        raise ValueError(
            "Hex color must be '#RRGGBB' or '#RRGGBBAA' format."
        )
    r = int(hex_color[0:2], 16) / 255
    g = int(hex_color[2:4], 16) / 255
    b = int(hex_color[4:6], 16) / 255
    a = int(hex_color[6:8], 16) / 255 if len(hex_color) == 8 else 1
    return (r, g, b, a)


# -------------------------------------------------------------------
# Custom Widgets
# -------------------------------------------------------------------
class PushButton(Button):
    """
    Button widget that sends a message upon press.
    """

    def __init__(self, text, comp_id, color=(1, 1, 1, 1), **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.id = comp_id
        self.background_color = color

    def on_press(self):
        message = f"{self.id},1"
        print(f"[PushButton] {message}")
        # Write to serial if not in debug mode
        if not DEBUG_MODE:
            # ser.write(message.encode('utf-8'))  # Your serial instance
            pass


class ToggleButtonWidget(ToggleButton):
    """
    Toggle button widget that sends a message upon state change.
    """

    def __init__(self, comp_id, text, **kwargs):
        super().__init__(**kwargs)
        self.id = comp_id
        self.text = text
        self.state = 'normal'

    def on_state(self, instance, value):
        message = f"{self.id},{value}"
        print(f"[ToggleButton] {message}")
        if not DEBUG_MODE:
            # ser.write(message.encode('utf-8'))
            pass


class SliderWidget(BoxLayout):
    """
    Slider widget that prints and sends serial messages whenever its value changes.
    """

    def __init__(self, text, min_val, max_val, comp_id, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        self.slider = Slider(
            min=min_val,
            max=max_val,
            value=min_val,  # Initial slider value
            orientation='horizontal',
            value_track=True,
            value_track_color=[1, 0, 0, 1]
        )
        self.slider.text = text  # Keep reference of the label text
        self.slider.bind(value=self.on_value_change)
        self.slider.id = comp_id

        self.value_label = Label(
            text=f"{text}",
            size_hint=(1, 0.2),
            font_size='40sp'
        )

        self.add_widget(self.value_label)
        self.add_widget(self.slider)

    def on_value_change(self, instance, value):
        """
        Called whenever slider value changes.
        """
        rounded_value = round(value, 2)
        message = f"{self.slider.id},{rounded_value}"
        self.value_label.text = f"{self.slider.text}: {rounded_value}"
        print(f"[Slider] {message}")
        if not DEBUG_MODE:
            # ser.write(message.encode('utf-8'))
            pass


class ConsoleWidget(BoxLayout):
    """
    A simple console-like widget that displays text logs.
    """

    def __init__(self, text, comp_id, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.id = comp_id

        self.label = Label(
            text=text,
            size_hint=(1, 0.1),
            font_size='18sp'
        )
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
        """
        Append text to the console.
        """
        # Could append, but in your original code it overwrote the text each time.
        self.content.text += f"{text}\n"


# -------------------------------------------------------------------
# Widget Factory
# -------------------------------------------------------------------
def widget_factory(component_data):
    """
    Returns an instance of the appropriate widget class
    based on the component's 'type' field.
    """
    comp_type = component_data.get('type')
    comp_id = str(component_data.get('id'))
    text = str(component_data.get('label', ''))
    primary_color = component_data.get('primaryColor', '#FFFFFF')

    color = hex_to_rgba(primary_color)
    size_hint = _calculate_size_hint(component_data)
    pos_hint = _calculate_pos_hint(component_data)

    if comp_type == "Button":
        return PushButton(
            text=text,
            comp_id=comp_id,
            color=color,
            size_hint=size_hint,
            pos_hint=pos_hint
        )
    elif comp_type == "Toggle":
        return ToggleButtonWidget(
            comp_id=comp_id,
            text=text,
            size_hint=size_hint,
            pos_hint=pos_hint
        )
    elif comp_type == "Slider":
        min_val = component_data.get("min", 0)
        max_val = component_data.get("max", 100)
        return SliderWidget(
            text=text,
            min_val=min_val,
            max_val=max_val,
            comp_id=comp_id,
            size_hint=size_hint,
            pos_hint=pos_hint
        )
    elif comp_type == "Console":
        return ConsoleWidget(
            text=text,
            comp_id=comp_id,
            size_hint=size_hint,
            pos_hint=pos_hint
        )
    else:
        # Could raise an error or return None
        print(f"[widget_factory] Unknown component type: {comp_type}")
        return None


def _calculate_size_hint(component_data, grid_width=12, grid_height=7):
    """
    Convert grid size to size_hint percentages.
    """
    w = component_data.get('w', 1)
    h = component_data.get('h', 1)
    size_hint_w = max(w / grid_width, 1 / grid_width)
    size_hint_h = max(h / grid_height, 1 / grid_height)
    return (size_hint_w, size_hint_h)


def _calculate_pos_hint(component_data, grid_width=12, grid_height=7):
    """
    Convert grid positions to percentages of the screen size.
    Note: Kivy's default coordinate system has y=0 at the bottom.
    If your layout data has y=0 at top, you may want to invert it.
    """
    x = component_data.get('x', 0)
    y = component_data.get('y', 0)
    pos_hint_x = x / grid_width
    # Because top-left is often considered 0, let's invert Y to bottom-left
    pos_hint_y = 1 - ((y + 1) / grid_height)
    return {'x': pos_hint_x, 'y': pos_hint_y}


# -------------------------------------------------------------------
# Main App
# -------------------------------------------------------------------
class MyApp(App):
    """
    Main Application class.
    """

    def build(self):
        """
        Kivy calls build() to get the root widget.
        """
        # Use a FloatLayout as our main container
        self.main_layout = FloatLayout()
        Window.clearcolor = (0.7, 0.7, 0.7, 1)

        # Attempt initial data fetch
        self.get_and_build_layout()

        # If on a supported system and not in debug mode, set up GPIO
        if not DEBUG_MODE and platform.system() == 'Linux':
            self.setup_gpio()

        # Poll the GPIO button (if in production environment) every 0.1s
        Clock.schedule_interval(self.poll_gpio_button, 0.1)

        return self.main_layout

    def on_start(self):
        """
        Called after the application has finished initializing and
        is about to start running.
        """
        print("[MyApp] on_start")
        return super().on_start()

    def on_pause(self):
        """
        Called when your application is about to go into the background.
        """
        print("[MyApp] on_pause")
        return True

    def on_resume(self):
        """
        Called when your app comes back from the background.
        """
        print("[MyApp] on_resume")
        return True

    def on_stop(self):
        """
        Called before the application stops.
        """
        print("[MyApp] on_stop")
        return super().on_stop()

    # -------------------------------------------------------------------
    # Data & Layout Handling
    # -------------------------------------------------------------------
    def get_and_build_layout(self):
        """
        Fetch the layout (JSON) from the server and build the corresponding UI.
        """
        try:
            response = requests.get(URL)
            response.raise_for_status()
            data = response.json()
            print("[MyApp] Layout data retrieved successfully.")

            # Rebuild the layout
            self.build_layout(data)

        except requests.exceptions.RequestException as err:
            print(f"[MyApp] An error occurred during layout fetch: {err}")

    def build_layout(self, layout_data):
        """
        Clear and rebuild main layout using fetched layout data.
        """
        self.main_layout.clear_widgets()
        for component in layout_data:
            widget = widget_factory(component)
            if widget:
                self.main_layout.add_widget(widget)
                print(f"[MyApp] Created widget: {widget}")

    # -------------------------------------------------------------------
    # GPIO Handling
    # -------------------------------------------------------------------
    def setup_gpio(self):
        """
        Set up Raspberry Pi GPIO if not in debug mode.
        """
        if GPIO is not None:
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            print("[MyApp] GPIO setup complete.")

        # If using serial, open the port here
        if serial is not None:
            try:
                # Adjust '/dev/tty0' to the actual port on your device
                self.ser = serial.Serial(
                    port='/dev/tty0',
                    baudrate=115200,
                    timeout=1
                )
                print("[MyApp] Serial port opened successfully.")
            except serial.SerialException as e:
                print(f"[MyApp] Error opening serial port: {e}")

    def poll_gpio_button(self, dt):
        """
        Called periodically by Kivy's Clock to check if a GPIO button is pressed.
        """
        if GPIO is not None:
            if GPIO.input(11) == GPIO.HIGH:
                print("[MyApp] Detected hardware button press!")
                self.get_and_build_layout()


# -------------------------------------------------------------------
# Entry Point
# -------------------------------------------------------------------
if __name__ == '__main__':
    MyApp().run()
