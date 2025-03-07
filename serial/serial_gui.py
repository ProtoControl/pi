#!/usr/bin/env python3
import tkinter as tk
from tkinter import scrolledtext
import serial
import msgpack
import struct
import cobs.cobs as cobs
import threading
import time
import os

# Serial communication setup
SERIAL_PORT = "/dev/pts/2"  # Must match socat link
BAUD_RATE = 9600

def crc16(data: bytes) -> int:
    crc = 0xFFFF
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ 0x8005
            else:
                crc <<= 1
    return crc & 0xFFFF

def encode_message(data: dict) -> bytes:
    packed = msgpack.packb(data, use_bin_type=True)  # Ensure consistent encoding
    encoded = cobs.encode(packed)  # Apply COBS encoding
    crc = crc16(encoded)  # Compute CRC
    return encoded + struct.pack(">H", crc)  # Append CRC


def send_message():
    msg = entry.get()
    if not msg:
        return
    encoded_msg = encode_message({"message": msg})
    ser.write(encoded_msg)
    sent_text.insert(tk.END, f"Sent: {msg}\n")
    encoded_text.insert(tk.END, f"Encoded: {encoded_msg.hex()}\n")
    entry.delete(0, tk.END)

def receive_messages():
    while True:
        try:
            # Read from the log file
            with open("/tmp/c_output.log", "r") as f:
                lines = f.readlines()
            
            if lines:
                for line in lines[-10:]:  # Only process the last 10 messages
                    recv_text.insert(tk.END, f"{line.strip()}\n")
                    recv_text.see(tk.END)

            time.sleep(1)

        except Exception as e:
            recv_text.insert(tk.END, f"Error: {e}\n")

# Setup serial communication
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

# Setup GUI
root = tk.Tk()
root.title("Serial Communication GUI")

entry = tk.Entry(root, width=50)
entry.pack(pady=5)

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(pady=5)

sent_text = scrolledtext.ScrolledText(root, width=60, height=5)
sent_text.pack(pady=5)
sent_text.insert(tk.END, "Sent Messages:\n")

encoded_text = scrolledtext.ScrolledText(root, width=60, height=5)
encoded_text.pack(pady=5)
encoded_text.insert(tk.END, "Encoded Messages:\n")

recv_text = scrolledtext.ScrolledText(root, width=60, height=10)
recv_text.pack(pady=5)
recv_text.insert(tk.END, "Received Messages:\n")

# Start a thread to continuously read messages from the C program
threading.Thread(target=receive_messages, daemon=True).start()

root.mainloop()
