from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.slider import Slider
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
#import serial
import ast
import re
import sys
import requests
import random
import string

import platform


# Set the custom screen ratio (e.g., 800x480 for a widescreen format)
Window.size = (800, 480)
debug_mode = '-d' in sys.argv
#Window.fullscreen = 'auto'


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
    {"x": 8, "y": 0, "w": 4, "h": 0, "id": "unknown-id", "compType": "PushButton"},
    {"x": 0, "y": 1, "w": 0, "h": 0, "id": "unknown-id", "compType": "PushButton"},
    {"x": 8, "y": 3, "w": 4, "h": 0, "id": "unknown-id", "compType": "PushButton"}
]



class MyApp(App):
    def build(self):
        main_layout = FloatLayout()
        create_components(input_data, main_layout)
        Clock.schedule_once(self.force_refresh, 0)
        return main_layout
    def force_refresh(self, dt):
        # Force a redraw of the window/canvas
        Window.canvas.clear()
        Window.canvas.ask_update()
        Window.show()


if __name__ == '__main__':
    MyApp().run()
