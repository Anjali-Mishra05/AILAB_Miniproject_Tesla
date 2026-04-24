# Tesla Autonomous AI Simulation 🚗

> A mini self-driving car simulation built with Python and Pygame demonstrating path planning (A\*), obstacle avoidance, dynamic rerouting, and real-time traffic signal decision-making on a grid-based environment.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Simulation](#running-the-simulation)
- [Controls](#controls)
- [How It Works](#how-it-works)
  - [A\* Pathfinding Algorithm](#a-pathfinding-algorithm)
  - [Dynamic Re-routing](#dynamic-re-routing)
  - [Traffic Signal Logic](#traffic-signal-logic)
  - [Agent Decision-Making](#agent-decision-making)
  - [Grid Environment](#grid-environment)
- [Configuration](#configuration)
- [Module Reference](#module-reference)
- [Troubleshooting](#troubleshooting)
- [Known Limitations](#known-limitations)
- [Future Improvements](#future-improvements)
- [License](#license)

---

## Overview

This project simulates a Tesla-inspired autonomous vehicle navigating a 2D grid-based road map. The car uses the **A\* (A-star) search algorithm** to compute the optimal path from a start cell to a goal cell. When new obstacles are introduced at runtime, the car immediately recalculates a fresh route — mimicking how a real autonomous vehicle would respond to sudden changes in the environment.

The simulation also includes a basic **traffic signal system**: the car halts when it encounters a red light and resumes once the signal turns green. All of this is rendered in real time using **Pygame**, with color-coded cells representing roads, obstacles, the planned path, the car, and signals.

---

## Features

| Feature | Description |
|---|---|
| **A\* Pathfinding** | Computes the shortest, obstacle-free path from start to goal using heuristic search |
| **Dynamic Re-routing** | Re-plans the path in real time whenever a new obstacle blocks the current route |
| **Traffic Signal Logic** | Car stops at red lights; proceeds on green |
| **Interactive Obstacles** | Add obstacles with a key press or by clicking any grid cell |
| **Pause / Resume** | Freeze and unfreeze the simulation at any time |
| **Visual Grid Display** | Color-coded cells for roads, obstacles, path, car position, start, and goal |
| **Configurable Constants** | All colors, sizes, and speeds are editable in `config.py` |

---

## Project Structure

```
AILAB_Miniproject_Tesla/
│
├── main.py            # Entry point — simulation loop, rendering, event handling
├── agent.py           # Car agent — movement logic, state, decision-making
├── environment.py     # Grid map — obstacle management, traffic signals
├── astar.py           # A* pathfinding algorithm implementation
├── config.py          # Global constants — colors, grid size, FPS, speeds
├── requirements.txt   # Python dependency list
└── README.md          # This file
```

### File Responsibilities at a Glance

| File | Responsibility |
|---|---|
| `main.py` | Initialises Pygame, runs the game loop, dispatches events, draws the grid |
| `agent.py` | Represents the car: holds position, follows the computed path, checks signals |
| `environment.py` | Owns the grid state: which cells are obstacles, where the signal is, its current color |
| `astar.py` | Pure pathfinding — takes a grid, start, and goal; returns a list of (row, col) waypoints |
| `config.py` | Single source of truth for all magic numbers and color tuples |

---

## Prerequisites

| Requirement | Minimum Version | Notes |
|---|---|---|
| Python | 3.8+ | 3.10+ recommended |
| pip | 21+ | Bundled with Python 3.8+ |
| Pygame | 2.0+ | Installed via `requirements.txt` |
| OS | Windows / macOS / Linux | Any desktop OS with display support |

> **Headless servers:** Pygame requires a display. If you are on a server without a monitor, set up a virtual framebuffer (e.g., `Xvfb`) or run locally.

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/AILAB_Miniproject_Tesla.git
cd AILAB_Miniproject_Tesla
```

### 2. (Recommended) Create a virtual environment

```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
python3 -m pip install -r requirements.txt
```

The `requirements.txt` should contain at minimum:

```
pygame>=2.0.0
```

---

## Running the Simulation

```bash
python3 main.py
```

A Pygame window will open showing the grid. The car starts at the **Start** cell and will begin moving along the calculated A\* path once the simulation is unpaused.

---

## Controls

| Input | Action |
|---|---|
| `SPACE` | Start / Pause the simulation |
| `O` key | Add a random obstacle to the grid |
| `T` key | Toggle the traffic signal between Red and Green |
| **Mouse Click** | Add an obstacle at the clicked grid cell |
| `ESC` / Close window | Quit the simulation |

> **Note:** Clicking on the car's current cell, the start cell, or the goal cell has no effect — only empty road cells can become obstacles.

---

## How It Works

### A\* Pathfinding Algorithm

**File:** `astar.py`

A\* is an informed search algorithm that finds the shortest path between two nodes in a graph. It combines:

- **g(n)** — the actual cost to reach node `n` from the start
- **h(n)** — a heuristic estimate of the cost from `n` to the goal
- **f(n) = g(n) + h(n)** — the total estimated cost

The implementation uses the **Manhattan distance** as the heuristic, which is optimal for a 4-directional grid (no diagonal movement):

```
h(n) = |current_row - goal_row| + |current_col - goal_col|
```

**Algorithm steps:**

1. Push the start cell onto a min-heap (priority queue) with `f = 0`.
2. Pop the cell with the lowest `f` score.
3. If it is the goal, reconstruct and return the path.
4. For each of the 4 neighbours (up, down, left, right):
   - Skip if it is a wall/obstacle or out of bounds.
   - Calculate tentative `g` score.
   - If this `g` is lower than previously recorded, update and push to the heap.
5. If the heap empties with no solution, return `None` (no path exists).

**Return value:** An ordered list of `(row, col)` tuples from start to goal, or `None` if blocked.

---

### Dynamic Re-routing

**Files:** `main.py`, `agent.py`, `astar.py`

Every time a new obstacle is placed (via key press or mouse click), the simulation:

1. Updates the grid in `environment.py` to mark the new cell as blocked.
2. Calls `astar.find_path()` again with the current car position as the new start.
3. If a path is found, updates the agent's waypoint list.
4. If no path exists (car is completely surrounded), the car halts and waits.

This re-routing happens synchronously within the event loop, so the car path updates on the very next frame.

---

### Traffic Signal Logic

**File:** `environment.py`, `agent.py`

- The grid contains a single traffic signal cell at a fixed position.
- The signal has two states: **Red** and **Green**.
- On every movement step, before advancing to the next waypoint, the agent checks:
  - Is the next cell the signal cell?
  - If yes, is the signal **Red**?
  - If both are true, the car holds its position until the signal turns Green.
- Pressing `T` toggles the signal state instantly.

---

### Agent Decision-Making

**File:** `agent.py`

The `Agent` class holds:

- **`position`** — current `(row, col)` on the grid
- **`path`** — the list of upcoming waypoints returned by A\*
- **`moving`** — boolean flag controlled by SPACE

On each tick (when `moving` is `True`):

1. Check if `path` is non-empty.
2. Peek at the next waypoint.
3. Query the environment for signal state at that waypoint.
4. If clear, pop the waypoint and update `position`.
5. If blocked by signal, stay in place.

---

### Grid Environment

**File:** `environment.py`

The grid is a 2D list of cell states:

| State | Meaning |
|---|---|
| `0` | Open road |
| `1` | Obstacle / wall |
| `2` | Traffic signal |

The `Environment` class exposes methods to:

- `add_obstacle(row, col)` — mark a cell as blocked
- `toggle_signal()` — flip signal color
- `is_obstacle(row, col)` — query whether a cell is passable
- `get_signal_color()` — return current signal state

---

## Configuration

All tunable parameters live in `config.py`. Edit this file to change the look and feel of the simulation without touching any logic code.

```python
# config.py (example values — actual values may differ)

# Grid dimensions
GRID_ROWS = 20
GRID_COLS = 20
CELL_SIZE  = 30           # Pixels per grid cell

# Window
WINDOW_WIDTH  = GRID_COLS * CELL_SIZE
WINDOW_HEIGHT = GRID_ROWS * CELL_SIZE
FPS = 10                  # Frames per second (controls car speed)

# Colors (R, G, B)
COLOR_BACKGROUND = (30,  30,  30)
COLOR_ROAD       = (200, 200, 200)
COLOR_OBSTACLE   = (50,  50,  50)
COLOR_PATH       = (100, 180, 255)
COLOR_CAR        = (0,   220, 0  )
COLOR_START      = (0,   150, 0  )
COLOR_GOAL       = (220, 0,   0  )
COLOR_SIGNAL_RED = (255, 0,   0  )
COLOR_SIGNAL_GRN = (0,   255, 0  )
```

| Constant | Effect |
|---|---|
| `GRID_ROWS` / `GRID_COLS` | Size of the navigable map |
| `CELL_SIZE` | Visual size of each cell in pixels |
| `FPS` | Lower values slow the car down; higher values speed it up |
| `COLOR_*` | Any cell or UI element color |

---

## Module Reference

### `main.py`

```
main()
  └── Initialise Pygame and create window
  └── Instantiate Environment and Agent
  └── Compute initial A* path
  └── Game loop:
        ├── handle_events()   → keyboard / mouse input
        ├── update()          → advance agent if moving
        └── draw()            → render grid, path, agent, signal
```

### `agent.py`

```
class Agent
  ├── __init__(start_pos)
  ├── set_path(path)         → load new waypoint list
  ├── step(environment)      → move one cell (respects signals)
  └── get_position()         → returns current (row, col)
```

### `environment.py`

```
class Environment
  ├── __init__(rows, cols)
  ├── add_obstacle(row, col)
  ├── add_random_obstacle()
  ├── toggle_signal()
  ├── is_obstacle(row, col)  → bool
  ├── get_signal_color()     → "red" | "green"
  └── get_grid()             → 2D list
```

### `astar.py`

```
find_path(grid, start, goal)
  └── Returns: list of (row, col) tuples | None
```

### `config.py`

```
GRID_ROWS, GRID_COLS, CELL_SIZE, FPS
COLOR_BACKGROUND, COLOR_ROAD, COLOR_OBSTACLE,
COLOR_PATH, COLOR_CAR, COLOR_START, COLOR_GOAL,
COLOR_SIGNAL_RED, COLOR_SIGNAL_GRN
```

---

## Troubleshooting

| Problem | Likely Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: pygame` | Pygame not installed | Run `pip install -r requirements.txt` |
| Window does not open on Linux server | No display detected | Use `export DISPLAY=:0` or set up Xvfb |
| Car stops and does not move | No path found — obstacles surround it | Press `O` to add an obstacle elsewhere, or restart |
| Simulation runs too fast / slow | FPS too high / low | Reduce / increase `FPS` in `config.py` |
| `pygame.error: No video mode has been set` | Pygame init order issue | Ensure `pygame.display.set_mode()` is called before any draw operations |
| Car ignores traffic signal | Signal cell position mismatch | Verify the signal cell coordinates in `environment.py` match those in `config.py` |

---

## Known Limitations

- **Single agent only** — the simulation supports one car at a time.
- **Static goal** — the destination cell is fixed at launch and cannot be changed at runtime via UI.
- **4-directional movement** — the car cannot move diagonally.
- **One traffic signal** — only a single signal node is supported in the current grid.
- **No persistence** — obstacle layouts reset on every run; there is no save/load feature.

---

## Future Improvements

- [ ] Multi-agent support with collision avoidance between cars
- [ ] Dijkstra and BFS algorithm toggle for comparison
- [ ] Draggable start and goal cells via mouse
- [ ] Multiple traffic signals with timed automatic cycling
- [ ] Save and load custom grid layouts (JSON)
- [ ] Speed control slider in the UI
- [ ] Step-by-step debug mode showing A\* open/closed sets

---

## License

This project was created as part of an AI Lab mini-project. All code is provided for educational purposes.

---

*Built with Python 🐍 and Pygame 🎮*