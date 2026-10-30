import pygame


WHITE = (245, 245, 245)
GREEN = (85, 190, 105)
YELLOW = (235, 190, 70)
RED = (220, 80, 80)
BLUE = (75, 145, 220)


# =========================================================
# BAR
# =========================================================

def draw_bar(
    screen,
    x,
    y,
    width,
    height,
    value,
    maximum,
    color
):

    pygame.draw.rect(
        screen,
        (55, 58, 65),
        (x, y, width, height),
        border_radius=6
    )

    percentage = max(
        0,
        min(
            1,
            value / maximum
        )
    )

    fill_width = int(
        width * percentage
    )

    if fill_width > 0:

        pygame.draw.rect(
            screen,
            color,
            (
                x,
                y,
                fill_width,
                height
            ),
            border_radius=6
        )


# =========================================================
# MAIN HUD
# =========================================================

def draw_hud(
    screen,
    player,
    game_state,
    ai_decision,
    ai_reason,
    goals_completed
):

    font = pygame.font.SysFont(
        "arial",
        14,
        bold=True
    )

    small = pygame.font.SysFont(
        "arial",
        12
    )

    width = 650
    height = 120

    x = (
        screen.get_width()
        - width
    ) // 2

    y = (
        screen.get_height()
        - height
        - 10
    )

    panel = pygame.Surface(
        (width, height),
        pygame.SRCALPHA
    )

    panel.fill(
        (20, 23, 28, 235)
    )

    screen.blit(
        panel,
        (x, y)
    )

    pygame.draw.rect(
        screen,
        (100, 105, 115),
        (
            x,
            y,
            width,
            height
        ),
        width=2,
        border_radius=12
    )

    # =====================================================
    # ENERGY
    # =====================================================

    screen.blit(
        font.render(
            "Energy",
            True,
            WHITE
        ),
        (x + 15, y + 10)
    )

    draw_bar(
        screen,
        x + 70,
        y + 12,
        90,
        11,
        player.energy,
        100,
        GREEN
    )

    screen.blit(
        small.render(
            str(int(player.energy)),
            True,
            WHITE
        ),
        (x + 165, y + 9)
    )

    # =====================================================
    # STRESS
    # =====================================================

    screen.blit(
        font.render(
            "Stress",
            True,
            WHITE
        ),
        (x + 205, y + 10)
    )

    draw_bar(
        screen,
        x + 255,
        y + 12,
        90,
        11,
        player.stress,
        100,
        RED
    )

    screen.blit(
        small.render(
            str(int(player.stress)),
            True,
            WHITE
        ),
        (x + 350, y + 9)
    )

    # =====================================================
    # FOCUS
    # =====================================================

    screen.blit(
        font.render(
            "Focus",
            True,
            WHITE
        ),
        (x + 390, y + 10)
    )

    draw_bar(
        screen,
        x + 440,
        y + 12,
        90,
        11,
        player.focus,
        100,
        BLUE
    )

    screen.blit(
        small.render(
            str(int(player.focus)),
            True,
            WHITE
        ),
        (x + 535, y + 9)
    )

    # =====================================================
    # GRADE
    # =====================================================

    grade_text = font.render(
        f"Grade: {int(player.grade)}",
        True,
        YELLOW
    )

    screen.blit(
        grade_text,
        (x + 15, y + 42)
    )

    # =====================================================
    # TIME
    # =====================================================

    time_text = font.render(
        "Time: "
        + game_state.get_time(),
        True,
        WHITE
    )

    screen.blit(
        time_text,
        (x + 130, y + 42)
    )

    # =====================================================
    # GOALS COMPLETED
    # =====================================================

    goals_text = font.render(
        f"Goals Completed: {goals_completed}",
        True,
        GREEN
    )

    screen.blit(
        goals_text,
        (x + 330, y + 42)
    )

    # =====================================================
    # AI RECOMMENDATION
    # =====================================================

    screen.blit(
        font.render(
            "AI Recommendation:",
            True,
            WHITE
        ),
        (x + 15, y + 72)
    )

    screen.blit(
        font.render(
            ai_decision,
            True,
            YELLOW
        ),
        (x + 160, y + 72)
    )

    screen.blit(
        small.render(
            ai_reason,
            True,
            (195, 205, 220)
        ),
        (x + 15, y + 96)
    )


# =========================================================
# CURRENT DYNAMIC GOAL
# =========================================================

def draw_goals(
    screen,
    current_goal,
    goals_completed
):

    font = pygame.font.SysFont(
        "arial",
        14,
        bold=True
    )

    small = pygame.font.SysFont(
        "arial",
        13
    )

    x = 15
    y = 15

    width = 290
    height = 105

    panel = pygame.Surface(
        (width, height),
        pygame.SRCALPHA
    )

    panel.fill(
        (20, 23, 28, 220)
    )

    screen.blit(
        panel,
        (x, y)
    )

    pygame.draw.rect(
        screen,
        (95, 100, 110),
        (
            x,
            y,
            width,
            height
        ),
        width=1,
        border_radius=10
    )

    # Title
    screen.blit(
        font.render(
            "CURRENT AI GOAL",
            True,
            YELLOW
        ),
        (x + 12, y + 10)
    )

    # Current task
    screen.blit(
        small.render(
            current_goal["name"],
            True,
            WHITE
        ),
        (x + 12, y + 40)
    )

    # Completed counter
    screen.blit(
        small.render(
            f"Completed: {goals_completed}",
            True,
            GREEN
        ),
        (x + 12, y + 70)
    )


# =========================================================
# DAY OVER
# =========================================================

def draw_day_over(
    screen,
    player,
    goals_completed
):

    overlay = pygame.Surface(
        screen.get_size(),
        pygame.SRCALPHA
    )

    overlay.fill(
        (5, 7, 10, 225)
    )

    screen.blit(
        overlay,
        (0, 0)
    )

    # =====================================================
    # RESULT
    # =====================================================

    if player.energy <= 0:

        result = (
            "DAY FAILED - EXHAUSTED"
        )

    elif player.stress >= 100:

        result = (
            "DAY FAILED - TOO MUCH PRESSURE"
        )

    elif player.grade < 50:

        result = (
            "DAY COMPLETED - "
            "ACADEMIC PERFORMANCE LOW"
        )

    else:

        result = (
            "UNIVERSITY DAY COMPLETED"
        )

    title_font = pygame.font.SysFont(
        "arial",
        34,
        bold=True
    )

    font = pygame.font.SysFont(
        "arial",
        20
    )

    title = title_font.render(
        result,
        True,
        YELLOW
    )

    screen.blit(
        title,
        (
            screen.get_width() // 2
            - title.get_width() // 2,

            200
        )
    )

    # =====================================================
    # FINAL STATS
    # =====================================================

    lines = [

        f"Grade: {int(player.grade)}/100",

        f"Energy: {int(player.energy)}/100",

        f"Stress: {int(player.stress)}/100",

        f"Focus: {int(player.focus)}/100",

        f"Goals Completed: {goals_completed}"
    ]

    for index, line in enumerate(
        lines
    ):

        text = font.render(
            line,
            True,
            WHITE
        )

        screen.blit(
            text,
            (
                screen.get_width() // 2
                - text.get_width() // 2,

                275 + index * 34
            )
        )