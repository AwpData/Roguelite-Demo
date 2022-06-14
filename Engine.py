from typing import Set, Iterable, Any

from tcod.console import Console
from tcod.context import Context

from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler


class Engine:  # Responsible for drawing the map, entities, and handling player input
    def __init__(self, entities: Set[Entity], event_handler: EventHandler, game_map: GameMap, player: Entity):
        self.entities = entities  # All entities (a set of them) we will want to handle
        self.event_handler = event_handler  # Handles events
        self.game_map = game_map
        self.player = player

    def handle_events(self, events: Iterable[Any]) -> None:  # Handles events listened to from main.py
        for event in events:  # Handles events based on action type (if any)
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            action.perform(self, self.player)  # Since action has type checking, it will automatically perform the event

    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)  # Draw the game map first
        for entity in self.entities:  # Print the entities in their respective positions, image, and color
            console.print(entity.x, entity.y, entity.char, fg=entity.color)

        context.present(console)  # Updates the window
        console.clear()  # Clear the screen for next time we move things around
