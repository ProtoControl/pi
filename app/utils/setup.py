#Python setup script to Create entry in the database


import requests

from platform_utils import generate_alphanumeric_code


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

import time
import secrets
import string

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



url = ""


serialNumber = generate_serial_number(prefix="TEST")
registrationId = generate_alphanumeric_code()
User = None
deviceStatus = "built"
deviceName = None
devType = "ProtoType"
version = "BETA"
payload = {
    "serialNumber":
    "registrationId": registrationId,
    "User":User,
    "deviceStatus": deviceStatus,
    "deviceName":deviceName,
    "devType": devType,
    "version": version
}

response = requests.put(url, json=payload)
print(response)
