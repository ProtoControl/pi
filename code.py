import hashlib

def generate_device_code():
    """
    Generate a unique 4-digit code for a Raspberry Pi using its hardware ID.

    Returns:
        int: A 4-digit code unique to the device.
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
        
        # Hash the hardware ID to ensure uniqueness
        hash_obj = hashlib.sha256(hardware_id.encode())
        hashed_value = int(hash_obj.hexdigest(), 16)
        
        # Generate a 4-digit code (use modulo to ensure it fits 4 digits)
        device_code = hashed_value % 10000
        return device_code

    except Exception as e:
        print(f"Error generating device code: {e}")
        return None

# Example usage
if __name__ == "__main__":
    code = generate_device_code()
    if code is not None:
        print(f"Unique device code: {code:04d}")
