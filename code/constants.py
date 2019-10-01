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
WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 720
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
BLACK = (0, 0, 0)
DARK_GRAY = (30, 30, 30)

# Constants representing discrete states
GREEN_STATE = 1
BLACK_STATE = 0

# UI parameters
UI_ELEMENT_WIDTH = 200
UI_ELEMENT_HEIGHT = 100
UI_ELEMENT_SIZE = (UI_ELEMENT_WIDTH, UI_ELEMENT_HEIGHT)
