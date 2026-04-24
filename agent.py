# agent.py
from astar import astar_search
from config import GRID_SIZE

class CarAgent:
    def __init__(self, start_pos, goal_pos):
        self.pos = start_pos
        self.goal = goal_pos
        self.path = []
        self.path_index = 0

    def plan_path(self, obstacles):
        """Calculate or recalculate the path using A*."""
        self.path = astar_search(self.pos, self.goal, GRID_SIZE, obstacles)
        self.path_index = 0
        return self.path

    def move(self, environment):
        """Move the car one step along the path if possible."""
        if environment.signal_state == "RED":
            return self.pos, "WAITING_SIGNAL"

        if not self.path or self.path_index >= len(self.path) - 1:
            return self.pos, "REACHED_GOAL" if self.pos == self.goal else "IDLE"

        next_pos = self.path[self.path_index + 1]

        # Check if next move is blocked (e.g., dynamic obstacle added)
        if environment.is_obstacle(next_pos):
            # Re-plan!
            self.plan_path(environment.obstacles)
            if not self.path:
                return self.pos, "BLOCKED_NO_PATH"
            # After replanning, our current position is path[0], so next is path[1]
            if len(self.path) > 1:
                next_pos = self.path[1]
                self.path_index = 1
                self.pos = next_pos
                return self.pos, "RE-ROUTING"
            else:
                 return self.pos, "BLOCKED"

        self.path_index += 1
        self.pos = next_pos
        return self.pos, "MOVING"
