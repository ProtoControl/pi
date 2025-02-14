import json
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button.button import MDButton, MDButtonText
from kivymd.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivymd.uix.textfield import MDTextField
import requests
from utils.graybox import GrayBox
from kivymd.uix.gridlayout import GridLayout
from utils.platform_utils import PlatformUtils

platform_utils = PlatformUtils()
code = platform_utils.generate_alphanumeric_code()

class ConfigScreen(MDScreen):
    def __init__(self, **kwargs):
        super(ConfigScreen, self).__init__(**kwargs)
        print("ConfigScreen")
        self.name = "config_screen"  # ScreenManager reference name
        
        main_layout = MDBoxLayout(orientation='horizontal', spacing=10, padding=10)

        # LEFT SIDE
        left_layout = MDBoxLayout(orientation='vertical', spacing=10, size_hint=(0.3, 1))
        
        # Device Info
        device_info_container = GrayBox(orientation='vertical', size_hint=(1, 3), padding=10, spacing=5)
        device_info_box = GridLayout(cols=1, spacing=5, size_hint_y=3)

        #Code generation
        
        device_info_box.add_widget(MDLabel(
            text="Device Info",
            font_size="20sp",
            bold=True,
            color=(0, 0, 0, 1)
        ))

        with open("settings.json","r") as save:
            data = save.read()
            data = json.loads(data)
        device_info_box.add_widget(MDLabel(text="Name: MyDevice", color=(0, 0, 0, 1)))
        device_info_box.add_widget(MDLabel(text=f"Registration Code: {data['registrationId']}", color=(0, 0, 0, 1)))
        device_info_box.add_widget(MDLabel(text = "Serial Number:",color=(0,0,0,1)))
        device_info_box.add_widget(MDLabel(text = f"{data['serialNumber']}",color=(0,0,0,1)))
        device_info_box.add_widget(MDLabel(text=f"Firmware: {data['version']}", color=(0, 0, 0, 1)))
        device_info_box.add_widget(MDLabel(text=f"Status: {data['deviceStatus']}", color=(0, 0, 0, 1)))
        device_info_box.add_widget(MDLabel(text=f"User: {data['User']}", color=(0, 0, 0, 1)))


        device_info_container.add_widget(device_info_box)
        left_layout.add_widget(device_info_container)

        filler_box = MDBoxLayout(size_hint=(1, 1))
        left_layout.add_widget(filler_box)

        # Buttons
        buttons_layout = MDBoxLayout(orientation='vertical', spacing=10, size_hint=(1, None))

        layout_button = MDButton(
            MDButtonText(text="Fetch Layout", text_color=(1, 0, 0, 1)),
            size_hint=(1,None),
            height = 50
        )
        layout_button.bind(on_press=self.fetch_button)
        buttons_layout.add_widget(layout_button)

        wifi_button = MDButton(
            MDButtonText(text="Connect to Wi-Fi", text_color=(1, 0, 0, 1)),
            size_hint=(None, None),
            height=50,
            md_bg_color=(0, 0, 0, 1),
        )
        wifi_button.bind(on_press=self.launch_wifi_screen)
        buttons_layout.add_widget(wifi_button)

        cancel_button = MDButton(
            MDButtonText(text="Cancel", text_color=(1, 0, 1, 1)),
            style="filled",
            size_hint=(1, None),
            height=50,
            md_bg_color=(0, 0, 0, 1),
        )
        cancel_button.bind(on_press=self.launch_my_app_screen)
        buttons_layout.add_widget(cancel_button)

        left_layout.add_widget(buttons_layout)

        main_layout.add_widget(left_layout)

        # RIGHT SIDE: Serial Console
        right_layout = MDBoxLayout(orientation='vertical', spacing=10, size_hint=(0.7, 1))
        console_label = MDLabel(
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
    def fetch_button(self, instance):
        self.__class__.fetch_layout()
    @classmethod
    def fetch_layout(self):
        # Example GET request to fetch layout
        url = "https://protocontrol.dev/api/builder/get-most-recent-layout"
        #self.main_layout.clear_widgets()

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            print(data)
            
            with open("layout.json","w") as save:
                print("writing")
                json.dump(data, save, indent=4)
                #save.write(str(data).replace("'","\""))
            # Build dynamic components
            #self.create_components(data, self.main_layout)
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

