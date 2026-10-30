import pygame
# =========================================================
# WORLD SETTINGS
# =========================================================
MAP_WIDTH = 1800
MAP_HEIGHT = 1200
# =========================================================
# COLORS
# =========================================================
GRASS = (112, 170, 105)
GRASS_LIGHT = (125, 183, 115)
ROAD = (92, 96, 105)
ROAD_LIGHT = (108, 112, 120)
PLAZA = (205, 198, 178)
PLAZA_LIGHT = (220, 214, 195)
WATER = (75, 155, 190)
WATER_LIGHT = (105, 185, 215)
BUILDING_SHADOW = (65, 70, 75)
WHITE = (245, 245, 245)
BLACK = (35, 38, 42)
WINDOW = (150, 205, 225)
WINDOW_DARK = (90, 150, 175)
DOOR = (105, 75, 55)
TREE_TRUNK = (105, 75, 45)
TREE_GREEN = (55, 125, 65)
TREE_LIGHT = (80, 150, 80)
BENCH = (110, 75, 48)
# =========================================================
# BUILDINGS
# =========================================================
BUILDINGS = [
    # Top area
    ("Library", 100, 130, 260, 150),
    ("Computer Lab", 770, 110, 270, 155),
    ("Science Lab", 1350, 140, 270, 150),
    # Middle area
    ("Lecture Hall", 100, 650, 280, 165),
    ("AI Lab", 760, 650, 280, 165),
    ("Student Center", 1360, 650, 280, 165),
    # Bottom area
    ("Cafeteria", 470, 950, 270, 145),
    ("Administration", 1050, 950, 280, 145),
]
# =========================================================
# DRAW BUILDING
# =========================================================
def draw_building(screen, camera, name, x, y, width, height):
    world_rect = pygame.Rect(x, y, width, height)
    rect = camera.apply(world_rect)
    # Shadow
    shadow_world = pygame.Rect(
        x + 8,
        y + 10,
        width,
        height
    )
    shadow = camera.apply(shadow_world)
    pygame.draw.rect(
        screen,
        BUILDING_SHADOW,
        shadow,
        border_radius=14
    )
    # Main building
    pygame.draw.rect(
        screen,
        WHITE,
        rect,
        border_radius=14
    )
    # Header
    top_height = 40
    top_world = pygame.Rect(
        x,
        y,
        width,
        top_height
    )
    top_rect = camera.apply(top_world)
    pygame.draw.rect(
        screen,
        ROAD,
        top_rect,
        border_top_left_radius=14,
        border_top_right_radius=14
    )
    # Outline
    pygame.draw.rect(
        screen,
        BLACK,
        rect,
        width=2,
        border_radius=14
    )
    # -----------------------------------------------------
    # Windows
    # -----------------------------------------------------
    window_y = y + 58
    window_width = 36
    window_height = 28
    spacing = 18
    window_count = 5
    total_width = (
        window_count * window_width
        + (window_count - 1) * spacing
    )
    start_x = x + (width - total_width) // 2
    for i in range(window_count):
        wx = start_x + i * (window_width + spacing)
        world_window = pygame.Rect(
            wx,
            window_y,
            window_width,
            window_height
        )
        window_rect = camera.apply(world_window)
        pygame.draw.rect(
            screen,
            WINDOW,
            window_rect,
            border_radius=5
        )
        pygame.draw.rect(
            screen,
            WINDOW_DARK,
            window_rect,
            width=2,
            border_radius=5
        )
        # Vertical divider
        pygame.draw.line(
            screen,
            WINDOW_DARK,
            (
                window_rect.centerx,
                window_rect.y + 3
            ),
            (
                window_rect.centerx,
                window_rect.bottom - 3
            ),
            2
        )
    # -----------------------------------------------------
    # Door
    # -----------------------------------------------------
    door_width = 38
    door_height = 44
    door_x = x + width // 2 - door_width // 2
    door_y = y + height - door_height
    world_door = pygame.Rect(
        door_x,
        door_y,
        door_width,
        door_height
    )
    door_rect = camera.apply(world_door)
    pygame.draw.rect(
        screen,
        DOOR,
        door_rect,
        border_radius=5
    )
    pygame.draw.rect(
        screen,
        BLACK,
        door_rect,
        width=2,
        border_radius=5
    )
    pygame.draw.circle(
        screen,
        (220, 190, 90),
        (
            door_rect.x + 29,
            door_rect.y + 23
        ),
        3
    )
    # -----------------------------------------------------
    # Building name
    # -----------------------------------------------------
    font = pygame.font.SysFont(
        "arial",
        18,
        bold=True
    )
    text = font.render(
        name,
        True,
        WHITE
    )
    text_rect = text.get_rect(
        center=top_rect.center
    )
    screen.blit(
        text,
        text_rect
    )
# =========================================================
# TREE
# =========================================================
def draw_tree(screen, camera, x, y):
    sx, sy = camera.apply_position(x, y)
    pygame.draw.ellipse(
        screen,
        (75, 105, 70),
        (sx - 22, sy + 18, 44, 14)
    )
    pygame.draw.rect(
        screen,
        TREE_TRUNK,
        (sx - 5, sy, 10, 28),
        border_radius=3
    )
    pygame.draw.circle(
        screen,
        TREE_GREEN,
        (sx, sy - 5),
        21
    )
    pygame.draw.circle(
        screen,
        TREE_LIGHT,
        (sx - 11, sy - 2),
        13
    )
    pygame.draw.circle(
        screen,
        TREE_LIGHT,
        (sx + 11, sy - 1),
        13
    )
# =========================================================
# BENCH
# =========================================================
def draw_bench(screen, camera, x, y):
    rect = camera.apply(
        pygame.Rect(x, y, 52, 30)
    )
    pygame.draw.rect(
        screen,
        BENCH,
        (
            rect.x,
            rect.y,
            52,
            8
        ),
        border_radius=3
    )
    pygame.draw.rect(
        screen,
        BENCH,
        (
            rect.x + 4,
            rect.y + 13,
            44,
            7
        ),
        border_radius=3
    )
    pygame.draw.line(
        screen,
        BLACK,
        (
            rect.x + 8,
            rect.y + 20
        ),
        (
            rect.x + 8,
            rect.y + 29
        ),
        3
    )
    pygame.draw.line(
        screen,
        BLACK,
        (
            rect.x + 44,
            rect.y + 20
        ),
        (
            rect.x + 44,
            rect.y + 29
        ),
        3
    )
# =========================================================
# WATER
# =========================================================
def draw_water(screen, camera):
    world_rect = pygame.Rect(
        520,
        350,
        760,
        150
    )
    rect = camera.apply(world_rect)
    pygame.draw.rect(
        screen,
        WATER,
        rect,
        border_radius=35
    )
    pygame.draw.rect(
        screen,
        WATER_LIGHT,
        rect,
        width=4,
        border_radius=35
    )
    for y in range(
        world_rect.y + 30,
        world_rect.bottom - 20,
        25
    ):
        start_x = world_rect.x + 50
        end_x = world_rect.right - 50
        start = camera.apply_position(
            start_x,
            y
        )
        end = camera.apply_position(
            end_x,
            y
        )
        pygame.draw.line(
            screen,
            WATER_LIGHT,
            start,
            end,
            2
        )
# =========================================================
# PLAZA
# =========================================================
def draw_plaza(screen, camera):
    world_rect = pygame.Rect(
        590,
        525,
        620,
        70
    )
    rect = camera.apply(world_rect)
    pygame.draw.rect(
        screen,
        PLAZA,
        rect,
        border_radius=20
    )
    pygame.draw.rect(
        screen,
        PLAZA_LIGHT,
        rect,
        width=3,
        border_radius=20
    )
# =========================================================
# MAP
# =========================================================
def draw_map(screen, camera):
    # Background
    screen.fill(GRASS)
    # -----------------------------------------------------
    # Main roads
    # -----------------------------------------------------
    vertical_road_world = pygame.Rect(
        410,
        60,
        90,
        1140
    )
    horizontal_road_world = pygame.Rect(
        0,
        560,
        MAP_WIDTH,
        90
    )
    vertical_road = camera.apply(
        vertical_road_world
    )
    horizontal_road = camera.apply(
        horizontal_road_world
    )
    pygame.draw.rect(
        screen,
        ROAD,
        vertical_road
    )
    pygame.draw.rect(
        screen,
        ROAD,
        horizontal_road
    )
    # -----------------------------------------------------
    # Road markings
    # -----------------------------------------------------
    for y in range(80, MAP_HEIGHT, 45):
        start = camera.apply_position(
            455,
            y
        )
        end = camera.apply_position(
            455,
            y + 22
        )
        pygame.draw.line(
            screen,
            ROAD_LIGHT,
            start,
            end,
            3
        )
    for x in range(20, MAP_WIDTH, 45):
        start = camera.apply_position(
            x,
            605
        )
        end = camera.apply_position(
            x + 22,
            605
        )
        pygame.draw.line(
            screen,
            ROAD_LIGHT,
            start,
            end,
            3
        )
    # -----------------------------------------------------
    # Water
    # -----------------------------------------------------
    draw_water(
        screen,
        camera
    )
    # -----------------------------------------------------
    # Plaza
    # -----------------------------------------------------
    draw_plaza(
        screen,
        camera
    )
    # -----------------------------------------------------
    # Buildings
    # -----------------------------------------------------
    for building in BUILDINGS:
        name, x, y, width, height = building
        draw_building(
            screen,
            camera,
            name,
            x,
            y,
            width,
            height
        )
    # -----------------------------------------------------
    # Trees
    # -----------------------------------------------------
    trees = [
        # Left
        (45, 120),
        (45, 350),
        (45, 900),
        (360, 1050),
        # Upper middle
        (600, 80),
        (1100, 75),
        (1250, 300),
        # Right
        (1740, 110),
        (1740, 360),
        (1740, 900),
        # Bottom
        (800, 1130),
        (1450, 1130),
        # Around plaza
        (570, 520),
        (1230, 520),
    ]
    for x, y in trees:
        draw_tree(
            screen,
            camera,
            x,
            y
        )
    # -----------------------------------------------------
    # Benches
    # -----------------------------------------------------
    benches = [
        (650, 530),
        (1120, 530),
        (650, 610),
        (1120, 610),
    ]
    for x, y in benches:
        draw_bench(
            screen,
            camera,
            x,
            y
        )
    # -----------------------------------------------------
    # University title
    # -----------------------------------------------------
    title_font = pygame.font.SysFont(
        "arial",
        30,
        bold=True
    )
    subtitle_font = pygame.font.SysFont(
        "arial",
        15
    )
    title = title_font.render(
        "UNIVERSITY",
        True,
        WHITE
    )
    subtitle = subtitle_font.render(
        "SURVIVAL CAMPUS",
        True,
        WHITE
    )
    title_position = camera.apply_position(
        MAP_WIDTH // 2,
        30
    )
    subtitle_position = camera.apply_position(
        MAP_WIDTH // 2,
        55
    )
    title_rect = title.get_rect(
        center=title_position
    )
    subtitle_rect = subtitle.get_rect(
        center=subtitle_position
    )
    screen.blit(
        title,
        title_rect
    )
    screen.blit(
        subtitle,
        subtitle_rect
    )
# =========================================================
# OBSTACLES
# =========================================================
def get_obstacles():
    obstacles = []
    # Buildings
    for name, x, y, width, height in BUILDINGS:
        obstacles.append(
            pygame.Rect(
                x,
                y,
                width,
                height
            )
        )
    # Water
    obstacles.append(
        pygame.Rect(
            520,
            350,
            760,
            150
        )
    )
    # Benches
    obstacles.extend([
        pygame.Rect(650, 530, 52, 30),
        pygame.Rect(1120, 530, 52, 30),
        pygame.Rect(650, 610, 52, 30),
        pygame.Rect(1120, 610, 52, 30),
    ])
    # Trees
    trees = [
        (45, 120),
        (45, 350),
        (45, 900),
        (360, 1050),
        (600, 80),
        (1100, 75),
        (1250, 300),
        (1740, 110),
        (1740, 360),
        (1740, 900),
        (800, 1130),
        (1450, 1130),
        (570, 520),
        (1230, 520),
    ]
    for x, y in trees:
        obstacles.append(
            pygame.Rect(
                x - 22,
                y - 25,
                44,
                55
            )
        )
    return obstacles