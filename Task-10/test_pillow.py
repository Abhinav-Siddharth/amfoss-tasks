from PIL import Image, ImageDraw
print("ImageDraw imported successfully")
img = Image.new('RGB', (100, 100), color='white')
draw = ImageDraw.Draw(img)
print("ImageDraw works!")
