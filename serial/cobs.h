#ifndef COBS_H
#define COBS_H

#include <stddef.h>
#include <stdint.h>

/**
 * @brief Encode data using COBS (Consistent Overhead Byte Stuffing)
 * @param input Pointer to the input data
 * @param length Length of the input data
 * @param output Pointer to the output buffer (must be at least `length + 1` bytes)
 * @return Size of encoded data
 */
size_t cobs_encode(const uint8_t *input, size_t length, uint8_t *output);

/**
 * @brief Decode COBS-encoded data
 * @param input Pointer to the encoded data
 * @param length Length of the encoded data
 * @param output Pointer to the output buffer (must be at least `length` bytes)
 * @return Size of decoded data, or 0 if decoding fails
 */
size_t cobs_decode(const uint8_t *input, size_t length, uint8_t *output);

#endif // COBS_H
