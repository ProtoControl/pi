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

registrationId = generate_alphanumeric_code()
User = None
deviceStatus = "built"
deviceName = None
devType = "ProtoType"
version = "BETA"
payload = {
    "registrationId": registrationId,
    "User":User,
    "deviceStatus": deviceStatus,
    "deviceName":deviceName,
    "devType": devType,
    "version": version
}

response = requests.put(url, json=payload)
print(response)
