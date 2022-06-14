class Action:
    pass


class EscapeAction(Action):  # For when the player hits ESC
    pass


class MovementAction(Action):  # For when the player wants to move
    def __init__(self, dx: int, dy: int):
        super().__init__()
        self.dx = dx
        self.dy = dy
