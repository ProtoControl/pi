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
import serial
import ast
import re
# ser = serial.Serial(
#     port='/dev/ttyS0',  # Replace with your serial port
#     baudrate=115200,
#     timeout=1
# )

import random
import string

def generate_random_text(max_length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(1, max_length)))

def generate_random_color():
    return tuple(random.choice([0, 1]) for _ in range(4))

def generate_random_size_hint():
    return (1, random.uniform(0, 0.2))

def generate_constructor():
    text = generate_random_text()
    color = generate_random_color()
    size_hint = generate_random_size_hint()
    # Generate the constructor string
    constructor_str = (f"PushButton,{text},{color},{size_hint}")
    return constructor_str

def dynamic_constructor(input_string):
    # Use regex to extract the parts correctly
    match = re.match(r'(\w+),(\w+),(\([^\)]+\)),(\([^\)]+\))', input_string)
    
    if not match:
        raise ValueError(f"Input string format is invalid: {input_string}")
    
    class_name = match.group(1)  # Extract class name
    text = match.group(2)        # Extract text
    color_str = match.group(3)   # Extract color tuple string
    size_hint_str = match.group(4)  # Extract size_hint tuple string

    # Convert the string representations of tuples into actual tuples
    color = ast.literal_eval(color_str)
    size_hint = ast.literal_eval(size_hint_str)

    # Dynamically get the class by its name and call the constructor
    cls = globals().get(class_name)
    if not cls:
        raise ValueError(f"Class {class_name} not found!")

    # Instantiate the class using the parsed arguments
    instance = cls(text=text, color=color, size_hint=size_hint)
    
    return instance



# Set the custom screen ratio (e.g., 800x480 for a widescreen format)
Window.size = (800, 480)
#Window.fullscreen = 'auto'

class PushButton(Button):
    def __init__(self, text, color, **kwargs):
        super(PushButton, self).__init__(**kwargs)
        self.text = text
        self.background_color = color
        #self.location = self.assign(self.x, self.y)

    def on_press(self):
        #Also Print to uart
        print(f"{self.text}1")


class ToggleButtonWidget(ToggleButton):
    def __init__(self, **kwargs):
        super(ToggleButtonWidget, self).__init__(**kwargs)
        #self.location = self.assign(self.x, self.y)
        self.state = 'normal'

    def on_state(self, widget, value):
        message = f"{self.text}{value}"
        print(message)

        #ser.write(message.encode('utf-8'))



class SliderWidget(BoxLayout):
    def __init__(self, text, min, max, **kwargs):
        super(SliderWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'

        self.slider = Slider(min=min, max = max, value=min)
        self.slider.orientation = 'horizontal'
        self.slider.value_track = True
        self.slider.value_track_color = [1, 0, 0, 1]
        self.slider.text = text
        self.slider.min = min
        self.slider.max = max
        self.value_label = Label(text=f"{text}: {min}", size_hint=(1, 0.2), font_size = '40sp')
        self.slider.bind(value=self.on_value_change)

        self.add_widget(self.value_label)
        self.add_widget(self.slider)

    def on_value_change(self, instance, value):
        rounded_value = round(value, 2)
        print(f"Slider Value: {rounded_value}")
        self.value_label.text = f"Value: {rounded_value}"
 

class ConsoleWidget(BoxLayout):
    def __init__(self, label_text, **kwargs):
        super(ConsoleWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'
        
        # Create a label at the top of the console
        self.label = Label(text=label_text, size_hint=(1, 0.1), font_size='18sp')
        
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


class MyApp(App):
    def build(self):
        # Define a 4x3 GridLayout
        main_layout = FloatLayout()

        
        # Create other functional widgets
        toggle_button = ToggleButtonWidget(text="Toggle Button", size_hint=(.25, .3), pos_hint={'x':.5, 'y':.2})
        slider_widget = SliderWidget(text = "value", min=1, max=50, size_hint=(1, .3), pos_hint={'x':.2, 'y':.6})
        push_button = PushButton(text = "press", color = (1,1,1,1), size_hint = (.25,.3), pos_hint = {'x':.1,'y':.1})
        console = ConsoleWidget(label_text="Toggle State", size_hint=(.25, .3), pos_hint={'x':.02, 'y':.6})

        console.write_to_console(toggle_button.state)
        
        # Bind the toggle button state to the method that updates the console
        toggle_button.bind(state=lambda instance, value: console.write_to_console(f"Toggle State: {value}"))

        main_layout.add_widget(console)
        main_layout.add_widget(push_button)
        main_layout.add_widget(toggle_button)
        main_layout.add_widget(slider_widget)
        return main_layout


if __name__ == '__main__':
    MyApp().run()
