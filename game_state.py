class GameState:

    def __init__(
        self,
        start_hour=8,
        start_minute=0,
        minutes_per_second=1
    ):

        self.hour = start_hour
        self.minute = start_minute

        self.minutes_per_second = (
            minutes_per_second
        )

        self._time_accumulator = 0.0

        self.day_over = False

    def update(self, dt):

        if self.day_over:
            return

        self._time_accumulator += (
            dt
            * self.minutes_per_second
        )

        whole_minutes = int(
            self._time_accumulator
        )

        if whole_minutes <= 0:
            return

        self._time_accumulator -= (
            whole_minutes
        )

        self.minute += whole_minutes

        while self.minute >= 60:

            self.minute -= 60
            self.hour += 1

        if self.hour >= 18:

            self.hour = 18
            self.minute = 0

            self.day_over = True

    def get_time(self):

        suffix = (
            "AM"
            if self.hour < 12
            else "PM"
        )

        display_hour = (
            self.hour % 12
        )

        if display_hour == 0:
            display_hour = 12

        return (
            f"{display_hour:02d}:"
            f"{self.minute:02d} "
            f"{suffix}"
        )