import os
import cv2
import numpy as np
from PIL import Image, ImageDraw

# --- CONFIG ---
INPUT_FOLDER = "Treasure-Map/assets"
OUTPUT_FILE = "treasure_map.png"

# Get sorted image file paths
def get_sorted_images(folder):
    files = [f for f in os.listdir(folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    return sorted(files, key=lambda x: int("".join(filter(str.isdigit, x))))

# Check if an image is blank (teleportation point)
def is_blank(img):
    return np.std(img) < 2  # Very low variance = blank image

# Get average color and center coordinates
def analyze_block(path):
    img = cv2.imread(path)
    h, w, _ = img.shape
    avg_color = cv2.mean(img)[:3]  # BGR
    center = (w // 2, h // 2)
    return avg_color, center

# Main function
def main():
    files = get_sorted_images(INPUT_FOLDER)
    if not files:
        print("⚠️ No biome scans found in the folder!")
        return

    # Store data for plotting
    block_data = []

    for file in files:
        path = os.path.join(INPUT_FOLDER, file)
        img = cv2.imread(path)

        if is_blank(img):
            block_data.append({"teleport": True})
            continue

        avg_color, center = analyze_block(path)
        block_data.append({
            "avg_color": avg_color,
            "center": center,
            "teleport": False
        })

    # Create output image (big enough canvas)
    canvas_size = (1500, 1500)
    map_img = Image.new("RGB", canvas_size, (255, 255, 255))
    draw = ImageDraw.Draw(map_img)

    prev_center = None
    prev_color = None

    for data in block_data:
        if data["teleport"]:
            prev_center = None
            prev_color = None
            continue

        avg_color = tuple(map(int, data["avg_color"][::-1]))  # Convert BGR → RGB
        cx, cy = data["center"]

        # Scale coordinates to fit canvas (adjust if needed)
        scaled_center = (cx * 3, cy * 3)

        # Draw block point
        draw.ellipse(
            [scaled_center[0] - 5, scaled_center[1] - 5,
             scaled_center[0] + 5, scaled_center[1] + 5],
            fill=avg_color, outline="black"
        )

        # Draw connecting lines unless teleporting
        if prev_center is not None:
            draw.line([prev_center, scaled_center], fill=prev_color, width=3)

        prev_center = scaled_center
        prev_color = avg_color

    map_img.save(OUTPUT_FILE)
    print(f"✅ Treasure map saved as: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
