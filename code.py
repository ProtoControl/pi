import hashlib

def generate_alphanumeric_code(length=8):
    """
    Generate an alphanumeric code based on the Raspberry Pi's hardware ID.

    Args:
        length (int): Length of the alphanumeric code. Default is 8 characters.

    Returns:
        str: An alphanumeric code unique to the device.
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
        print(hardware_id)
        # Hash the hardware ID to ensure uniqueness
        hash_obj = hashlib.sha256(hardware_id.encode())
        hashed_value = hash_obj.hexdigest()
        
        # Generate an alphanumeric code of the specified length
        alphanumeric_code = hashed_value[:length].upper()  # Use uppercase for consistency
        return alphanumeric_code

    except Exception as e:
        print(f"Error generating alphanumeric code: {e}")
        return None

# Example usage
if __name__ == "__main__":
    code = generate_alphanumeric_code(8)  # Generate an 8-character alphanumeric code
    if code:
        print(f"Unique alphanumeric code: {code}")
