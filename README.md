# Uni Survivor 🎓🤖

A Python-based AI campus simulation and game built with **Pygame** and **AIMA-Python**[cite: 1, 2]. Experience a simulated university day balancing personal survival stats while autonomous NPC students navigate the campus using artificial intelligence search algorithms[cite: 1].

---

## ✨ Features

- **Autonomous NPC Students:** NPCs independently monitor their stats, decide on activities (Rest, Study, Socialize, Attend Class), select targets, and execute pathfinding routines[cite: 1, 3, 4].
- **AIMA Pathfinding Integration:** Implements Breadth-First Search (BFS) via the AIMA library (`aima-python`) using a custom `CampusPathProblem` class[cite: 2].
- **Dynamic Player Goals & HUD:** Real-time stat tracking (Energy, Stress, Focus, Grade) with dynamic goal recommendations and pressure events that test decision-making[cite: 1, 4].
- **Accelerated Virtual Day Loop:** A full campus day compressed into a dynamic 10-minute simulation (8:00 AM – 6:00 PM)[cite: 1, 4].
- **Environment & Obstacle Handling:** Automatic mapping of world boundaries, campus structures, and obstacles into grid-safe blocked coordinates[cite: 3].

---

## 🛠️ Tech Stack & Requirements

- **Language:** Python[cite: 1]
- **Graphics & UI:** Pygame[cite: 1, 4]
- **AI Core:** AIMA-Python library (`breadth_first_graph_search`, `Problem`)[cite: 2]

---

## 📂 Project Structure

| File | Description |
| :--- | :--- |
| `main.py` | Controls the primary game loop and integrates all subsystems[cite: 4]. |
| `Ai_agent.py` | Core AI module: state decisions, AIMA integration, `CampusPathProblem`, and BFS execution[cite: 2, 4]. |
| `npc.py` | Manages autonomous NPC behavior, destination selection, and activity cycles[cite: 3, 4]. |
| `player.py` | Handles player movement, collision detection, and core statistics[cite: 4]. |
| `Map.py` | Defines the campus layout and obstacle grids used for pathfinding[cite: 3, 4]. |
| `events.py` | Manages university pressure events and choice consequences[cite: 4]. |
| `game_state.py` | Controls the virtual day clock (8 AM to 6 PM)[cite: 4]. |
| `hud.py` | Displays stats, AI recommendations, dynamic goals, and messages[cite: 4]. |
| `camera.py` / `Config.py` | Handles viewport tracking and global configurations[cite: 4]. |

---

## 🧠 How the AI Works

The AI design cleanly separates high-level decision making from low-level pathfinding:
1. **Perceive & Decide:** The agent evaluates its stats (Energy, Stress, Focus, Grade) to select a goal activity[cite: 1, 3].
2. **Search (AIMA BFS):** Once a target destination is chosen, a custom `CampusPathProblem` is initialized, and AIMA's `breadth_first_graph_search` evaluates the campus grid state-by-state while avoiding obstacles[cite: 2, 3].
3. **Act:** The NPC converts the resulting grid path back into world coordinates and navigates step-by-step to the location[cite: 3].

---

## 🚀 Getting Started

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/GhaidaaIssa/University-Survivor-Game-.git](https://github.com/GhaidaaIssa/University-Survivor-Game-.git)
   cd Uni-Survivor-Game
