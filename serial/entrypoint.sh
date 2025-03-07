#!/bin/bash
set -e

echo "Starting socat to create virtual serial port..."
socat -d -d pty,raw,echo=0,link=/tmp/serial pty,raw,echo=0 &
sleep 3  # Give socat time to set up the serial port

echo "Starting C receiver..."
./serial_receiver | tee /tmp/c_output.log &  # Pipe C output to a log file
C_RECEIVER_PID=$!

echo "Starting Python GUI..."
python3 serial_gui.py &  # Run the Python GUI

# Wait for GUI to close before killing C receiver
wait $!
kill $C_RECEIVER_PID
