from typing import Optional  # Optional means that we don't have to have an action, but this is an optional import

import tcod.event

from actions import Action, MovementAction, EscapeAction


class EventHandler(
    tcod.event.EventDispatch[Action]):  # Subclass of tcod's EventDispatch (allows sending events to proper methods)
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:  # Override quit function (which is empty)
        raise SystemExit

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:  # Override keydown function (which is empty)
        action: Optional[Action] = None
        key = event.sym

        if key == tcod.event.K_UP:
            action = MovementAction(dx=0, dy=-1)
        elif key == tcod.event.K_DOWN:
            action = MovementAction(dx=0, dy=1)
        elif key == tcod.event.K_RIGHT:
            action = MovementAction(dx=1, dy=0)
        elif key == tcod.event.K_LEFT:
            action = MovementAction(dx=-1, dy=0)
        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction()

        return action
