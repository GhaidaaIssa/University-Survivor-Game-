import pygame

from Config import PLAYER_SPEED


class Player:

    def __init__(self, x, y):

        self.rect = pygame.Rect(
            x,
            y,
            40,
            48
        )

        self.speed = PLAYER_SPEED

        self.direction = "down"

        self.animation_frame = 0
        self.animation_timer = 0.0

        # ================================================
        # PLAYER STATS
        # ================================================

        self.energy = 100.0
        self.focus = 85.0
        self.stress = 15.0
        self.grade = 70.0

    # ====================================================
    # KEEP STATS BETWEEN 0 AND 100
    # ====================================================

    def clamp_stats(self):

        self.energy = max(
            0.0,
            min(100.0, self.energy)
        )

        self.focus = max(
            0.0,
            min(100.0, self.focus)
        )

        self.stress = max(
            0.0,
            min(100.0, self.stress)
        )

        self.grade = max(
            0.0,
            min(100.0, self.grade)
        )

    # ====================================================
    # APPLY EVENT / GOAL EFFECTS
    # ====================================================

    def apply_effects(self, effects):

        self.energy += effects.get(
            "energy",
            0
        )

        self.focus += effects.get(
            "focus",
            0
        )

        self.stress += effects.get(
            "stress",
            0
        )

        self.grade += effects.get(
            "grade",
            0
        )

        self.clamp_stats()

    # ====================================================
    # NATURAL STAT CHANGES
    # ====================================================

    def update_stats(self, dt, moving):

        # These values are intentionally noticeable
        # during a 10-minute presentation.

        self.energy -= 0.045 * dt
        self.focus -= 0.060 * dt
        self.stress += 0.035 * dt

        # Walking consumes extra energy and focus.
        if moving:

            self.energy -= 0.025 * dt
            self.focus -= 0.025 * dt

        self.clamp_stats()

    # ====================================================
    # MOVEMENT
    # ====================================================

    def handle_movement(
        self,
        dt,
        obstacles
    ):

        keys = pygame.key.get_pressed()

        dx = 0
        dy = 0

        if (
            keys[pygame.K_w]
            or keys[pygame.K_UP]
        ):

            dy -= 1
            self.direction = "up"

        if (
            keys[pygame.K_s]
            or keys[pygame.K_DOWN]
        ):

            dy += 1
            self.direction = "down"

        if (
            keys[pygame.K_a]
            or keys[pygame.K_LEFT]
        ):

            dx -= 1
            self.direction = "left"

        if (
            keys[pygame.K_d]
            or keys[pygame.K_RIGHT]
        ):

            dx += 1
            self.direction = "right"

        moving = (
            dx != 0
            or dy != 0
        )

        # Normalize diagonal movement.
        if dx != 0 and dy != 0:

            dx *= 0.7071
            dy *= 0.7071

        dx *= self.speed * dt
        dy *= self.speed * dt

        self._move_x(
            dx,
            obstacles
        )

        self._move_y(
            dy,
            obstacles
        )

        if moving:

            self.animation_timer += dt

            if self.animation_timer >= 0.12:

                self.animation_timer = 0.0

                self.animation_frame = (
                    self.animation_frame + 1
                ) % 4

        else:

            self.animation_frame = 0

        # Update survival stats.
        self.update_stats(
            dt,
            moving
        )

        return moving

    # ====================================================
    # X MOVEMENT + COLLISION
    # ====================================================

    def _move_x(
        self,
        dx,
        obstacles
    ):

        self.rect.x += int(dx)

        for obstacle in obstacles:

            if self.rect.colliderect(
                obstacle
            ):

                if dx > 0:

                    self.rect.right = (
                        obstacle.left
                    )

                elif dx < 0:

                    self.rect.left = (
                        obstacle.right
                    )

    # ====================================================
    # Y MOVEMENT + COLLISION
    # ====================================================

    def _move_y(
        self,
        dy,
        obstacles
    ):

        self.rect.y += int(dy)

        for obstacle in obstacles:

            if self.rect.colliderect(
                obstacle
            ):

                if dy > 0:

                    self.rect.bottom = (
                        obstacle.top
                    )

                elif dy < 0:

                    self.rect.top = (
                        obstacle.bottom
                    )

    # ====================================================
    # DRAW PLAYER
    # ====================================================

    def draw(
        self,
        screen,
        camera
    ):

        rect = camera.apply(
            self.rect
        )

        # Shadow
        pygame.draw.ellipse(
            screen,
            (35, 35, 40),
            (
                rect.x + 5,
                rect.y + 40,
                30,
                7
            )
        )

        # Backpack
        pygame.draw.rect(
            screen,
            (125, 80, 45),
            (
                rect.x + 3,
                rect.y + 19,
                9,
                19
            ),
            border_radius=3
        )

        # Body
        pygame.draw.rect(
            screen,
            (55, 110, 190),
            (
                rect.x + 11,
                rect.y + 20,
                18,
                18
            ),
            border_radius=5
        )

        # Hair
        pygame.draw.circle(
            screen,
            (65, 42, 32),
            (
                rect.x + 20,
                rect.y + 8
            ),
            9
        )

        # Face
        pygame.draw.circle(
            screen,
            (235, 190, 160),
            (
                rect.x + 20,
                rect.y + 13
            ),
            7
        )

        # Legs
        pygame.draw.rect(
            screen,
            (45, 50, 65),
            (
                rect.x + 12,
                rect.y + 35,
                7,
                10
            ),
            border_radius=2
        )

        pygame.draw.rect(
            screen,
            (45, 50, 65),
            (
                rect.x + 21,
                rect.y + 35,
                7,
                10
            ),
            border_radius=2
        )

        # YOU label
        font = pygame.font.Font(
            None,
            18
        )

        text = font.render(
            "YOU",
            True,
            (255, 230, 90)
        )

        screen.blit(
            text,
            (
                rect.centerx
                - text.get_width() // 2,

                rect.y - 18
            )
        )