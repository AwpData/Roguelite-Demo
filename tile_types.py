from typing import Tuple

import numpy as np

# This file contains the tile information that makes up the GameMap

graphic_dt = np.dtype(  # Create the datatype for NumPy for a graphic. It takes a character, and a FG and BG color (RGB)
    [
        ("ch", np.int32),
        ("fg", "3B"),
        ("bg", "3B"),
    ]
)

tile_dt = np.dtype(  # Create the tile datatype for NumPy. Can we walk or see it? Dark holds the graphic dt
    [
        ("walkable", np.bool),
        ("transparent", np.bool),
        ("dark", graphic_dt),
    ]
)


def new_tile(  # Helper function for defining individual tile types
        *,  # Forces use of keywords
        walkable: int,
        transparent: int,
        dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    return np.array((walkable, transparent, dark), dtype=tile_dt)


floor = new_tile(  # Define the floor tiles
    walkable=True, transparent=True, dark=(ord(" "), (255, 255, 255), (50, 50, 150)),
)

wall = new_tile(  # Define wall tiles
    walkable=False, transparent=False, dark=(ord(" "), (255, 255, 255), (0, 0, 100)),
)
