"""
I'm placing the edition settings here until I find
a better place, but I want to keep them in the same
file by now to avoid duplicating them in the files
I am building for new concepts.

TODO: Move this to a definitive file in a near 
future, please
"""
from yta_image.edition.settings import COLOR_TEMPERATURE_CHANGE_LIMIT, BRIGHTNESS_LIMIT, CONTRAST_LIMIT, SHARPNESS_LIMIT, WHITE_BALANCE_LIMIT, SPEED_FACTOR_LIMIT


SMALL_AMOUNT_TO_FIX = 0.000001
"""
Small decimal amount to fix an error with frame
time moments. We use those time moments as limits
and due to a random rounding by the system, the
value is sometimes above the limit and sometimes
below, so we fix that randomness with this small
value we add.
"""


MAX_TIMELINE_LAYER_DURATION = 1200
"""
The maximum duration a timeline layer can have
according to all the subclips on it. This value
can change to allow longer timeline layers.
"""

LAYERS_INDEXES_LIMIT = (0, 9)
"""
The limit of the layers indexes we have, starting
from 0, so only the upper limit + 1 layers are
available in the edition system.
"""
VOLUME_LIMIT = (0, 300)
"""
The limit of the volumen adjustment. Zero (0) means
silence, 100 means the original audio volume and
300 means 3 times higher volume.
"""
ZOOM_LIMIT = (1, 500)
"""
The limit of the zoom adjustment. One (1) means a
zoom out until the video is a 1% of its original 
size, 100 means the original size and 500 means a
zoom in to reach 5 times the original video size.
"""
ROTATION_LIMIT = (-360, 360)
"""
The limit of the rotation adjustment. Zero (0) 
means no rotation, while 90 means rotated 90 
degrees to the left, 180 means flipped vertically
and 360 means no rotation.
"""
COLOR_TEMPERATURE_LIMIT = COLOR_TEMPERATURE_CHANGE_LIMIT
"""
The limit of the color temperature adjustment. Zero
(0) means no change, while -50 means...

TODO: Fulfill this as it depends on another const
"""
BRIGHTNESS_LIMIT = BRIGHTNESS_LIMIT
"""
The limit of the image brightness adjustment.
"""
CONTRAST_LIMIT = CONTRAST_LIMIT
"""
The limit of the image contrast adjustment.
"""
SHARPNESS_LIMIT = SHARPNESS_LIMIT
"""
The limit of the image sharpness adjustment.
"""
WHITE_BALANCE_LIMIT = WHITE_BALANCE_LIMIT
"""
The limit of the image white balance adjustment.
"""
SPEED_FACTOR_LIMIT = SPEED_FACTOR_LIMIT
"""
The limit of the speed factor adjustment.
"""