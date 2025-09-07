import os
from PIL import Image
import cv2
import numpy as np

# Step 1: Get and sort images
assets_folder = os.path.join('Treasure-Map', 'assets')  # Updated path

# Print current working directory for debugging
print("Current working directory:", os.getcwd())

# Check if the folder exists
if not os.path.exists(assets_folder):
    print(f"Warning: Folder '{assets_folder}' does not exist in {os.getcwd()}.")
    print("Suggestions:")
    print("1. Run 'ls -l Treasure-Map/assets/' to check for PNG files.")
    print("2. Ensure you cloned the full repo and assets folder exists.")
    print("3. Update 'assets_folder' variable if the path is different.")
    raise FileNotFoundError(f"The folder '{assets_folder}' does not exist.")

try:
    image_files = [f for f in os.listdir(assets_folder) if f.endswith('.png')]
except FileNotFoundError:
    raise FileNotFoundError(f"Could not access '{assets_folder}'. Verify the folder exists and contains PNG files.")

if not image_files:
    raise ValueError(f"No PNG files found in '{assets_folder}'. Ensure images like '001_dirt.png' are present.")

# Sort by numerical prefix (e.g., '001_dirt.png' -> 1)
image_files.sort(key=lambda x: int(x.split('_')[0]))

print("Sorted images:", image_files)

# Full paths for loading
image_paths = [os.path.join(assets_folder, f) for f in image_files]




# Step 2: Analyze each image
block_data = []  # Store (center_x, center_y, avg_color, is_blank)

for path in image_paths:
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)  # Load with alpha channel
    if img is None:
        print(f"Error loading {path}")
        block_data.append((None, None, None, True))  # Treat as blank
        continue
    
    # Convert to HSV for better color detection
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Threshold to isolate block (assume background is transparent or uniform)
    # If transparent, use alpha channel; else, adjust HSV bounds
    if img.shape[2] == 4:  # Has alpha channel
        mask = img[:, :, 3] > 0  # Non-transparent pixels
        mask = mask.astype(np.uint8) * 255  # Convert to binary mask
    else:
        # Fallback: HSV threshold (tweak if background isn't neutral)
        lower_bound = np.array([0, 0, 50])  # Ignore dark/low saturation
        upper_bound = np.array([180, 255, 255])
        mask = cv2.inRange(hsv, lower_bound, upper_bound)
    
    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours or cv2.contourArea(max(contours, key=cv2.contourArea)) < 100:
        # Blank or too small → teleport point
        block_data.append((None, None, None, True))
        continue
    
    # Largest contour = block
    largest_contour = max(contours, key=cv2.contourArea)
    
    # Center via moments
    M = cv2.moments(largest_contour)
    if M['m00'] == 0:
        block_data.append((None, None, None, True))
        continue
    center_x = int(M['m10'] / M['m00'])
    center_y = int(M['m01'] / M['m00'])
    
    # Average color (BGR)
    masked_img = cv2.bitwise_and(img, img, mask=mask)
    avg_color = cv2.mean(masked_img, mask=mask)[:3]  # Ignore alpha
    
    block_data.append((center_x, center_y, avg_color, False))
    print(f"{path}: Center ({center_x}, {center_y}), Color {avg_color}")
