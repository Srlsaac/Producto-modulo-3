from PIL import Image, ImageDraw, ImageFont

img = Image.new("RGB", (64, 64), "#1F4E79")
draw = ImageDraw.Draw(img)
draw.text((18, 14), "H", fill="white")
img.save("favicon.ico", format="ICO")