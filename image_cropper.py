# Importing Image class from PIL module
from PIL import Image

# Opens a image in RGB mode
im = Image.open(r"D:\Github\tools\generated\avatars\original\100\Character-In Car_20.png")

# Size of the image in pixels (size of original image)
# (This is not mandatory)
width, height = im.size

# Setting the points for cropped image
left = 55
top = 151
right = 519
bottom = 487

# Cropped image of above dimension
# (It will not change original image)
im1 = im.crop((left, top, right, bottom))

# Shows the image in image viewer
im1.save(r"D:\Github\tools\generated\avatars\original\100\cropped.png")
