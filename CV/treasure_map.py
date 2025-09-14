import cv2
import numpy as np
from PIL import Image, ImageDraw
import glob
import os
import re

# Step 1: Load and sort image files
def get_sorted_images(folder_path):
    image_files = glob.glob(os.path.join(folder_path, "*.png"))
    # Sort by numerical prefix (e.g., 001, 002)
    image_files.sort(key=lambda x: int(re.match(r'(\d+)_', os.path.basename(x)).group(1)))
    return image_files

# Step 2: Process image to detect block, average color, and center
def process_image(image_path):
    # Load image with OpenCV (BGR format)
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print(f"Failed to load {image_path}")
        return None, None, None

    # Check if image is blank (fully transparent or uniform color)
    if img.shape[2] == 4:  # Has alpha channel
        alpha = img[:, :, 3]
        if np.all(alpha == 0):  # Fully transparent
            return None, None, None
    else:
        # Check for uniform color (e.g., all black or white)
        if np.std(img) < 1:  # Low standard deviation indicates uniform color
            return None, None, None

    # Convert to grayscale for contour detection
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return None, None, None

    # Get the largest contour (assumed to be the block)
    contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(contour)
    center = (x + w // 2, y + h // 2)

    # Calculate average color of the block
    mask = np.zeros_like(gray)
    cv2.drawContours(mask, [contour], -1, 255, -1)
    block_pixels = img[mask == 255]
    if block_pixels.size == 0:
        return None, None, None
    avg_color = np.mean(block_pixels, axis=0)[:3]  # BGR, ignore alpha if present

    return center, avg_color, contour

# Step 3: Create the treasure map
def create_treasure_map(image_files):
    # Calculate canvas size (e.g., 10x10 grid for up to 100 images)
    grid_size = int(np.ceil(np.sqrt(len(image_files))))
    canvas_size = grid_size * 128
    canvas = Image.new('RGBA', (canvas_size, canvas_size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(canvas)

    # Store block info
    blocks = []
    for idx, img_path in enumerate(image_files):
        center, avg_color, _ = process_image(img_path)
        if center is None:  # Blank image
            blocks.append(None)
        else:
            # Map center to canvas coordinates
            row = idx // grid_size
            col = idx % grid_size
            canvas_x = col * 128 + center[0]
            canvas_y = row * 128 + center[1]
            # Convert BGR to RGB
            rgb_color = (int(avg_color[2]), int(avg_color[1]), int(avg_color[0]))
            blocks.append((canvas_x, canvas_y, rgb_color))

    # Draw blocks and lines
    for i in range(len(blocks)):
        if blocks[i] is None:
            continue
        x, y, color = blocks[i]
        # Draw block center as a small circle
        draw.ellipse([x-5, y-5, x+5, y+5], fill=color)

        # Draw line to next non-blank block
        for j in range(i + 1, len(blocks)):
            if blocks[j] is not None:
                next_x, next_y, _ = blocks[j]
                draw.line([x, y, next_x, next_y], fill=color, width=2)
                break

    return canvas

# Main execution
def main():
    folder_path = "assets"  # Adjust if assets is elsewhere
    image_files = get_sorted_images(folder_path)
    if not image_files:
        print("No images found in the assets folder!")
        return

    treasure_map = create_treasure_map(image_files)
    treasure_map.save("treasure_map.png")
    print("Treasure map saved as treasure_map.png")

if __name__ == "__main__":
    main()
