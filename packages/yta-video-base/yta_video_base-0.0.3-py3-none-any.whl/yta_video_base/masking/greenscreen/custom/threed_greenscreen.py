"""
This is a class to keep the code that allows me to
insert an image into another image that contains
a greenscreen region but that is not rectangular,
so we need to make some transformations to fit the
expected region and position.

TODO: Please, this is not fine at all and need 
review, work and love
"""
from yta_image.converter import ImageConverter
from yta_validation import PythonValidator
from moviepy.Clip import Clip
from moviepy import ImageClip, concatenate_videoclips

import cv2
import numpy as np


def _detect_image_corners_with_hsv(image_filename: str):
    """
    Detect the greenscreen corners by applying a hsv mask.
    This method should be improved as it is not detecting 
    the greenscreen properly.

    TODO: Maybe append this to the ImageRegionFinder class.
    """
    image = cv2.imread(image_filename)

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the mask color in HSV values
    low = np.array([35, 50, 50])
    high = np.array([85, 255, 255])

    # Mask to detect green pixels
    mask = cv2.inRange(hsv, low, high)

    # Erode an dilate to improve the mask quality (but it doesn't)
    # work properly for sure
    # mask = cv2.erode(mask, None, iterations=2)  # Erosiona la máscara para eliminar ruido
    # mask = cv2.dilate(mask, None, iterations=2)  # Dilata la máscara para conectar áreas cercanas

    # Find region contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    corners = []
    # Draw green rectangle around the detected region
    # TODO: I should have only one rectangle
    for contour in contours:
        # We approach the shape to a polygon
        # Original factor was 0.02
        epsilon = 0.01 * cv2.arcLength(contour, True)
        polygon_approach = cv2.approxPolyDP(contour, epsilon, True)

        # We accept a 4 corners polygon
        if len(polygon_approach) == 4:
            corners = [(corner[0][0], corner[0][1]) for corner in polygon_approach]

    return corners

def _order_corners(corners):
    """
    This method orders the coordinates clockwise from upper
    left to lower left corner.
    """
    # We ensure they are numpy arrays to work with them
    corners = np.array(corners, dtype = 'float32')

    # We apply a 'x' order from lower to higher
    corners = corners[np.argsort(corners[:, 1])]
    upper_left, upper_right = sorted(corners[:2], key = lambda p: p[0])
    lower_left, lower_right = sorted(corners[2:], key = lambda p: p[0])

    return [
        upper_left,
        upper_right,
        lower_right,
        lower_left
    ]

def insert_image_into_3d_greenscreen(greenscreen_filename: str, image_to_insert_filename: str, output_filename: str):
    """
    Inserts the provided 'image_to_insert_filename' in the 3d
    greenscreen region available in the also provided 
    'greenscreen_filename' and writes it as a local file with
    the given 'output_filename' file name.
    """
    corners = _detect_image_corners_with_hsv(greenscreen_filename)

    image = greenscreen_filename
    if PythonValidator.is_string(greenscreen_filename):
        image = cv2.imread(greenscreen_filename)

    image_to_inject = image_to_insert_filename
    if PythonValidator.is_string(image_to_insert_filename):
        image_to_inject = cv2.imread(image_to_insert_filename)

    # We need coordinates in clockwise order following the next
    # format: ul, ur, br, bl (u = upper, b = bottom)
    corners = _order_corners(corners)
    corners = np.array(corners, dtype = 'float32')

    # Corners of the image to inject
    alto, ancho = image_to_inject.shape[:2]
    shape_to_inject = np.array([
        [0, 0],
        [ancho - 1, 0],
        [ancho - 1, alto - 1],
        [0, alto - 1]
    ], dtype = 'float32')

    # Calculate new matrix to fit the new region
    matriz = cv2.getPerspectiveTransform(shape_to_inject, corners)

    # Transform the perspective to fit the region
    inserted_image = cv2.warpPerspective(image_to_inject, matriz, (image.shape[1], image.shape[0]), flags = cv2.INTER_NEAREST)

    # Create a mask of the inserted image (only non-transparent part)
    inserted_mask = np.zeros_like(image, dtype = np.uint8)
    cv2.fillConvexPoly(inserted_mask, corners.astype(int), (255, 255, 255))

    # Merge original image with new image applying the mask
    final_image = cv2.bitwise_and(image, cv2.bitwise_not(inserted_mask))
    final_image = cv2.add(final_image, inserted_image)

    # TODO: I need to be more accurate on detecting the corners. I
    # think I could do it manually by detecting all pixels and getting
    # firstly those that are more on the left

    # TODO: I would need to detect the corners better, and also apply
    # another kind of replacement (put the original image in the 
    # foreground, with the region as transparent pixels, and place the
    # the image to insert in the region but also adding some pixels
    # to the corners to ensure it fits the region)

    # TODO: Adapt this to return the image object and not only writing
    # it
    cv2.imwrite(output_filename, final_image)

    return output_filename

def insert_video_into_3d_greenscreen(greenscreen_filename: str, video: Clip, output_filename: str):
    """
    Inserts the provided 'video' into the also provided 3d 
    greenscreen in the file 'greenscreen_filename'. This 
    method will write the file as 'output_filename' if this
    is provided, and will return the new video anyways.
    """
    # We create each image by inserting each frame and then 
    # concatenate all of them to make a new video
    imageclips = [
        ImageClip(insert_image_into_3d_greenscreen(greenscreen_filename, ImageConverter.numpy_image_to_opencv(frame), 'a.png'), duration = 1 / video.fps).with_fps(video.fps) 
        for frame in video.iter_frames()
    ]

    video = concatenate_videoclips(imageclips)

    if (output_filename):
        video.write_videofile(output_filename)

    return video