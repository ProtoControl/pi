from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit,
                             QTextEdit, QLabel, QScrollArea)
from PySide6.QtCore import QThread, Signal, Slot
import serial
import msgpack
import struct
import cobs.cobs as cobs
import sys

SERIAL_PORT = "/dev/ttyACM0"
BAUD_RATE = 115200

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
    packed = msgpack.packb(data, use_bin_type=True)
    encoded = cobs.encode(packed)
    crc = crc16(encoded)
    return encoded + struct.pack(">H", crc)

def decode_message(encoded_msg: bytes) -> dict:
    try:
        decoded = cobs.decode(encoded_msg[:-2])
        crc_received = struct.unpack(">H", encoded_msg[-2:])[0]
        crc_calculated = crc16(encoded_msg[:-2])
        if crc_received != crc_calculated:
            return {"error": "CRC mismatch"}
        return msgpack.unpackb(decoded, raw=False)
    except Exception as e:
        return {"error": str(e)}

class SerialReader(QThread):
    message_received = Signal(bytes)

    def run(self):
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        while True:
            if ser.in_waiting > 0:
                received_data = ser.read(ser.in_waiting)
                self.message_received.emit(received_data)

class SerialGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        self.serial_thread = SerialReader()
        self.serial_thread.message_received.connect(self.handle_received_data)
        self.serial_thread.start()

    def initUI(self):
        self.setWindowTitle("Serial Communication GUI")
        layout = QVBoxLayout()
        
        self.entry = QLineEdit()
        self.entry.setPlaceholderText("Enter message")
        layout.addWidget(self.entry)
        
        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send_message)
        layout.addWidget(send_button)
        
        self.sent_text = QTextEdit()
        self.sent_text.setReadOnly(True)
        self.sent_text.setPlaceholderText("Sent Messages:")
        layout.addWidget(self.sent_text)
        
        self.encoded_text = QTextEdit()
        self.encoded_text.setReadOnly(True)
        self.encoded_text.setPlaceholderText("Encoded Messages:")
        layout.addWidget(self.encoded_text)
        
        self.recv_text = QTextEdit()
        self.recv_text.setReadOnly(True)
        self.recv_text.setPlaceholderText("Received Messages:")
        layout.addWidget(self.recv_text)
        
        self.decoded_text = QTextEdit()
        self.decoded_text.setReadOnly(True)
        self.decoded_text.setPlaceholderText("Decoded Messages:")
        layout.addWidget(self.decoded_text)
        
        self.setLayout(layout)

    @Slot()
    def send_message(self):
        msg = self.entry.text()
        if not msg:
            return
        encoded_msg = encode_message({"message": msg})
        self.ser.write(encoded_msg)
        self.sent_text.append(f"Sent: {msg}")
        self.encoded_text.append(f"Encoded: {encoded_msg.hex()}")
        self.entry.clear()

    @Slot(bytes)
    def handle_received_data(self, received_data):
        self.recv_text.append(f"Received: {received_data.hex()}")
        decoded_msg = decode_message(received_data)
        self.decoded_text.append(f"Decoded: {decoded_msg}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SerialGUI()
    window.show()
    sys.exit(app.exec())
