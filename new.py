from PIL import Image
import numpy as np

'''# Load image
img = Image.open("CERT-SE.jpg")
pixels = np.array(img)

# Parameters
start_x, start_y = 1860, 130
block_size = 50
grid_size = 3
gap = 5  # adjust if there’s spacing between big blocks

# Function to get binary pattern from one 50x50 block
def decode_block(x, y):
    sub_size = block_size // grid_size
    bits = ""
    for row in range(grid_size):
        for col in range(grid_size):
            # Coordinates of sub-block
            sx = x + col * sub_size
            sy = y + row * sub_size
            sub = pixels[sy:sy+sub_size, sx:sx+sub_size]
            # Average brightness
            avg = np.mean(sub)
            bits += "1" if avg > 128 else "0"
    return bits

# Decode all 15 blocks
binaries = []
for row in range(3):  # 3 rows of blocks
    cols = 7 if row < 2 else 1
    for col in range(cols):
        x = start_x + col * (block_size + 2)  # tweak +2 if blocks touch
        y = start_y + row * (block_size + 2)
        bits = decode_block(x, y)
        binaries.append(bits)

# Convert binary to ASCII
decoded_text = ""
for b in binaries:
    # Take first 8 bits
    char = chr(int(b[:8], 2))
    decoded_text += char

print("Binary patterns:", binaries)
print("Decoded:", decoded_text)'''

binaries = [
'001111011', '001110001', '110011100', '000101110', '101011100',
'010110001', '100010111', '111001000', '001111111', '011100111',
'111110111', '110011110', '101110011', '101110011', '111011111'
]

# Combine all bits
all_bits = "".join(binaries)

# Pad to multiple of 8
while len(all_bits) % 8 != 0:
    all_bits += "0"

# Convert to bytes
bytes_data = bytes(int(all_bits[i:i+8], 2) for i in range(0, len(all_bits), 8))
print("Raw bytes:", bytes_data)

# Try ASCII
try:
    print("ASCII:", bytes_data.decode("utf-8"))
except:
    print("Non-ASCII characters present.")

# Try base64
import base64
try:
    decoded_b64 = base64.b64decode(bytes_data).decode("utf-8", errors="ignore")
    print("Base64 decoded:", decoded_b64)
except:
    pass

# Try hex
print("Hex:", bytes_data.hex())
