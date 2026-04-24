# Tesla Autonomous AI Simulation 🚗

A mini self-driving car simulation built with Python and Pygame. This project demonstrates path planning (A*), obstacle avoidance, and real-time decision making.

## 🚀 How to Run
1. Ensure you have the dependencies installed:
   ```bash
   python3 -m pip install -r requirements.txt
   ```
2. Run the simulation:
   ```bash
   python3 main.py
   ```

## 🎮 Demo Controls
* **SPACE**: Start / Pause the simulation.
* **'O' Key**: Add a random obstacle to the grid.
* **'T' Key**: Toggle the traffic signal (Red/Green).
* **Mouse Click**: Add an obstacle at a specific grid position.

## 🧠 Key Features
* **A* Pathfinding**: The car calculates the most efficient route from Start to Goal.
* **Dynamic Re-routing**: If an obstacle is placed in the path, the car automatically recalculates a new route in real-time.
* **Traffic Logic**: The car respects signals and waits for Green before proceeding.
* **Visual Perception**: Clear grid-based representation of roads, obstacles, and the car's planned path.

## 📂 Project Structure
* `main.py`: The core simulation loop and visualization.
* `agent.py`: Car logic, movement, and decision-making.
* `environment.py`: Grid management, obstacles, and signals.
* `astar.py`: Pathfinding algorithm implementation.
* `config.py`: Colors, grid sizes, and game constants.
