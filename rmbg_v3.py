from rembg import new_session, remove

session = new_session(model_name="isnet-general-use")

from PIL import Image, ImageOps, ImageEnhance
import numpy as np
import io

# Load and remove background
input_path = "ik.png"
with open(input_path, 'rb') as f:
    input_data = f.read()

output_data = remove(input_data, session=session)
image = Image.open(io.BytesIO(output_data)).convert("RGBA")

# Split channels
r, g, b, a = image.split()

# Grayscale
gray = ImageOps.grayscale(Image.merge("RGB", (r, g, b)))

# Increase contrast (1.0 = original, >1 = more contrast)
contrast_enhancer = ImageEnhance.Contrast(gray)
gray_contrasted = contrast_enhancer.enhance(1)  # Try values like 1.2 to 1.6

# Combine with original alpha
# Merge with alpha
final_image = Image.merge("LA", (gray_contrasted, a)).convert("RGBA")

# Target aspect ratio (height / width)
aspect_ratio = 3 / 5  # or whatever you want

# Get image dimensions
img_width, img_height = final_image.size

# Determine crop width and height while fitting inside the image
max_crop_width = img_width
max_crop_height = int(max_crop_width * aspect_ratio)

if max_crop_height > img_height:
    # If too tall, scale down width to fit withirn height
    max_crop_height = img_height
    max_crop_width = int(max_crop_height / aspect_ratio)

# Align crop to bottom and center horizontally
left = (img_width - max_crop_width) // 2
upper = img_height - max_crop_height
right = left + max_crop_width
lower = img_height

# Crop
custom_cropped = final_image.crop((left, upper, right, lower))

# Save and show
custom_cropped.save(f"{aspect_ratio}.png")
custom_cropped.show()

