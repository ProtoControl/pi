from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'dock')
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from screens.config_screen import ConfigScreen
from screens.wifi_screen import WiFiScreen
from screens.app_screen import MyAppScreen
from kivy.clock import Clock
import platform
from utils.platform_utils import PlatformUtils
import time
from kivy.core.window import Window

Window.size = (800, 480)

platform_utils = PlatformUtils()
debug_mode = platform_utils.debug_mode

platform_utils.setup_platform_specifics()

class CombinedApp(App):

    def build(self):
        self.sm = ScreenManager(transition=FadeTransition())
        self.polling_interval = 0.01
        
        # Add screens
        self.sm.add_widget(ConfigScreen())
        self.sm.add_widget(WiFiScreen())
        self.sm.add_widget(MyAppScreen())
        ConfigScreen.fetch_layout()
        self.sm.current = "config_screen"  # Start on config screen
        Clock.schedule_interval(self.poll_gpio_button, self.polling_interval)
        return self.sm
    
    def poll_gpio_button(self, dt):
        """Poll GPIO pin 11 for button press."""
        if not debug_mode and platform.system() == 'Linux':
            import serial
            import RPi.GPIO as GPIO
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
   
            if GPIO.input(11) == GPIO.HIGH:
                print("Button was pushed!")
                # For example, fetch new data and rebuild
                #self.fetch_data_and_build_ui()
                if self.sm.current == "config_screen":
                    self.sm.current = "myapp_screen"
                else:
                    self.sm.current = "config_screen"
            time.sleep(0.01)

if __name__ == '__main__':
    CombinedApp().run()
