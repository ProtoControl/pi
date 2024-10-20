from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.slider import Slider
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.graphics import Rectangle, Color
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
#import serial
import ast
import re
import sys
import requests
import random
import string

import platform
import os
import subprocess
import time
import platform
import socket

Window.size = (800, 480)
debug_mode = '-d' in sys.argv

class WifiSetupApp(App):
    def build(self):
        self.main_layout = FloatLayout()

        # Check for internet connectivity
        if not self.is_connected():
            # No internet - enter Wi-Fi setup mode
            self.wifi_setup()
        else:
            # Internet connected - proceed with app normally
            self.main_layout.add_widget(Label(text="Connected to the internet!"))
            self.on_connected()

        return self.main_layout

    def is_connected(self):
        """Check if the Raspberry Pi is connected to the internet."""
        try:
            # Try to connect to a reliable host (Google DNS)
            socket.create_connection(("8.8.8.8", 53))
            return True
        except OSError:
            return False

    def wifi_setup(self):
        """Display available networks and allow the user to connect."""
        available_networks = self.scan_wifi_networks()

        # Display available networks
        network_list_layout = BoxLayout(orientation='vertical', size_hint=(1, 1))
        network_list_label = Label(text="Available Networks:", size_hint=(1, 0.1))
        network_list_layout.add_widget(network_list_label)

        for network in available_networks:
            network_button = Button(text=network, size_hint=(1, 0.1))
            network_button.bind(on_press=self.show_password_popup)
            network_list_layout.add_widget(network_button)

        self.main_layout.clear_widgets()
        self.main_layout.add_widget(network_list_layout)

    def scan_wifi_networks(self):
        """Scan for available Wi-Fi networks using iwlist."""
        try:
            result = subprocess.run(['sudo', 'iwlist', 'wlan0', 'scan'], capture_output=True, text=True)
            networks = set()
            for line in result.stdout.split('\n'):
                if "ESSID" in line:
                    essid = line.split(':')[1].strip().replace('"', '')
                    if essid:
                        networks.add(essid)
            return list(networks)
        except subprocess.CalledProcessError as e:
            print(f"Error scanning networks: {e}")
            return []

    def show_password_popup(self, instance):
        """Show a popup to input the password for the selected Wi-Fi network."""
        network_name = instance.text

        content = BoxLayout(orientation='vertical', spacing=10)
        label = Label(text=f"Enter password for {network_name}:")
        password_input = TextInput(password=True, multiline=False)
        submit_button = Button(text="Connect")

        content.add_widget(label)
        content.add_widget(password_input)
        content.add_widget(submit_button)

        popup = Popup(title="Wi-Fi Password", content=content, size_hint=(0.6, 0.6))

        submit_button.bind(on_press=lambda x: self.connect_to_wifi(network_name, password_input.text, popup))
        popup.open()

    def connect_to_wifi(self, ssid, password, popup):
        """Connect to the Wi-Fi network with the given credentials."""
        popup.dismiss()
        try:
            wifi_config = f"""
            network={{
                ssid="{ssid}"
                psk="{password}"
            }}
            """
            with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'a') as file:
                file.write(wifi_config)

            subprocess.run(['sudo', 'wpa_cli', '-i', 'wlan0', 'reconfigure'])
            time.sleep(5)  # Wait for the connection to establish

            if self.is_connected():
                self.main_layout.clear_widgets()
                self.main_layout.add_widget(Label(text="Connected to the internet!"))
                self.on_connected()  # Call when connected
            else:
                self.main_layout.clear_widgets()
                self.main_layout.add_widget(Label(text="Failed to connect. Please try again."))

        except Exception as e:
            print(f"Error connecting to Wi-Fi: {e}")
            self.main_layout.clear_widgets()
            self.main_layout.add_widget(Label(text="Error connecting to Wi-Fi."))

    def on_connected(self):
        """Callback when Wi-Fi is connected. Closes the WifiSetupApp and launches MyApp."""
        self.stop()  # Close the Wi-Fi setup app
        MyApp().run()  # Launch the main app


if platform.system() == 'Windows':
    print("Running on Windows")
    debug_mode = True  # Automatically enable debug mode on Windows

if debug_mode:
    print("DEBUG MODE - NO UART CONNECTED")
else:
    if platform.system() == 'Linux':  # Assuming Raspberry Pi is running Linux
        import serial  # Import serial module only if not in debug mode

        try:
            ser = serial.Serial(
                port='/dev/tty0',  # Replace with your serial port
                baudrate=115200,
                timeout=1
            )
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")
            debug_mode = True
    else:
        print("This script is not running on a supported system for UART.")


class PushButton(Button):
    def __init__(self, text, id, color = (1,1,1,1), **kwargs):
        super(PushButton, self).__init__(**kwargs)
        self.text = text
        self.background_color = color
        self.id = id

    def on_press(self):
        message = f"{self.id},1"
        print(message)
        #if not debug_mode:
            #ser.write(message.encode('utf-8'))


class ToggleButtonWidget(ToggleButton):
    def __init__(self,id,text, **kwargs):
        super(ToggleButtonWidget, self).__init__(**kwargs)
        self.state = 'normal'
        self.id = id
        self.text = text
    def on_state(self, widget, value):
        message = f"{self.id},{value}"
        print(message)
        #if not debug_mode:
            #ser.write(message.encode('utf-8'))



class SliderWidget(BoxLayout):
    def __init__(self, text, min, max, id,**kwargs):
        super(SliderWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'

        self.slider = Slider(min=min, max = max, value=min)
        self.slider.orientation = 'horizontal'
        self.slider.value_track = True
        self.slider.value_track_color = [1, 0, 0, 1]
        self.slider.text = text
        self.slider.min = min
        self.slider.max = max
        self.slider.id = id
        self.value_label = Label(text=f"{text}: {min}", size_hint=(1, 0.2), font_size = '40sp')
        self.slider.bind(value=self.on_value_change)

        self.add_widget(self.value_label)
        self.add_widget(self.slider)

    def on_value_change(self, instance, value):
        rounded_value = round(value, 2)
        message = f"{self.slider.id},{rounded_value}"
        print(message)
        #if not debug_mode:
            #ser.write(message.encode('utf-8'))
        self.value_label.text = f"Value: {rounded_value}"
 

class ConsoleWidget(BoxLayout):
    def __init__(self, text, id,**kwargs):
        super(ConsoleWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'
        
        # Create a label at the top of the console
        self.label = Label(text=text, size_hint=(1, 0.1), font_size='18sp')
        self.id = id
        # Create a text input field to display the content (like a console log)
        self.content = TextInput(
            multiline=True,
            readonly=True,  # Prevent editing
            font_size='16sp',
            size_hint=(1, 0.9),
            background_color=[0, 0, 0, 1],  # Console-like background (black)
            foreground_color=[1, 1, 1, 1]   # Text color (white)
        )
        
        # Add the label and the text field to the layout
        self.add_widget(self.label)
        self.add_widget(self.content)
    def write_to_console(self, text):
        self.content.text = f"{text}\n"

#Hard coded json website example:
#input = [{"x":11,"y":6,"w":0,"h":0,"id":"unknown-id","compType":"button"},{"x":0,"y":0,"w":0,"h":0,"id":"unknown-id","compType":"button"},{"x":0,"y":6,"w":4,"h":0,"id":"unknown-id","compType":"button"},{"x":4,"y":3,"w":4,"h":0,"id":"unknown-id","compType":"button"},{"x":11,"y":0,"w":0,"h":0,"id":"unknown-id","compType":"button"}]


#decode function
def create_components(input_data, main_layout, grid_width=12, grid_height=7):

    for component_data in input_data:

        x = component_data.get('x', 0)
        y = component_data.get('y', 0)
        w = component_data.get('w', 1)
        h = component_data.get('h', 1)
        compType = component_data.get('compType')
        comp_id = component_data.get('id', 'unknown-id')
        
        # Convert grid positions to percentages of the screen size
        pos_hint_x = x / grid_width
        pos_hint_y = 1 - ((y + 1) / grid_height)        
        print(pos_hint_x)
        print(pos_hint_y)
        # Convert grid size to size_hint percentages
        size_hint_w = max(w / grid_width, 1 / grid_width)  # Minimum size 1 grid unit wide
        size_hint_h = max(h / grid_height, 1 / grid_height)  # Minimum size 1 grid unit tall
        
        # Create pos_hint and size_hint
        pos_hint = {'x': pos_hint_x, 'y': pos_hint_y}
        size_hint = (size_hint_w, size_hint_h)
        
        # Format the constructor call
        constructor_call = f'{compType}(text="{comp_id}", id="{comp_id}", size_hint={size_hint}, pos_hint={pos_hint})'
        
        # Dynamically create the widget using eval
        try:
            widget = eval(constructor_call)
            main_layout.add_widget(widget)
            print(f"Created: {widget}")
        except NameError:
            print(f"Component type {compType} not recognized")


# Example input
input_data = [
    {"x": 0, "y": 0, "w": 0, "h": 0, "id": "unknown-id", "compType": "PushButton"},
    {"x": 1, "y": 0, "w": 4, "h": 0, "id": "unknown-id", "compType": "PushButton"},
    {"x": 4, "y": 4, "w": 4, "h": 0, "id": "unknown-id", "compType": "PushButton"},
    {"x": 4, "y": 2, "w": 2, "h": 0, "id": "unknown-id", "compType": "PushButton"},
    {"x": 0, "y": 4, "w": 4, "h": 0, "id": "unknown-id", "compType": "PushButton"},
    {"x": 0, "y": 5, "w": 6, "h": 0, "id": "unknown-id", "compType": "PushButton"},
    {"x": 0, "y": 3, "w": 2, "h": 0, "id": "unknown-id", "compType": "PushButton"},
    {"x": 0, "y": 6, "w": 4, "h": 0, "id": "unknown-id", "compType": "PushButton"},
    {"x": 8, "y": 2, "w": 4, "h": 0, "id": "unknown-id", "compType": "PushButton"},
    {"x": 5, "y": 1, "w": 4, "h": 0, "id": "unknown-id", "compType": "PushButton"},
    {"x": 0, "y": 2, "w": 3, "h": 0, "id": "unknown-id", "compType": "PushButton"},
    {"x": 8, "y": 6, "w": 4, "h": 0, "id": "unknown-id", "compType": "PushButton"},
    {"x": 8, "y": 0, "w": 4, "h": 0, "id": "unknown-id", "compType": "PushButton"}
]



class MyApp(App):
    def build(self):
        #grab layout from website:
        #r = requests.get('https://api.github.com/events')
        #print(r.json)
        # Define a 4x3 GridLayout
        main_layout = FloatLayout()

        create_components(input_data, main_layout)


        # Create other functional widgets
        # toggle_button = ToggleButtonWidget(text="toggle", id = 'B', size_hint=(.25, .3), pos_hint={'x':.5, 'y':.2})
        # slider_widget = SliderWidget(text = "value", min=1, max=50, id = 'C', size_hint=(1, .3), pos_hint={'x':.2, 'y':.6})
        # push_button = PushButton(text = "press", color = (1,1,1,1), id = 'A',size_hint = (.25,.3), pos_hint = {'x':.1,'y':.1})
        # console = ConsoleWidget(text="Toggle State", id = 'D', size_hint=(.25, .3), pos_hint={'x':.02, 'y':.6})
        # console.write_to_console(toggle_button.state)
        
        # Bind the toggle button state to the method that updates the console
        #toggle_button.bind(state=lambda instance, value: console.write_to_console(f"Toggle State: {value}"))

        # main_layout.add_widget(console)
        # main_layout.add_widget(push_button)
        # main_layout.add_widget(toggle_button)
        # main_layout.add_widget(slider_widget)
        return main_layout


if __name__ == "__main__":
    if WifiSetupApp().is_connected():
        MyApp().run()  # Skip WifiSetupApp and directly launch MyApp
    else:
        WifiSetupApp().run()  # Run the Wifi setup if not connected
