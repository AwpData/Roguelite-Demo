from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Engine import Engine
    from entity import Entity


class Action:
    def perform(self, engine: Engine, entity: Entity) -> None:  # Perform the desired action in engine on some entity
        raise NotImplementedError()  # Must be implemented in the subclasses


class EscapeAction(Action):  # For when the player hits ESC
    def perform(self, engine: Engine, entity: Entity) -> None:
        raise SystemExit()  # Quit the game


class MovementAction(Action):  # For when the player wants to move
    def __init__(self, dx: int, dy: int):
        super().__init__()
        self.dx = dx
        self.dy = dy

    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if not engine.game_map.in_bounds(dest_x, dest_y):
            return  # Destination is out of bounds
        if not engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return  # Destination blocked by a tile

        entity.move(self.dx, self.dy)
