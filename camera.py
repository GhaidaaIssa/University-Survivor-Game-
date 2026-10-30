import pygame


class Camera:
    def __init__(self, screen_width, screen_height, world_width, world_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.world_width = world_width
        self.world_height = world_height

        self.x = 0
        self.y = 0

    def update(self, target):
        """
        Move the camera so the target stays near the center.
        """

        target_center_x = target.rect.centerx
        target_center_y = target.rect.centery

        # Center camera on player
        self.x = target_center_x - self.screen_width // 2
        self.y = target_center_y - self.screen_height // 2

        # Keep camera inside the world
        max_x = self.world_width - self.screen_width
        max_y = self.world_height - self.screen_height

        self.x = max(0, min(self.x, max_x))
        self.y = max(0, min(self.y, max_y))

    def apply(self, rect):
        """
        Convert a world rectangle to screen coordinates.
        """

        return pygame.Rect(
            rect.x - self.x,
            rect.y - self.y,
            rect.width,
            rect.height
        )

    def apply_position(self, x, y):
        """
        Convert a world position to screen coordinates.
        """

        return (
            x - self.x,
            y - self.y
        )
        