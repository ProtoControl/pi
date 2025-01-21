import json
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.clock import Clock
import requests
from widgets.console_widget import ConsoleWidget
from widgets.pushbuttton_widget import PushButton
from widgets.slider_widget import SliderWidget
from widgets.toggle_widget import ToggleButtonWidget
from utils.helpers import hex_to_rgba

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
        self.build_ui()

    def on_leave(self, *args):
        """Called automatically when leaving the screen."""
        print("MyAppScreen on_leave")

    def build_ui(self):
        
        with open("layout.txt","r") as save:
            data = save.read()
            print(data)
            data = json.loads(data)
            
        self.create_components(data, self.main_layout)
        

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

