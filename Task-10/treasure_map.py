import os
from PIL import Image  # Pillow for image creation later
import cv2  # OpenCV for analysis
import numpy as np  # Helper for arrays (comes with OpenCV)

# Step 1: Get and sort images
assets_folder = 'assets'  # Change if different
image_files = [f for f in os.listdir(assets_folder) if f.endswith('.png')]

# Sort by numerical prefix (e.g., '001_dirt.png' -> 1)
image_files.sort(key=lambda x: int(x.split('_')[0]))

print("Sorted images:", image_files)  # Debug: Check order

# Now, full paths for loading
image_paths = [os.path.join(assets_folder, f) for f in image_files]
