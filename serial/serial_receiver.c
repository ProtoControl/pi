#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <termios.h>
#include <stdint.h>
#include <msgpack.h>
#include "cobs.h"

#define SERIAL_PORT "/dev/pts/1"  // Virtual serial port path
#define BUFFER_SIZE 256

int serial_fd;

// CRC-16 Calculation
uint16_t crc16(const uint8_t *data, size_t length) {
    uint16_t crc = 0xFFFF;
    for (size_t i = 0; i < length; i++) {
        crc ^= (uint16_t)data[i] << 8;
        for (uint8_t j = 0; j < 8; j++) {
            if (crc & 0x8000) {
                crc = (crc << 1) ^ 0x8005;
            } else {
                crc <<= 1;
            }
        }
    }
    return crc;
}

// Initialize the virtual serial port
int init_serial() {
    serial_fd = open(SERIAL_PORT, O_RDWR | O_NOCTTY);
    if (serial_fd == -1) {
        perror("Error opening serial port");
        return -1;
    }

    struct termios options;
    tcgetattr(serial_fd, &options);
    cfsetispeed(&options, B9600);
    cfsetospeed(&options, B9600);
    options.c_cflag = CS8 | CLOCAL | CREAD;
    options.c_iflag = IGNPAR;
    options.c_oflag = 0;
    options.c_lflag = 0;
    tcflush(serial_fd, TCIFLUSH);
    tcsetattr(serial_fd, TCSANOW, &options);

    return 0;
}

// Read and process data from the virtual serial port
void read_serial() {
    uint8_t buffer[BUFFER_SIZE];

    while (1) {
        int len = read(serial_fd, buffer, BUFFER_SIZE);
        if (len < 3) continue;

        uint16_t received_crc = (buffer[len - 2] << 8) | buffer[len - 1];

        uint16_t calculated_crc = crc16(buffer, len - 2);
        if (received_crc != calculated_crc) {
            fprintf(stderr, "Error: CRC Mismatch!\n");
            continue;
        }

        uint8_t decoded_data[BUFFER_SIZE];
        size_t decoded_length = cobs_decode(buffer, len - 2, decoded_data);
        if (decoded_length == 0) {
            fprintf(stderr, "Error: COBS Decoding Failed\n");
            continue;
        }

        // Deserialize MessagePack
        msgpack_unpacked result;
        msgpack_unpacked_init(&result);

        if (msgpack_unpack_next(&result, decoded_data, decoded_length, NULL) == MSGPACK_UNPACK_SUCCESS) {
            msgpack_object obj = result.data;
            printf("Received: ");
            msgpack_object_print(stdout, obj);
            printf("\n");
        } else {
            fprintf(stderr, "Error: MsgPack Deserialization Failed\n");
        }

        msgpack_unpacked_destroy(&result);
    }
}

int main() {
    if (init_serial() != 0) return 1;
    printf("Listening on virtual serial port: %s\n", SERIAL_PORT);
    read_serial();
    return 0;
}
