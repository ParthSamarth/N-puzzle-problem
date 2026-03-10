# 🧩 8-Puzzle / N-Puzzle Solver (Python + Pygame)

An interactive sliding puzzle solver built using **Python**, **Pygame**, and **Pygame GUI**.  
Play, shuffle, resize, and automatically solve puzzles using heuristic search algorithms.

---

## 🚀 Features

- 🎮 Interactive graphical interface
- 🔀 Shuffle puzzle board
- 📏 Multiple puzzle sizes:
  - 3×3 (8-Puzzle)
  - 4×4 (15-Puzzle)
  - 5×5 (24-Puzzle)
- 🧠 Heuristic search algorithms:
  - A* Search (Manhattan Distance)
  - Best-First Search (Manhattan Distance)
- 📊 Algorithm performance report:
  - Visited nodes
  - Execution time
  - Number of steps
- 🎞️ Animated solution playback
- 🎨 Custom GUI theme
- 📦 Standalone executable build support

---

## 🛠️ Tech Stack

- Python 3
- Pygame
- pygame_gui
- NumPy
- cx_Freeze

---

## 📂 Project Structure
8-puzzle/
│
├── main.py # GUI application
├── puzzle.py # Puzzle logic & search algorithms
├── matrix.py # Matrix state & heuristics
├── colors.py # Color definitions
├── theme.json # GUI theme config
├── logo.png # App icon
├── FiraCode-Retina.ttf # Custom font
├── setup.py # Executable build script
└── README.md

---

## 🧠 How It Works

### Puzzle Representation
- The puzzle board is stored as a NumPy matrix.
- Each state keeps:
  - Manhattan distance
  - Previous state reference
  - Move direction
  - Path cost

### Heuristic Used — Manhattan Distance
h(n) = Σ |x_current - x_goal| + |y_current - y_goal|
