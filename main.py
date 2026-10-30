import sys
import pygame

from Config import (
    WIDTH,
    HEIGHT,
    FPS,
    TITLE,
    BACKGROUND_COLOR,
    START_HOUR,
    START_MINUTE,
    GAME_MINUTES_PER_SECOND
)

from Map import (
    draw_map,
    get_obstacles,
    MAP_WIDTH,
    MAP_HEIGHT
)

from player import Player

from game_state import GameState

from hud import (
    draw_hud,
    draw_goals,
    draw_day_over
)

from events import EventManager

from Ai_agent import AIAgent

from camera import Camera

from npc import create_students


# =========================================================
# INITIALIZE PYGAME
# =========================================================

pygame.init()

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT)
)

pygame.display.set_caption(
    TITLE
)

clock = pygame.time.Clock()


# =========================================================
# CREATE GAME OBJECTS
# =========================================================

player = Player(
    220,
    335
)

game_state = GameState(
    START_HOUR,
    START_MINUTE,
    GAME_MINUTES_PER_SECOND
)

event_manager = EventManager()

ai_agent = AIAgent()

obstacles = get_obstacles()

camera = Camera(
    WIDTH,
    HEIGHT,
    MAP_WIDTH,
    MAP_HEIGHT
)

students = create_students(
    ai_agent
)


# =========================================================
# DYNAMIC AI GOALS
# =========================================================

goal_locations = {

    "Visit Library":
    (230, 308),

    "Visit AI Lab":
    (900, 843),

    "Visit Lecture Hall":
    (240, 843),

    "Visit Cafeteria":
    (605, 1123),

    "Visit Student Center":
    (1500, 843),

    "Visit Computer Lab":
    (905, 293)
}


# First goal
current_goal = {

    "name":
    "Visit Lecture Hall",

    "position":
    goal_locations[
        "Visit Lecture Hall"
    ]
}


goals_completed = 0

last_goal_name = None


# =========================================================
# CHOOSE A NEW GOAL USING PLAYER STATE
# =========================================================

def choose_new_goal():

    global current_goal
    global last_goal_name

    # -----------------------------------------------------
    # Low energy -> rest
    # -----------------------------------------------------

    if player.energy <= 40:

        goal_name = (
            "Visit Cafeteria"
        )

    # -----------------------------------------------------
    # High stress -> socialize
    # -----------------------------------------------------

    elif player.stress >= 60:

        goal_name = (
            "Visit Student Center"
        )

    # -----------------------------------------------------
    # Low focus -> study
    # -----------------------------------------------------

    elif player.focus <= 55:

        goal_name = (
            "Visit Library"
        )

    # -----------------------------------------------------
    # Low grade -> academic improvement
    # -----------------------------------------------------

    elif player.grade <= 65:

        goal_name = (
            "Visit AI Lab"
        )

    # -----------------------------------------------------
    # Normal state -> academic activity
    # -----------------------------------------------------

    else:

        academic_goals = [

            "Visit Lecture Hall",

            "Visit Computer Lab",

            "Visit AI Lab",

            "Visit Library"
        ]

        available = [

            name
            for name in academic_goals

            if name != last_goal_name
        ]

        index = (
            goals_completed
            % len(available)
        )

        goal_name = (
            available[index]
        )

    # -----------------------------------------------------
    # Avoid immediate duplicate goal
    # -----------------------------------------------------

    if goal_name == last_goal_name:

        alternatives = [

            "Visit Library",

            "Visit AI Lab",

            "Visit Lecture Hall",

            "Visit Cafeteria",

            "Visit Student Center",

            "Visit Computer Lab"
        ]

        for alternative in alternatives:

            if (
                alternative
                != last_goal_name
            ):

                goal_name = (
                    alternative
                )

                break

    # -----------------------------------------------------
    # Save new goal
    # -----------------------------------------------------

    current_goal = {

        "name":
        goal_name,

        "position":
        goal_locations[
            goal_name
        ]
    }

    last_goal_name = (
        goal_name
    )

    # Show message
    event_manager.show(
        "AI NEW GOAL: "
        + goal_name,
        4.0
    )


# =========================================================
# CHECK IF PLAYER COMPLETED CURRENT GOAL
# =========================================================

def update_goal():

    global goals_completed

    player_x = (
        player.rect.centerx
    )

    player_y = (
        player.rect.centery
    )

    target_x, target_y = (
        current_goal[
            "position"
        ]
    )

    dx = (
        target_x - player_x
    )

    dy = (
        target_y - player_y
    )

    distance = (
        dx * dx
        + dy * dy
    ) ** 0.5

    # =====================================================
    # GOAL COMPLETED
    # =====================================================

    if distance <= 80:

        completed_name = (
            current_goal[
                "name"
            ]
        )

        goals_completed += 1

        # -------------------------------------------------
        # CAFETERIA
        # -------------------------------------------------

        if (
            completed_name
            == "Visit Cafeteria"
        ):

            player.apply_effects({

                "energy": 14,

                "stress": -5,

                "focus": 3
            })

        # -------------------------------------------------
        # STUDENT CENTER
        # -------------------------------------------------

        elif (
            completed_name
            == "Visit Student Center"
        ):

            player.apply_effects({

                "energy": 4,

                "stress": -10,

                "focus": 2
            })

        # -------------------------------------------------
        # LIBRARY
        # -------------------------------------------------

        elif (
            completed_name
            == "Visit Library"
        ):

            player.apply_effects({

                "energy": -4,

                "stress": 2,

                "focus": 10,

                "grade": 5
            })

        # -------------------------------------------------
        # AI LAB
        # -------------------------------------------------

        elif (
            completed_name
            == "Visit AI Lab"
        ):

            player.apply_effects({

                "energy": -5,

                "stress": 3,

                "focus": 8,

                "grade": 6
            })

        # -------------------------------------------------
        # COMPUTER LAB
        # -------------------------------------------------

        elif (
            completed_name
            == "Visit Computer Lab"
        ):

            player.apply_effects({

                "energy": -4,

                "stress": 2,

                "focus": 7,

                "grade": 5
            })

        # -------------------------------------------------
        # LECTURE HALL
        # -------------------------------------------------

        elif (
            completed_name
            == "Visit Lecture Hall"
        ):

            player.apply_effects({

                "energy": -5,

                "stress": 2,

                "focus": 5,

                "grade": 6
            })

        # -------------------------------------------------
        # MESSAGE
        # -------------------------------------------------

        event_manager.show(
            "GOAL COMPLETED: "
            + completed_name,
            3.0
        )

        
        # AI immediately creates another goal
     

        choose_new_goal()



# FIRST AI RECOMMENDATION


ai_decision, ai_reason = (
    ai_agent.explain_decision(
        player
    )
)



# GAME LOOP


running = True

day_over = False


while running:

    dt = (
        clock.tick(FPS)
        / 1000.0
    )

    
    # PYGAME EVENTS
    

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        if event.type == pygame.KEYDOWN:

            # ESC = Exit
            if event.key == pygame.K_ESCAPE:

                running = False

           
            # EVENT DECISION 1 / 2
          

            if not day_over:

                event_manager.handle_key(
                    event.key,
                    player
                )

    
    # GAME UPDATE
   

    if not day_over:

        
        # PLAYER MOVEMENT + STATS
       

        player.handle_movement(
            dt,
            obstacles
        )

        
        # AI OBSERVES PLAYER
        

        new_decision, new_reason = (
            ai_agent.explain_decision(
                player
            )
        )

        
        # AI RECOMMENDATION CHANGED
        

        if (
            new_decision
            != ai_decision
        ):

            ai_decision = (
                new_decision
            )

            ai_reason = (
                new_reason
            )

            event_manager.show(
                "AI changed recommendation: "
                + ai_decision,
                4.0
            )

        else:

            ai_reason = (
                new_reason
            )

        # -------------------------------------------------
        # AUTONOMOUS NPC STUDENTS
        # -------------------------------------------------

        for student in students:

            student.update(
                dt,
                obstacles
            )

        # -------------------------------------------------
        # DYNAMIC PLAYER GOAL
        # -------------------------------------------------

        update_goal()

        # -------------------------------------------------
        # UNIVERSITY TIME
        # -------------------------------------------------

        game_state.update(
            dt
        )

        # -------------------------------------------------
        # PRESSURE / JUDGMENT EVENTS
        # -------------------------------------------------

        event_manager.update(
            dt,
            game_state
        )

        # -------------------------------------------------
        # FAILURE: ENERGY
        # -------------------------------------------------

        if player.energy <= 0:

            day_over = True

        # -------------------------------------------------
        # FAILURE: STRESS
        # -------------------------------------------------

        elif player.stress >= 100:

            day_over = True

        # -------------------------------------------------
        # END OF UNIVERSITY DAY
        # -------------------------------------------------

        elif game_state.day_over:

            day_over = True

    # =====================================================
    # CAMERA
    # =====================================================

    camera.update(
        player
    )

    # =====================================================
    # DRAW
    # =====================================================

    screen.fill(
        BACKGROUND_COLOR
    )

    # -----------------------------------------------------
    # MAP
    # -----------------------------------------------------

    draw_map(
        screen,
        camera
    )

    # -----------------------------------------------------
    # NPC STUDENTS
    # -----------------------------------------------------

    for student in students:

        student.draw(
            screen,
            camera
        )

    # -----------------------------------------------------
    # PLAYER
    # -----------------------------------------------------

    player.draw(
        screen,
        camera
    )

    # -----------------------------------------------------
    # CURRENT DYNAMIC GOAL
    # -----------------------------------------------------

    draw_goals(
        screen,
        current_goal,
        goals_completed
    )

    # -----------------------------------------------------
    # HUD
    # -----------------------------------------------------

    draw_hud(
        screen,
        player,
        game_state,
        ai_decision,
        ai_reason,
        goals_completed
    )

    # -----------------------------------------------------
    # NORMAL MESSAGE
    # -----------------------------------------------------

    event_manager.draw_message(
        screen
    )

    # -----------------------------------------------------
    # PRESSURE / JUDGMENT DECISION
    # -----------------------------------------------------

    event_manager.draw_event(
        screen
    )

    # -----------------------------------------------------
    # FINAL RESULT
    # -----------------------------------------------------

    if day_over:

        draw_day_over(
            screen,
            player,
            goals_completed
        )

    # -----------------------------------------------------
    # DISPLAY
    # -----------------------------------------------------

    pygame.display.flip()


# =========================================================
# EXIT
# =========================================================

pygame.quit()

sys.exit()