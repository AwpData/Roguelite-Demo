import tcod

from Engine import Engine
from entity import Entity
from input_handlers import EventHandler
from procgen import generate_dungeon


def main() -> None:  # -> None indicates we do not return anything
    screen_width = 80 # Define screen width
    screen_height = 50  # Define screen height

    map_width = 80
    map_height = 45

    # Define the max and min room size, and number of rooms each dungeon will have
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    tileset = tcod.tileset.load_tilesheet(  # Telling tcod which font to use
        "Icons.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    event_handler = EventHandler()  # Used to receive events and process them

    player = Entity(int(screen_width / 2), int(screen_height / 2), "@", (255, 255, 255))  # Create the player
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), "@", (255, 255, 0))  # Create the npc
    entities = {npc, player}  # Entities will be a set of objects in our map

    # Create the map for the game
    game_map = generate_dungeon(max_rooms, room_min_size, room_max_size, map_width, map_height, player)
    engine = Engine(entities=entities, event_handler=event_handler, game_map=game_map, player=player)

    with tcod.context.new_terminal(  # Create the screen with given dimensions, tileset, and title
            screen_width,
            screen_height,
            tileset=tileset,
            title="Testing Roguelite Program",
            vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")  # What we will draw to; F = [x, y]
        while True:  # "Game loop" - never ends until we quit
            engine.render(console=root_console, context=context)  # Render the screen to the window
            events = tcod.event.wait()  # Wait for some events
            engine.handle_events(events)  # Send events to engine for handling


if __name__ == "__main__":
    main()
