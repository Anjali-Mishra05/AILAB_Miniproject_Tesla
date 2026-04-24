# environment.py
import random
from config import GRID_SIZE

class Environment:
    def __init__(self):
        self.grid_size = GRID_SIZE
        self.obstacles = set()
        self.signal_state = "GREEN" # GREEN or RED
        self.start_pos = (0, 0)
        self.goal_pos = (GRID_SIZE - 1, GRID_SIZE - 1)
        self.reset_environment()

    def reset_environment(self):
        self.obstacles = set()
        # Add some initial fixed obstacles
        for _ in range(int(GRID_SIZE * GRID_SIZE * 0.15)):
            obs = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
            if obs != self.start_pos and obs != self.goal_pos:
                self.obstacles.add(obs)

    def add_obstacle(self, pos):
        if pos != self.start_pos and pos != self.goal_pos:
            self.obstacles.add(pos)
            return True
        return False

    def toggle_signal(self):
        self.signal_state = "RED" if self.signal_state == "GREEN" else "GREEN"
        return self.signal_state

    def is_obstacle(self, pos):
        return pos in self.obstacles
