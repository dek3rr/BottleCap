import os
import glob
import numpy as np
from PIL import Image


CAP_SIZE_MM = 30
CAP_RADIUS_MM = int(CAP_SIZE_MM / 2)


def create_circular_mask(radius):
    """create a circular mask to punch out a subimage"""
    y_coord, x_coord = np.ogrid[: radius * 2, : radius * 2]
    dist_from_center = np.sqrt(
        (x_coord - radius + 0.5) ** 2 + (y_coord - radius + 0.5) ** 2
    )
    circular_mask = dist_from_center <= radius
    return circular_mask


def cleanup():
    image_files = glob.glob("caps/*.png")  # Get all PNG files in the "caps" directory

    for image_file in image_files:
        # Get the dimensions of the image
        im = Image.open(image_file)
        width, height = im.size[1], im.size[0]
        im.close()
        if width == 30 and height == 30:
            try:
                # Remove the file
                os.remove(image_file)
            except OSError as e:
                print(e)


def convert():

    cleanup()
    image_files = glob.glob("caps/*")  # Get all files in the "caps" directory

    # Specify the output directory path
    output_directory = os.path.join(os.getcwd(), "caps_generated")
    print(output_directory)
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for image_file in image_files:
        file_name = os.path.splitext(os.path.basename(image_file))[0]
        try:
            im = Image.open(image_file)
            im = im.convert("RGBA")
            im = im.resize((30, 30))
            orig_img = np.asarray(im)
            mask = create_circular_mask(CAP_RADIUS_MM)
            orig_img[:, :, 3] = mask * 255
            masked = Image.fromarray(orig_img)
            masked.save(os.path.join(output_directory, f"{file_name}.png"))
        except IOError as e:
            print(f"Error converting {image_file}{e}.")


if __name__ == "__main__":
    convert()
