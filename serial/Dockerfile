# Use the latest Debian base image
FROM debian:latest

# Install required packages
RUN apt update && apt install -y \
    gcc \
    socat \
    python3 \
    python3-pip \
    python3-tk \
    python3-venv \
    libmsgpack-dev \
    libmsgpackc2 \
    x11-apps

# Set the working directory inside the container
WORKDIR /app

# Copy all the source files
COPY serial_receiver.c .
COPY cobs.h .
COPY cobs.c .
COPY serial_gui.py .
COPY entrypoint.sh .

# Compile the C receiver program
RUN gcc -o serial_receiver serial_receiver.c cobs.c -I/usr/include/ -L/usr/lib/x86_64-linux-gnu/ -lmsgpackc

# Create a virtual environment for Python dependencies
RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Install Python dependencies inside the virtual environment
RUN pip install --no-cache-dir pyserial msgpack cobs 

# Ensure the entrypoint script is executable
RUN chmod +x entrypoint.sh

# Set runtime library path so the MsgPack library is found
ENV LD_LIBRARY_PATH="/usr/lib/x86_64-linux-gnu/:$LD_LIBRARY_PATH"

# Set the DISPLAY variable for XQuartz on Mac (requires XQuartz to be running)
ENV DISPLAY=host.docker.internal:0h

# Use the entrypoint script as the container's startup command
ENTRYPOINT ["./entrypoint.sh"]
