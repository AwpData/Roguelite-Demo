from __future__ import annotations

import random
from typing import Tuple, Iterator, TYPE_CHECKING, List

import tcod

import tile_types
from game_map import GameMap

if TYPE_CHECKING:
    from entity import Entity


# This file will be used to procedurally generate our dungeons

class RectangularRoom:  # Used to create a room
    def __init__(self, x: int, y: int, width: int, height: int):  # Get the top left and bottom right corner of the room
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property  # Remember property is like a class attribute; calling it = gets some info about the class
    def center(self) -> Tuple[int, int]:  # Gets the center of the room
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:  # Gets the area of the room to carve out
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)  # + 1 to ensure a wall between each room

    def intersects(self, other: RectangularRoom) -> bool:  # Check if two rooms overlap each other
        return self.x1 <= other.x2 and self.x2 >= other.x1 and self.y1 <= other.y2 and self.y2 >= other.y1


def tunnel_between(start: Tuple[int, int], end: Tuple[int, int]) -> Iterator[
    Tuple[int, int]]:  # Connects rooms together with an L-shaped tunnel
    x1, y1 = start  # Get the coordinates from the parameters of where to start / end the tunnel
    x2, y2 = end
    if random.random() < 0.5:  # 50% chance to move horizontally first then vertically
        corner_x, corner_y = x2, y1
    else:  # Vice versa
        corner_x, corner_y = x1, y2

    # Draw the bresenham lines which define our tunnel. We convert the points of the line into a list
    # and yield the results with a generator so we don't have to start from the beginning each time
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y


def generate_dungeon(max_rooms: int, room_min_size: int, room_max_size: int, map_width: int, map_height: int,
                     player: Entity) -> GameMap:  # Generate a new dungeon map
    dungeon = GameMap(map_width, map_height)
    rooms: List[RectangularRoom] = []  # Keep a list of all the current rooms

    for r in range(max_rooms):  # Run through all the rooms. Notice that we aren't guaranteed to have # of max rooms
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - dungeon.height - 1)
        y = random.randint(0, dungeon.width - dungeon.height - 1)

        new_room = RectangularRoom(x, y, room_width, room_height)  # Create a rectangular room

        # See if any room in our rooms lists happens to intersect with the generated room
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue  # If it does, try again

        dungeon.tiles[new_room.inner] = tile_types.floor  # Make the inner area of the new room walkable

        if len(rooms) == 0:  # Means this is the first room where the player starts so place them in the center of it
            player.x, player.y = new_room.center
        else:  # Not the first room anymore
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_types.floor

        rooms.append(new_room)  # Append this new room then to the list

    return dungeon
