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


import random
import string


ser = serial.Serial(
    port='/dev/ttyS0',  # Replace with your serial port
    baudrate=115200,
    timeout=1
)



# Set the custom screen ratio (e.g., 800x480 for a widescreen format)
Window.size = (800, 480)
#Window.fullscreen = 'auto'

class PushButton(Button):
    def __init__(self, text, color, id, **kwargs):
        super(PushButton, self).__init__(**kwargs)
        self.text = text
        self.background_color = color
        self.id = id

    def on_press(self):
        message = f"{self.id},1"
        print(message)
        ser.write(message.encode('utf-8'))


class ToggleButtonWidget(ToggleButton):
    def __init__(self,id,text, **kwargs):
        super(ToggleButtonWidget, self).__init__(**kwargs)
        self.state = 'normal'
        self.id = id
        self.text = text
    def on_state(self, widget, value):
        message = f"{self.id},{value}"
        print(message)
        ser.write(message.encode('utf-8'))



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
        ser.write(message.encode('utf-8'))
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


class MyApp(App):
    def build(self):
        # Define a 4x3 GridLayout
        main_layout = FloatLayout()

        
        # Create other functional widgets
        toggle_button = ToggleButtonWidget(text="toggle", id = 'B', size_hint=(.25, .3), pos_hint={'x':.5, 'y':.2})
        slider_widget = SliderWidget(text = "value", min=1, max=50, id = 'C', size_hint=(1, .3), pos_hint={'x':.2, 'y':.6})
        push_button = PushButton(text = "press", color = (1,1,1,1), id = 'A',size_hint = (.25,.3), pos_hint = {'x':.1,'y':.1})
        console = ConsoleWidget(text="Toggle State", id = 'D', size_hint=(.25, .3), pos_hint={'x':.02, 'y':.6})

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
