import tcod

from actions import EscapeAction, MovementAction
from input_handlers import EventHandler


def main() -> None:  # -> None indicates we do not return anything
    screen_width = 80  # Define screen width
    screen_height = 50  # Define screen height

    player_x = int(screen_width / 2)  # Get player coordinates
    player_y = int(screen_height / 2)

    tileset = tcod.tileset.load_tilesheet(  # Telling tcod which font to use
        "Icons.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    event_handler = EventHandler()  # Used to receive events and process them

    with tcod.context.new_terminal(  # Create the screen with given dimensions, tileset, and title
            screen_width,
            screen_height,
            tileset=tileset,
            title="Testing Roguelite Program",
            vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")  # What we will draw to; F = [x, y]
        while True:  # "Game loop" - never ends until we quit
            root_console.print(x=player_x, y=player_y, string="@")  # Draw character to screen at given [x, y]
            context.present(root_console)  # Updates the window to show any changes
            root_console.clear()  # Clear the screen before we draw again
            for event in tcod.event.wait():  # Listens for events
                action = event_handler.dispatch(event)  # Sends the event to its proper place (ev_... in .py file)
                if action is None:
                    continue
                if isinstance(action, MovementAction):
                    player_x += action.dx
                    player_y += action.dy
                elif isinstance(action, EscapeAction):
                    raise SystemExit()


if __name__ == "__main__":
    main()
