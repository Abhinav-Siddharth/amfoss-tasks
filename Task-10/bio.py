import os
import cv2
import numpy as np
from PIL import Image, ImageDraw

# Path to your biome images
ASSETS_FOLDER = os.path.join("Treasure-Map", "assets")

# Create output file name
OUTPUT_MAP = "treasure_map.png"

def get_sorted_images(folder):
    if not os.path.exists(folder):
        raise FileNotFoundError(f"⚠️ Folder '{folder}' not found!")
    files = [f for f in os.listdir(folder) if f.endswith(".png")]
    if not files:
        raise ValueError(f"⚠️ No biome scan images found in '{folder}'!")
    files.sort(key=lambda x: int(x.split('_')[0]))
    return [os.path.join(folder, f) for f in files]

def analyze_image(path):
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if img is None:
        return None, None, None, True

    # Create mask to detect non-transparent or non-white areas
    if img.shape[2] == 4:  # RGBA
        mask = img[:, :, 3] > 0
        mask = mask.astype(np.uint8) * 255
    else:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 5, 255, cv2.THRESH_BINARY)

    # Find contours to locate the main block
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours or cv2.contourArea(max(contours, key=cv2.contourArea)) < 500:
        return None, None, None, True

    largest_contour = max(contours, key=cv2.contourArea)
    M = cv2.moments(largest_contour)
    if M["m00"] == 0:
        return None, None, None, True

    center_x = int(M["m10"] / M["m00"])
    center_y = int(M["m01"] / M["m00"])
    masked_img = cv2.bitwise_and(img, img, mask=mask)
    avg_color = cv2.mean(masked_img, mask=mask)[:3]

    return center_x, center_y, avg_color, False

def build_treasure_map(image_paths):
    block_data = []
    for path in image_paths:
        center_x, center_y, avg_color, is_blank = analyze_image(path)
        block_data.append((center_x, center_y, avg_color, is_blank))

    num_images = len(image_paths)
    map_width = num_images * 50
    map_height = 128
    output_img = Image.new("RGB", (map_width, map_height), color="white")
    draw = ImageDraw.Draw(output_img)

    prev_center = None
    prev_color = None

    for i, (center_x, center_y, avg_color, is_blank) in enumerate(block_data):
        if is_blank:
            prev_center = None
            continue

        adj_x = i * 50 + center_x // 2
        adj_y = center_y
        color_tuple = tuple(int(c) for c in avg_color[::-1])

        draw.ellipse((adj_x - 10, adj_y - 10, adj_x + 10, adj_y + 10), fill=color_tuple)

        if prev_center:
            prev_adj_x, prev_adj_y = prev_center
            draw.line((prev_adj_x, prev_adj_y, adj_x, adj_y), fill=prev_color, width=5)

        prev_center = (adj_x, adj_y)
        prev_color = color_tuple

    output_img.save(OUTPUT_MAP)
    print(f"✅ Treasure map saved as '{OUTPUT_MAP}'")
    output_img.show()

def main():
    image_paths = get_sorted_images(ASSETS_FOLDER)
    build_treasure_map(image_paths)

if __name__ == "__main__":
    main()
