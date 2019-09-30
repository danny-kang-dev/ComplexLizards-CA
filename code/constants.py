# Kernels for identifying neighbors
CONWAY_KERNEL = ((1, 1, 1),
                 (1, 0, 1),
                 (1, 1, 1))
HEX_KERNEL = ((0, 1, 1),
              (1, 0, 1),
              (1, 1, 0))
ADJ_KERNEL = ((0, 1, 0),
              (1, 0, 1),
              (0, 1, 0))

# Window settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)

# Hex rendering settings
HEX_LENGTH = 10  # Length of hexagon edge
HEX_SPACING_X = int(HEX_LENGTH*2)    # Spacing between adjacent tiles horizontally
HEX_SPACING_Y = int(HEX_LENGTH*1.8)  # Spacing between adjacent tiles vertically

# Constants for colors
GREEN = (50, 175, 40)
GRAY = (75, 75, 75)
WHITE = (255, 255, 255)
RED = (180, 40, 30)