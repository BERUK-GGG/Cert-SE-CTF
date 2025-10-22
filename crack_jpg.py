from PIL import Image
import numpy as np
from collections import Counter

# === Configuration ===
IMAGE_PATH = "CERT-SE.jpg"


import matplotlib.pyplot as plt

img = Image.open("CERT-SE.jpeg")
plt.imshow(img)
plt.title("Click on the top-left corner of first color block")
plt.show()

# You can crop manually to the colored grid section
'''CROP_BOX = (1300, 100, 1800, 250)  # (left, upper, right, lower) — adjust these!

# === Load and crop ===
img = Image.open(IMAGE_PATH)
flag_area = img.crop(CROP_BOX)
pixels = np.array(flag_area)

h, w, _ = pixels.shape
print(f"Cropped area: {w}x{h}")


# Reshape into a list of RGB pixels
pixels = pixels.reshape(-1, 3)

# Count unique colors and their frequency
colors, counts = np.unique(pixels, axis=0, return_counts=True)

# Convert each color to a tuple for sorting
color_tuples = [tuple(c) for c in colors]

# Zip together and sort by frequency descending
sorted_colors = sorted(zip(counts, color_tuples), key=lambda x: x[0], reverse=True)

print(f"Top 10 colors:")
for c, col in sorted_colors[:10]:
    print(f"{col} - {c} pixels")

# === Try to detect pattern size ===
# For example, find vertical/horizontal repeating blocks
block_size = 8  # adjust if the color squares are ~8x8 or 10x10 pixels
rows = h // block_size
cols = w // block_size
print(f"Detected grid: {rows} rows x {cols} cols")

# === Read average color per block ===
grid = []
for r in range(rows):
    row = []
    for c in range(cols):
        block = pixels[r*block_size:(r+1)*block_size, c*block_size:(c+1)*block_size]
        avg = np.mean(block.reshape(-1, 3), axis=0).astype(int)
        row.append(tuple(avg))
    grid.append(row)

# === Optional: visualize color codes ===
for r in range(rows):
    print(" ".join([f"{i}:{'#%02x%02x%02x' % rgb}" for i, rgb in enumerate(grid[r])]))

# === Try binary decoding (e.g., light=1, dark=0) ===
binary = ""
for r in grid:
    for rgb in r:
        brightness = sum(rgb) / 3
        binary += "1" if brightness > 128 else "0"

# === Convert binary to ASCII ===
try:
    decoded = "".join(
        chr(int(binary[i:i+8], 2))
        for i in range(0, len(binary), 8)
    )
    print("\nPossible decoded text:")
    print(decoded)
except Exception as e:

    print("Failed binary-to-text:", e)'''