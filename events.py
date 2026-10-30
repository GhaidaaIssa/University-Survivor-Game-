import pygame


class EventManager:

    def __init__(self):

        self.message = ""
        self.message_timer = 0.0

        self.active_event = None

        self.triggered_events = set()

        # =============================================
        # Every university hour =
        # approximately one real minute
        # =============================================

        self.events = [

            {
                "id": 1,
                "hour": 9,
                "title": "Morning Pressure",

                "text":
                "Your first class is starting. "
                "You also feel tired.",

                "option1":
                "Attend the class",

                "effect1": {
                    "grade": 6,
                    "energy": -8,
                    "stress": 5,
                    "focus": 3
                },

                "option2":
                "Take a short rest",

                "effect2": {
                    "grade": -2,
                    "energy": 10,
                    "stress": -6,
                    "focus": 2
                }
            },

            {
                "id": 2,
                "hour": 10,
                "title": "Academic Pressure",

                "text":
                "You have an assignment "
                "that needs more work.",

                "option1":
                "Study seriously",

                "effect1": {
                    "grade": 7,
                    "energy": -9,
                    "stress": 5,
                    "focus": 7
                },

                "option2":
                "Leave it for later",

                "effect2": {
                    "grade": -5,
                    "energy": 3,
                    "stress": 2,
                    "focus": -4
                }
            },

            {
                "id": 3,
                "hour": 11,
                "title": "Student Judgment",

                "text":
                "A classmate says: "
                "'You are falling behind.'",

                "option1":
                "Use it as motivation",

                "effect1": {
                    "grade": 5,
                    "energy": -4,
                    "stress": 5,
                    "focus": 8
                },

                "option2":
                "Ignore the comment",

                "effect2": {
                    "grade": 0,
                    "energy": 2,
                    "stress": -5,
                    "focus": -2
                }
            },

            {
                "id": 4,
                "hour": 12,
                "title": "Lunch Decision",

                "text":
                "You are hungry, "
                "but you still have work.",

                "option1":
                "Eat and recover",

                "effect1": {
                    "energy": 15,
                    "stress": -6,
                    "focus": 4,
                    "grade": 0
                },

                "option2":
                "Continue studying",

                "effect2": {
                    "energy": -10,
                    "stress": 6,
                    "focus": 7,
                    "grade": 5
                }
            },

            {
                "id": 5,
                "hour": 13,
                "title": "Group Project",

                "text":
                "Your group asks you "
                "to help with the project.",

                "option1":
                "Help the group",

                "effect1": {
                    "grade": 7,
                    "energy": -7,
                    "stress": 3,
                    "focus": 4
                },

                "option2":
                "Work alone",

                "effect2": {
                    "grade": -2,
                    "energy": 3,
                    "stress": 2,
                    "focus": 1
                }
            },

            {
                "id": 6,
                "hour": 14,
                "title": "Mental Pressure",

                "text":
                "The university day "
                "is becoming stressful.",

                "option1":
                "Take a healthy break",

                "effect1": {
                    "energy": 9,
                    "stress": -12,
                    "focus": 5,
                    "grade": 0
                },

                "option2":
                "Keep pushing",

                "effect2": {
                    "energy": -8,
                    "stress": 9,
                    "focus": 4,
                    "grade": 4
                }
            },

            {
                "id": 7,
                "hour": 15,
                "title": "Unexpected Quiz",

                "text":
                "The professor announces "
                "a surprise quiz.",

                "option1":
                "Focus and answer",

                "effect1": {
                    "energy": -6,
                    "stress": 7,
                    "focus": 5,
                    "grade": 8
                },

                "option2":
                "Give up early",

                "effect2": {
                    "energy": 1,
                    "stress": -2,
                    "focus": -5,
                    "grade": -8
                }
            },

            {
                "id": 8,
                "hour": 16,
                "title": "Social Pressure",

                "text":
                "Friends invite you out "
                "before your work is done.",

                "option1":
                "Finish your work",

                "effect1": {
                    "energy": -5,
                    "stress": 3,
                    "focus": 6,
                    "grade": 6
                },

                "option2":
                "Go with friends",

                "effect2": {
                    "energy": 2,
                    "stress": -10,
                    "focus": -3,
                    "grade": -3
                }
            },

            {
                "id": 9,
                "hour": 17,
                "title": "Final Hour",

                "text":
                "One hour remains. "
                "How will you finish the day?",

                "option1":
                "Final study session",

                "effect1": {
                    "energy": -10,
                    "stress": 6,
                    "focus": 6,
                    "grade": 8
                },

                "option2":
                "Recover before leaving",

                "effect2": {
                    "energy": 12,
                    "stress": -10,
                    "focus": 3,
                    "grade": 0
                }
            }
        ]

    # =====================================================
    # MESSAGE
    # =====================================================

    def show(
        self,
        message,
        duration=3.0
    ):

        self.message = message
        self.message_timer = duration

    # =====================================================
    # UPDATE
    # =====================================================

    def update(
        self,
        dt,
        game_state
    ):

        if self.message_timer > 0:

            self.message_timer -= dt

            if self.message_timer <= 0:

                self.message = ""

        if self.active_event is not None:
            return

        for event in self.events:

            if event["id"] in self.triggered_events:
                continue

            if game_state.hour >= event["hour"]:

                self.active_event = event

                self.triggered_events.add(
                    event["id"]
                )

                break

    # =====================================================
    # PLAYER CHOICE
    # =====================================================

    def handle_key(
        self,
        key,
        player
    ):

        if self.active_event is None:
            return False

        if key == pygame.K_1:

            player.apply_effects(
                self.active_event[
                    "effect1"
                ]
            )

            self.show(
                "Decision: "
                + self.active_event[
                    "option1"
                ]
            )

            self.active_event = None

            return True

        if key == pygame.K_2:

            player.apply_effects(
                self.active_event[
                    "effect2"
                ]
            )

            self.show(
                "Decision: "
                + self.active_event[
                    "option2"
                ]
            )

            self.active_event = None

            return True

        return False

    # =====================================================
    # DRAW EVENT
    # =====================================================

    def draw_event(
        self,
        screen
    ):

        if self.active_event is None:
            return

        width = 760
        height = 230

        x = (
            screen.get_width()
            - width
        ) // 2

        y = 170

        panel = pygame.Surface(
            (width, height),
            pygame.SRCALPHA
        )

        panel.fill(
            (18, 21, 27, 245)
        )

        screen.blit(
            panel,
            (x, y)
        )

        pygame.draw.rect(
            screen,
            (150, 155, 170),
            (x, y, width, height),
            width=2,
            border_radius=14
        )

        title_font = pygame.font.SysFont(
            "arial",
            25,
            bold=True
        )

        font = pygame.font.SysFont(
            "arial",
            18
        )

        option_font = pygame.font.SysFont(
            "arial",
            18,
            bold=True
        )

        title = title_font.render(
            self.active_event["title"],
            True,
            (245, 205, 80)
        )

        screen.blit(
            title,
            (x + 25, y + 20)
        )

        text = font.render(
            self.active_event["text"],
            True,
            (245, 245, 245)
        )

        screen.blit(
            text,
            (x + 25, y + 65)
        )

        option1 = option_font.render(
            "[1] "
            + self.active_event[
                "option1"
            ],
            True,
            (120, 220, 140)
        )

        option2 = option_font.render(
            "[2] "
            + self.active_event[
                "option2"
            ],
            True,
            (120, 175, 240)
        )

        screen.blit(
            option1,
            (x + 30, y + 115)
        )

        screen.blit(
            option2,
            (x + 30, y + 155)
        )

    # =====================================================
    # DRAW MESSAGE
    # =====================================================

    def draw_message(
        self,
        screen
    ):

        if not self.message:
            return

        font = pygame.font.SysFont(
            "arial",
            18,
            bold=True
        )

        text = font.render(
            self.message,
            True,
            (245, 245, 245)
        )

        width = (
            text.get_width()
            + 40
        )

        height = 48

        x = (
            screen.get_width()
            - width
        ) // 2

        y = 100

        pygame.draw.rect(
            screen,
            (25, 28, 34),
            (x, y, width, height),
            border_radius=10
        )

        screen.blit(
            text,
            (
                x + 20,
                y + 13
            )
        )