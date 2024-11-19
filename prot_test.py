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
import json
import random
import string

import platform
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import serial
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

# Define the URL
#url = "https://protocontrol.dev/template.php"
url = "https://protocontrol.dev/api/get-most-recent-layout"

ser = None

# Set the custom screen ratio (e.g., 800x480 for a widescreen format)
Window.size = (800, 480)
debug_mode = '-d' in sys.argv
#Window.fullscreen = 'auto'


ser = serial.Serial(
            port='/dev/ttyACM0',  # Replace with your serial port
            baudrate=115200,
            timeout=1
        )
if platform.system() == 'Windows':
    print("Running on Windows")
    debug_mode = True  # Automatically enable debug mode on Windows

if debug_mode:
    print("DEBUG MODE - NO UART CONNECTED")
else:
    if platform.system() == 'Linux':  # Assuming Raspberry Pi is running Linux
        import serial  # Import serial module only if not in debug mode

        
        ser = serial.Serial(
            port='/dev/ttyACM0',  # Replace with your serial port
            baudrate=115200,
            timeout=1
        )
        
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
        # if not debug_mode:
        #     ser.write(message.encode('utf-8'))


class ToggleButtonWidget(ToggleButton):
    def __init__(self,id,text, **kwargs):
        super(ToggleButtonWidget, self).__init__(**kwargs)
        self.state = 'normal'
        self.id = id
        self.text = text
    def on_state(self, widget, value):
        if(self.state == "normal"):
            message = "0"
        else:
            message = "1"
        #print(message)
        if not debug_mode:
            ser.write(message.encode('utf-8'))



class SliderWidget(BoxLayout):
    def __init__(self, text, min, max, id,**kwargs):
        super(SliderWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'

        self.slider = Slider(min=min, max= max, value=min) #Inital value passed to value
        self.slider.orientation = 'horizontal'
        self.slider.value_track = True
        self.slider.value_track_color = [1, 0, 0, 1]
        self.slider.text = text
        self.slider.min = min
        self.slider.max = max
        self.slider.id = id
        self.value_label = Label(text=f"{text}", size_hint=(1, 0.2), font_size = '40sp')
        self.slider.bind(value=self.on_value_change)

        self.add_widget(self.value_label)
        self.add_widget(self.slider)

    def on_value_change(self, instance,value):
        rounded_value = round(value, 2)
        message = f"{self.slider.id},{rounded_value}"
        print(message)
        # if not debug_mode:
        #     ser.write(message.encode('utf-8'))
        self.value_label.text = f"{self.slider.text}: {rounded_value}"
 

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
        
        #console = ConsoleWidget(text="System Output", id = 'D', size_hint=(.25, .3), pos_hint={'x':.02, 'y':.4})



class MyApp(App):

    def on_resume(self):
        print("RESUMED")
        return True
        
    def on_start(self):
        print("start")
        #self.main_layout.clear_widgets()
        self.polling_interval = 0.1
        Clock.schedule_interval(self.poll_gpio_button, self.polling_interval)
        return True
    def on_stop(self):
        print("stop")
        return True
    def on_pause(self):
        print("pause")
        return True
    @classmethod
    def create_components(cls, input_data, main_layout, grid_width=12, grid_height=7):
        #main_layout.clear_widgets()
        for component_data in input_data:

            x = component_data.get('x', 0)
            y = component_data.get('y', 0)
            w = component_data.get('w', 1)
            h = component_data.get('h', 1)
            compType = component_data.get('type')
            comp_id = component_data.get('id')
            text = component_data.get('label')
            
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
            
            # Dynamically create the widget using eval
            try:
                #widget = eval(constructor_call)
                #widget = PushButton(text=comp_id, id=comp_id, size_hint=size_hint, pos_hint=pos_hint)
                match compType:
                    case "Button":
                        widget = PushButton(text=str(text), id=str(comp_id), size_hint=size_hint, pos_hint=pos_hint)
                    case "Toggle":
                        print("tog")
                        widget = ToggleButtonWidget(text=str(text), id=str(comp_id), size_hint=size_hint, pos_hint=pos_hint)
                    case "Slider":
                        #parse slider specific vals
                        min_v = component_data.get("min")
                        max_v = component_data.get("max")
                        
                        widget = SliderWidget(text=str(text), min = min_v, max = max_v, id = str(comp_id), size_hint = size_hint, pos_hint = pos_hint)
                    case "Console":
                        widget = ConsoleWidget(text = str(text),id = str(comp_id), size_hint = size_hint, pos_hint = pos_hint)

                main_layout.add_widget(widget)
                print(f"Created: {widget}")
            except NameError:
                print(f"Component type {compType} not recognized")



    def poll_gpio_button(self, dt):
        """Poll GPIO pin 11 for button press."""
        if GPIO.input(11) == GPIO.HIGH:
            print("Button was pushed!")
            
            try:
                # Make a GET request to the URL
                response = requests.get(url)
                
                # Raise an exception if the request was unsuccessful
                response.raise_for_status()
                
                # Parse the JSON response
                data = response.json()
                print(data)
                self.main_layout.clear_widgets()
                MyApp.create_components(data, self.main_layout)
                print("Data successfully retrieved and components created.")
                
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")
        
        if ser.in_waiting > 0:
            message = ser.read(ser.in_waiting).decode('utf-8').strip()
            #print(message)
            
            self.consoleWidget.write_to_console(message)
            
            
    def build(self):
        # Define a 4x3 GridLayout
        self.main_layout = FloatLayout()
        Window.clearcolor = (0.7, 0.7, 0.7, 1)

        self.consoleWidget = ConsoleWidget(text="System Output", id='console', size_hint=(0.4, 0.15), pos_hint={'x': 0.6, 'y': 0.4})
        self.main_layout.add_widget(self.consoleWidget)
        try:
        # Make a GET request to the URL
            response = requests.get(url)
            
            # Raise an exception if the request was unsuccessful
            response.raise_for_status()
            
            # Parse the JSON response
            data = response.json()
            print(data)
            MyApp.create_components(data,self.main_layout)
            print("Data successfully retrieved and stored in 'output_data.json'.")
        
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
        
        return self.main_layout


if __name__ == '__main__':
    MyApp().run()


