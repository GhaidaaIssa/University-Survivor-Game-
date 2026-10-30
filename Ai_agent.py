import os
import sys

# =========================================================
# CONNECT AIMA
# =========================================================

PROJECT_FOLDER = os.path.dirname(os.path.abspath(__file__))
AIMA_FOLDER = os.path.join(PROJECT_FOLDER, "aima-python")

if AIMA_FOLDER not in sys.path:
    sys.path.insert(0, AIMA_FOLDER)

from aima.search import Problem, breadth_first_graph_search



# CAMPUS PATH PROBLEM


class CampusPathProblem(Problem):

    def __init__(self, start, goal, blocked):
        super().__init__(start, goal)
        self.blocked = blocked

    def actions(self, state):

        x, y = state

        moves = [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1)
        ]

        valid_moves = []

        for nx, ny in moves:

            if nx < 0 or nx > 44:
                continue

            if ny < 0 or ny > 29:
                continue

            if (nx, ny) in self.blocked:
                continue

            valid_moves.append((nx, ny))

        return valid_moves

    def result(self, state, action):
        return action


# =========================================================
# AI AGENT
# =========================================================

class AIAgent:

    GRID_SIZE = 40
    HALF_WIDTH = 17
    HALF_HEIGHT = 21

    def __init__(self):
        print("AIMA AI Agent initialized")

    # =====================================================
    # WORLD -> GRID
    # =====================================================

    def world_to_grid(self, x, y):

        return (
            int(x // self.GRID_SIZE),
            int(y // self.GRID_SIZE)
        )

    # =====================================================
    # GRID -> WORLD
    # =====================================================

    def grid_to_world(self, position):

        gx, gy = position

        return (
            gx * self.GRID_SIZE + 20,
            gy * self.GRID_SIZE + 20
        )

    # =====================================================
    # COLLISION CHECK
    # =====================================================

    def position_blocked(self, x, y, obstacles):

        left = x - self.HALF_WIDTH
        right = x + self.HALF_WIDTH

        top = y - self.HALF_HEIGHT
        bottom = y + self.HALF_HEIGHT

        for obstacle in obstacles:

            if (
                right > obstacle.left
                and left < obstacle.right
                and bottom > obstacle.top
                and top < obstacle.bottom
            ):
                return True

        return False

    # =====================================================
    # BLOCKED GRID
    # =====================================================

    def create_blocked_grid(self, obstacles):

        blocked = set()

        for gx in range(45):
            for gy in range(30):

                x = gx * self.GRID_SIZE + 20
                y = gy * self.GRID_SIZE + 20

                if self.position_blocked(
                    x,
                    y,
                    obstacles
                ):
                    blocked.add((gx, gy))

        return blocked

    # =====================================================
    # NEAREST FREE CELL
    # =====================================================

    def find_nearest_free_cell(
        self,
        position,
        blocked
    ):

        gx, gy = position

        if (
            0 <= gx <= 44
            and 0 <= gy <= 29
            and (gx, gy) not in blocked
        ):
            return (gx, gy)

        for distance in range(1, 10):

            for dx in range(
                -distance,
                distance + 1
            ):

                for dy in range(
                    -distance,
                    distance + 1
                ):

                    nx = gx + dx
                    ny = gy + dy

                    if nx < 0 or nx > 44:
                        continue

                    if ny < 0 or ny > 29:
                        continue

                    if (nx, ny) not in blocked:
                        return (nx, ny)

        return None

    # =====================================================
    # AIMA BFS PATHFINDING
    # =====================================================

    def find_path(
        self,
        start_x,
        start_y,
        goal_x,
        goal_y,
        obstacles
    ):

        start = self.world_to_grid(
            start_x,
            start_y
        )

        goal = self.world_to_grid(
            goal_x,
            goal_y
        )

        blocked = self.create_blocked_grid(
            obstacles
        )

        safe_start = self.find_nearest_free_cell(
            start,
            blocked
        )

        safe_goal = self.find_nearest_free_cell(
            goal,
            blocked
        )

        if safe_start is None:
            return []

        if safe_goal is None:
            return []

        blocked.discard(safe_start)
        blocked.discard(safe_goal)

        problem = CampusPathProblem(
            safe_start,
            safe_goal,
            blocked
        )

        try:

            result = breadth_first_graph_search(
                problem
            )

            if result is None:
                return []

            solution = result.solution()

            path = []

            for position in solution:

                path.append(
                    self.grid_to_world(
                        position
                    )
                )

            return path

        except Exception as error:

            print(
                "AIMA pathfinding error:",
                error
            )

            return []

    # =====================================================
    # AI DECISION MAKING
    # =====================================================

    def decide(self, agent):

        # Critical energy
        if agent.energy <= 25:
            return "REST"

        # Critical stress
        if agent.stress >= 75:
            return "REST"

        # Academic problem
        if agent.grade < 60:
            return "STUDY"

        # Low concentration
        if agent.focus < 40:
            return "STUDY"

        # Moderate pressure
        if agent.stress >= 55:
            return "SOCIALIZE"

        # Normal state
        return "ATTEND_CLASS"

    # =====================================================
    # EXPLAIN AI DECISION
    # =====================================================

    def explain_decision(self, agent):

        decision = self.decide(agent)

        if decision == "REST":

            if agent.energy <= 25:
                reason = "Energy is low. Rest is recommended."
            else:
                reason = "Stress is high. Rest is recommended."

        elif decision == "STUDY":

            if agent.grade < 60:
                reason = "Grade is low. Studying is recommended."
            else:
                reason = "Focus is low. Studying may improve performance."

        elif decision == "SOCIALIZE":

            reason = (
                "Stress is increasing. "
                "A social break may reduce pressure."
            )

        else:

            reason = (
                "Current condition is stable. "
                "Attending class is recommended."
            )

        return decision, reason