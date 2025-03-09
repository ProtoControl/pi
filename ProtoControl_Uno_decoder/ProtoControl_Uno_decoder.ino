#include <ArduinoJson.h>  // Include before MsgPack.h
#include <MsgPack.h>
#include <PacketSerial.h>
#include "CRC16.h"
#include "CRC.h"

#define BAUD_RATE 115200
#define BUFFER_SIZE 256

PacketSerial packetSerial;
CRC16 crc;  // Create CRC16 object

void onPacketReceived(const uint8_t* buffer, size_t size) {
    Serial.println("Received encoded data:");
    for (size_t i = 0; i < size; i++) {
        Serial.print(buffer[i], HEX);
        Serial.print(" ");
    }
    Serial.println();

    if (size < 2) {
        Serial.println("Error: Packet too small");
        return;
    }

    // Extract CRC16 from last two bytes
    uint16_t receivedCRC = (buffer[size - 2] << 8) | buffer[size - 1];
    size_t decodedSize = size - 2;

    // Compute CRC16
    crc.restart();
    crc.add(buffer, decodedSize);
    uint16_t calculatedCRC = crc.calc();

    if (calculatedCRC != receivedCRC) {
        Serial.println("Error: CRC mismatch");
        return;
    }

    // Unpack MessagePack
    MsgPack::Unpacker unpacker;
    unpacker.feed(buffer, decodedSize);
    String unpackedMessage;
    unpacker.deserialize(unpackedMessage);

    Serial.print("Decoded Message: ");
    Serial.println(unpackedMessage);
}

void setup() {
    Serial.begin(BAUD_RATE);
    while (!Serial);
    Serial.println("Arduino Serial Test Initialized");

    packetSerial.begin(BAUD_RATE);
    packetSerial.setPacketHandler(&onPacketReceived);
}

void loop() {
    Serial.println("Enter text to send:");
    while (!Serial.available());

    String input = Serial.readStringUntil('\n');
    input.trim();
    Serial.print("Input: ");
    Serial.println(input);

    // Pack using MessagePack
    MsgPack::Packer packer;
    packer.serialize(input);

    // Get packed data
    uint8_t packedData[BUFFER_SIZE];
    size_t packedSize = packer.size();
    memcpy(packedData, packer.data(), packedSize);

    // Compute CRC16
    crc.restart();
    crc.add(packedData, packedSize);
    uint16_t crcValue = crc.calc();

    // Append CRC16 to packed data
    packedData[packedSize] = (crcValue >> 8) & 0xFF;
    packedData[packedSize + 1] = crcValue & 0xFF;
    packedSize += 2;

    // Send encoded data (PacketSerial automatically handles COBS encoding)
    packetSerial.send(packedData, packedSize);
    Serial.println("Encoded message sent");

    delay(2000);
}
