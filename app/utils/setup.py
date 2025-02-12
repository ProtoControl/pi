#Python setup script to Create entry in the database


import requests
import sys

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


import hashlib

import time
import secrets
import string
import json

"""
Sends device data to the given URL via an HTTP PUT request.

:param url: The endpoint to which the PUT request is sent
:param user: User identifier
:param registrationId: Registration identifier
:param deviceStatus: Status of the device
:param lastCommunicated: Timestamp/device info when last communicated
:param deviceName: Name of the device
:param timeRegistered: Registration timestamp
:param devType: Type/class of the device
:param version: Version number
:param assembledOn: Timestamp when the device was assembled
"""


def generate_alphanumeric_code(length=8):
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


def generate_serial_number(prefix: str = "DEV", random_length: int = 6) -> str:
    """
    Generate a serial number with the following format:
    
        [prefix]-[YYMMDDHHmmSS]-[random_string]
    
    Where:
      - prefix          : A string that might represent the product code or family (default "DEV").
      - YYMMDDHHmmSS    : Timestamp for year, month, day, hour, minute, second.
      - random_string   : A randomly generated alphanumeric of specified length.
      
    Example output: "DEV-250125103045-K2TM4Q"
    
    :param prefix: A short code or label for product type.
    :param random_length: Number of random alphanumeric chars to include.
    :return: A unique serial number string.
    """
    # Get current time as YYYYMMDDHHmmSS, then slice to your preference
    # time.strftime("%y%m%d%H%M%S") -> YYMMDDHHmmSS
    timestamp = time.strftime("%y%m%d%H%M%S")

    # Generate a random alphanumeric string of desired length
    alphabet = string.ascii_uppercase + string.digits
    random_str = ''.join(secrets.choice(alphabet) for _ in range(random_length))
    
    # Combine prefix, timestamp, and random chunk
    serial_number = f"{prefix}-{timestamp}-{random_str}"
    
    return serial_number




class MyWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(MyWidget, self).__init__(**kwargs)
        self.orientation = "vertical"

        # Default variable values
        self.user_var = None
        self.deviceStatus_var = "pending"
        self.deviceName_var = None
        self.devType_var = "ProtoType"
        self.version_var = "0.1.0"

        # 1) User
        row_user = BoxLayout(orientation="horizontal")
        row_user.add_widget(Label(text="User:"))
        self.user_input = TextInput(
            text="" if self.user_var is None else str(self.user_var),
            multiline=False
        )
        row_user.add_widget(self.user_input)
        self.add_widget(row_user)

        # 2) deviceStatus
        row_deviceStatus = BoxLayout(orientation="horizontal")
        row_deviceStatus.add_widget(Label(text="deviceStatus:"))
        self.deviceStatus_input = TextInput(
            text=self.deviceStatus_var,
            multiline=False
        )
        row_deviceStatus.add_widget(self.deviceStatus_input)
        self.add_widget(row_deviceStatus)

        # 3) deviceName
        row_deviceName = BoxLayout(orientation="horizontal")
        row_deviceName.add_widget(Label(text="deviceName:"))
        self.deviceName_input = TextInput(
            text="" if self.deviceName_var is None else str(self.deviceName_var),
            multiline=False
        )
        row_deviceName.add_widget(self.deviceName_input)
        self.add_widget(row_deviceName)

        # 4) devType
        row_devType = BoxLayout(orientation="horizontal")
        row_devType.add_widget(Label(text="devType:"))
        self.devType_input = TextInput(
            text=self.devType_var,
            multiline=False
        )
        row_devType.add_widget(self.devType_input)
        self.add_widget(row_devType)

        # 5) version
        row_version = BoxLayout(orientation="horizontal")
        row_version.add_widget(Label(text="version:"))
        self.version_input = TextInput(
            text=self.version_var,
            multiline=False
        )
        row_version.add_widget(self.version_input)
        self.add_widget(row_version)

        # "Send" button
        send_button = Button(text="Send")
        send_button.bind(on_press=self.send_values_to_console)
        self.add_widget(send_button)

    def send_values_to_console(self, instance):
        # Read updated values
        self.user_var = self.user_input.text if self.user_input.text else None
        self.deviceStatus_var = self.deviceStatus_input.text if self.deviceStatus_input else "pending"
        self.deviceName_var = self.deviceName_input.text if self.deviceName_input.text else None
        self.devType_var = self.devType_input.text if self.devType_input.text else "ProtoType"
        self.version_var = self.version_input.text if self.version_input.text else "0.1.0"

        # Print to console
        print(f"User: {self.user_var}")
        print(f"deviceStatus: {self.deviceStatus_var}")
        print(f"deviceName: {self.deviceName_var}")
        print(f"devType: {self.devType_var}")
        print(f"version: {self.version_var}")

        url = "https://protocontrol.dev/users/initialize-device"

        serialNumber = generate_serial_number(prefix="TEST")
        registrationId = generate_alphanumeric_code()
        
        deviceStatus = self.deviceStatus_var
        
        devType = self.devType_var
        version = self.version_var
        registrationId = "123333"

        payload = {
            "devType": devType,
            "deviceStatus": deviceStatus,
            "registrationId": registrationId,
            "serialNumber": serialNumber,
            "version": version
        }
        
        response = requests.post(url, json=payload)
        print(response)
        with open("settings.json", "w") as save_file:
            json.dump(payload, save_file, indent=4)

        print("Payload written to settings.txt:")
        print(json.dumps(payload, indent=4))

class MyApp(App):
    def build(self):
        return MyWidget()

if __name__ == "__main__":
    MyApp().run()


        