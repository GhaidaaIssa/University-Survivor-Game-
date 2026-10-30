import pygame


# =========================================================
# STUDENT NPC
# =========================================================

class StudentNPC:

    def __init__(
        self,
        x,
        y,
        name,
        color,
        ai_agent,
        locations
    ):

        self.x = float(x)
        self.y = float(y)

        self.name = name
        self.color = color

        self.ai_agent = ai_agent
        self.locations = locations

        self.width = 34
        self.height = 42

        self.rect = pygame.Rect(
            int(self.x),
            int(self.y),
            self.width,
            self.height
        )

        self.speed = 55

        # =================================================
        # AI STATE
        # =================================================

        self.energy = 70.0
        self.focus = 70.0
        self.stress = 25.0
        self.grade = 65.0

        self.current_decision = (
            "ATTEND_CLASS"
        )

        self.current_place = ""

        # =================================================
        # PATH
        # =================================================

        self.path = []
        self.path_index = 0

        self.target = None

        self.target_choice_index = 0

        # =================================================
        # WAIT
        # =================================================

        self.wait_timer = 0.0
        self.wait_duration = 10.0

        self.recalculate_timer = 0.0

        # =================================================
        # AI TIMER
        # =================================================

        self.decision_timer = 0.0

    # =====================================================
    # SELECT LOCATION FROM AI DECISION
    # =====================================================

    def choose_target(
        self,
        obstacles
    ):

        self.current_decision = (
            self.ai_agent.decide(
                self
            )
        )

        if self.current_decision == "REST":

            choices = [
                "Cafeteria",
                "Student Center"
            ]

        elif self.current_decision == "STUDY":

            choices = [
                "Library",
                "Computer Lab",
                "AI Lab"
            ]

        elif self.current_decision == "SOCIALIZE":

            choices = [
                "Student Center",
                "Cafeteria"
            ]

        else:

            choices = [
                "Lecture Hall",
                "Science Lab",
                "AI Lab"
            ]

        place = choices[
            self.target_choice_index
            % len(choices)
        ]

        self.target_choice_index += 1

        self.current_place = place

        self.target = (
            self.locations[
                place
            ]
        )

        self.path = (
            self.ai_agent.find_path(
                self.x,
                self.y,
                self.target[0],
                self.target[1],
                obstacles
            )
        )

        self.path_index = 0

        self.recalculate_timer = 1.0

    # =====================================================
    # ACTIVITY EFFECT
    # =====================================================

    def complete_activity(self):

        if self.current_decision == "REST":

            self.energy += 15
            self.stress -= 10

        elif self.current_decision == "STUDY":

            self.grade += 4
            self.focus += 5
            self.energy -= 5

        elif (
            self.current_decision
            == "SOCIALIZE"
        ):

            self.stress -= 12
            self.energy += 3

        elif (
            self.current_decision
            == "ATTEND_CLASS"
        ):

            self.grade += 3
            self.focus += 3
            self.energy -= 5

        self.energy = max(
            0,
            min(100, self.energy)
        )

        self.stress = max(
            0,
            min(100, self.stress)
        )

        self.focus = max(
            0,
            min(100, self.focus)
        )

        self.grade = max(
            0,
            min(100, self.grade)
        )

    # =====================================================
    # UPDATE
    # =====================================================

    def update(
        self,
        dt,
        obstacles
    ):

        # Natural NPC changes
        self.energy -= 0.02 * dt
        self.stress += 0.01 * dt

        # =================================================
        # WAITING
        # =================================================

        if self.wait_timer > 0:

            self.wait_timer -= dt

            if self.wait_timer <= 0:

                self.wait_timer = 0

                self.complete_activity()

                self.choose_target(
                    obstacles
                )

            return

        # =================================================
        # FIRST TARGET
        # =================================================

        if self.target is None:

            self.choose_target(
                obstacles
            )

            return

        # =================================================
        # NO PATH
        # =================================================

        if not self.path:

            self.choose_target(
                obstacles
            )

            return

        # =================================================
        # FINISHED PATH
        # =================================================

        if self.path_index >= len(
            self.path
        ):

            self.x = float(
                self.target[0]
            )

            self.y = float(
                self.target[1]
            )

            self.rect.x = int(
                self.x
            )

            self.rect.y = int(
                self.y
            )

            self.wait_timer = (
                self.wait_duration
            )

            return

        # =================================================
        # CURRENT WAYPOINT
        # =================================================

        target_x, target_y = (
            self.path[
                self.path_index
            ]
        )

        dx = target_x - self.x
        dy = target_y - self.y

        distance = (
            dx * dx
            + dy * dy
        ) ** 0.5

        # =================================================
        # REACHED WAYPOINT
        # =================================================

        if distance < 8:

            self.x = target_x
            self.y = target_y

            self.rect.x = int(
                self.x
            )

            self.rect.y = int(
                self.y
            )

            self.path_index += 1

            if self.path_index >= len(
                self.path
            ):

                self.x = float(
                    self.target[0]
                )

                self.y = float(
                    self.target[1]
                )

                self.rect.x = int(
                    self.x
                )

                self.rect.y = int(
                    self.y
                )

                self.wait_timer = (
                    self.wait_duration
                )

            return

        # =================================================
        # MOVEMENT
        # =================================================

        if distance == 0:
            return

        move_x = (
            dx / distance
        ) * self.speed * dt

        move_y = (
            dy / distance
        ) * self.speed * dt

        old_x = self.x
        old_y = self.y

        # X
        self.x += move_x

        self.rect.x = int(
            self.x
        )

        blocked_x = any(
            self.rect.colliderect(
                obstacle
            )
            for obstacle in obstacles
        )

        if blocked_x:

            self.x = old_x

            self.rect.x = int(
                self.x
            )

        # Y
        self.y += move_y

        self.rect.y = int(
            self.y
        )

        blocked_y = any(
            self.rect.colliderect(
                obstacle
            )
            for obstacle in obstacles
        )

        if blocked_y:

            self.y = old_y

            self.rect.y = int(
                self.y
            )

        # =================================================
        # RECALCULATE USING AIMA
        # =================================================

        if blocked_x or blocked_y:

            self.recalculate_timer -= dt

            if self.recalculate_timer <= 0:

                self.path = (
                    self.ai_agent.find_path(
                        self.x,
                        self.y,
                        self.target[0],
                        self.target[1],
                        obstacles
                    )
                )

                self.path_index = 0

                self.recalculate_timer = 1.0

    # =====================================================
    # DRAW
    # =====================================================

    def draw(
        self,
        screen,
        camera
    ):

        screen_x, screen_y = (
            camera.apply_position(
                self.x,
                self.y
            )
        )

        # Shadow
        pygame.draw.ellipse(
            screen,
            (50, 50, 50),
            (
                int(screen_x + 4),
                int(screen_y + 34),
                26,
                8
            )
        )

        # Backpack
        pygame.draw.rect(
            screen,
            (90, 55, 35),
            (
                int(screen_x + 3),
                int(screen_y + 16),
                10,
                18
            ),
            border_radius=4
        )

        # Body
        pygame.draw.rect(
            screen,
            self.color,
            (
                int(screen_x + 8),
                int(screen_y + 15),
                20,
                20
            ),
            border_radius=6
        )

        # Head
        pygame.draw.ellipse(
            screen,
            (225, 180, 145),
            (
                int(screen_x + 9),
                int(screen_y + 2),
                18,
                18
            )
        )

        # Hair
        pygame.draw.arc(
            screen,
            (45, 30, 25),
            (
                int(screen_x + 9),
                int(screen_y + 1),
                18,
                8
            ),
            3.14,
            6.28,
            5
        )

        # Legs
        pygame.draw.rect(
            screen,
            (45, 45, 55),
            (
                int(screen_x + 10),
                int(screen_y + 34),
                6,
                8
            ),
            border_radius=2
        )

        pygame.draw.rect(
            screen,
            (45, 45, 55),
            (
                int(screen_x + 19),
                int(screen_y + 34),
                6,
                8
            ),
            border_radius=2
        )

        # Name
        font = pygame.font.Font(
            None,
            18
        )

        name_surface = font.render(
            self.name,
            True,
            (255, 255, 255)
        )

        name_rect = (
            name_surface.get_rect(
                center=(
                    int(
                        screen_x
                        + self.width / 2
                    ),
                    int(
                        screen_y - 9
                    )
                )
            )
        )

        pygame.draw.rect(
            screen,
            (30, 30, 35),
            name_rect.inflate(
                6,
                4
            ),
            border_radius=4
        )

        screen.blit(
            name_surface,
            name_rect
        )

        # AI decision
        small_font = pygame.font.Font(
            None,
            14
        )

        decision_surface = (
            small_font.render(
                self.current_decision,
                True,
                (255, 225, 90)
            )
        )

        decision_rect = (
            decision_surface.get_rect(
                center=(
                    int(
                        screen_x
                        + self.width / 2
                    ),
                    int(
                        screen_y + 51
                    )
                )
            )
        )

        screen.blit(
            decision_surface,
            decision_rect
        )


# =========================================================
# CREATE STUDENTS
# =========================================================

def create_students(ai_agent):

    locations = {

        "Library":
        (230, 308),

        "Computer Lab":
        (905, 293),

        "Science Lab":
        (1485, 318),

        "Lecture Hall":
        (240, 843),

        "AI Lab":
        (900, 843),

        "Student Center":
        (1500, 843),

        "Cafeteria":
        (605, 1123),

        "Administration":
        (1190, 1123)
    }

    students = [

        StudentNPC(
            520,
            270,
            "Sara",
            (185, 95, 150),
            ai_agent,
            locations
        ),

        StudentNPC(
            720,
            530,
            "Omar",
            (70, 130, 200),
            ai_agent,
            locations
        ),

        StudentNPC(
            1200,
            520,
            "Lina",
            (80, 165, 110),
            ai_agent,
            locations
        ),

        StudentNPC(
            850,
            850,
            "Ahmed",
            (210, 150, 65),
            ai_agent,
            locations
        ),

        StudentNPC(
            1500,
            520,
            "Noor",
            (145, 100, 190),
            ai_agent,
            locations
        )
    ]

    return students