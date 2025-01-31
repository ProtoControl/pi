import sys
import platform
import hashlib
import requests
import json
#from config_screen import code

class PlatformUtils:
    def __init__(self):
        self.debug_mode = self.check_debug_mode()
        self.code = self.generate_alphanumeric_code()
        self.setup_platform_specifics()

    def check_debug_mode(self):
        return '-d' in sys.argv or platform.system() in ['Windows', 'Darwin']

    def generate_alphanumeric_code(self, length=8):
        """
        Generate an alphanumeric code based on the Raspberry Pi's hardware ID.

        Args:
            length (int): Length of the alphanumeric code. Default is 8 characters.

        Returns:
            str: An alphanumeric code unique to the device.
        """
        try:
            # Read the hardware ID from /proc/cpuinfo
            with open("/proc/cpuinfo", "r") as f:
                for line in f:
                    if line.startswith("Serial"):
                        hardware_id = line.strip().split(":")[1].strip()
                        break
                else:
                    raise ValueError("Hardware ID not found in /proc/cpuinfo")
            print(hardware_id)
            # Hash the hardware ID to ensure uniqueness
            hash_obj = hashlib.sha256(hardware_id.encode())
            hashed_value = hash_obj.hexdigest()
            
            # Generate an alphanumeric code of the specified length
            alphanumeric_code = hashed_value[:length].upper()  # Use uppercase for consistency
            return alphanumeric_code

        except Exception as e:
            print(f"Error generating alphanumeric code: {e}")
            return None

    def setup_platform_specifics(self):
        if platform.system() == 'Windows' or platform.system() == 'Darwin':
            print("Running on Windows or macOS")
            self.debug_mode = True  # Automatically enable debug mode on Windows
        else:
            print("Running on a non-Windows system")
            print(self.debug_mode)
            print(sys.argv)

        # If you need RPi GPIO and serial in production:
        if not self.debug_mode and platform.system() == 'Linux':
            import serial
            import RPi.GPIO as GPIO
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
   
    
