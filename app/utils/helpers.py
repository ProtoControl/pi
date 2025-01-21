import platform
import sys
import hashlib



def hex_to_rgba(hex_color):
    # Remove the '#' if present
    hex_color = hex_color.lstrip('#')
    
    if len(hex_color) not in (6, 8):
        raise ValueError("Hex color must be in the format '#RRGGBB' or '#RRGGBBAA'")
    
    r = int(hex_color[0:2], 16) / 255
    g = int(hex_color[2:4], 16) / 255
    b = int(hex_color[4:6], 16) / 255
    a = int(hex_color[6:8], 16) / 255 if len(hex_color) == 8 else 1
    return (r, g, b, a)