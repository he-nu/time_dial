#! /usr/bin/env python3

"""
Prints an ascii art sun/moon dial based on current hour.
"""

from datetime import datetime
import subprocess
import time


from ascii_modules import sun_and_moon
from ascii_modules.art import Art, TimeLine


class TimeDial():

    time_face = TimeLine()
    time_line_art = time_face.timeline
    numline = time_face.numline

    moon_string = sun_and_moon.MOON2
    sun_string = sun_and_moon.SUN
    moon_art = Art(moon_string)
    sun = Art(sun_string)
    timeline = Art(time_line_art)

    face_hours = 12 # Clock face indexes
    x_incr = 5 # shift in white space per hour
    sun_pad = 4 # sun needs a negative pad
    top_pad = 6 # the objects rise and fall for 6 steps: clockface//2

    pad_ = " "
    half_sun_art = sun.lines[: (len(sun.lines) // 2) + 1]
    half_moon_art = moon_art.lines[: (len(moon_art.lines) // 2) + 1]


    def __height_diff(self, art1:list, art2:list) -> int:
        """
        Calculate the absolute difference in length between two lists.

        Args:
            art1 (list): The first list.
            art2 (list): The second list.

        Returns:
            int: The absolute difference in length between the two 
                    lists.
        """
        return abs(len(art1)-len(art2))

    def __sunrise(self) -> str:
        """
        Generate the sunrise string by combining the sun and moon art,
        adjusting for their relative positions.

        This method calculates the height difference between the sun and
        moon art, then constructs a sunrise scene by combining them with
        the appropriate padding and spacing.

        Returns:
            str: The generated sunrise scene as a string.
        """
        # Sunrise, moonset
        __height_diff = self.__height_diff(
            self.half_sun_art, self.half_moon_art)
        top_ = "\n" * 3
        # adjusting for the sun art is bigger
        for top_r in self.half_sun_art[: __height_diff]:
            top_ += top_r[self.sun_pad:] + "\n"
        mixed = ""
        for i, sun_ray in enumerate(self.half_sun_art[__height_diff:]):
            # Add some sun to the row
            line_ = sun_ray[self.sun_pad:]

            # Calculate the distance between the sun and the moon.
            # Add space and moon.
            line_ += f"""{self.pad_ 
                        * (self.x_incr*self.face_hours - len(sun_ray) 
                        + self.sun_pad)} {self.half_moon_art[i]}"""
            mixed += line_ + "\n"
        # Add the timeline to the bottom
        result = top_ + mixed + self.timeline.art
        return result

    def __mark_hour(self, hour:int) -> str:
        """
        Generate a marking line to visually represent the current hour
        on a numeric timeline.

        This method determines the stage of the given hour, then 
        identifies the position of each numeric value on the timeline.
        It creates a string where a caret (^) is placed at the position
        corresponding to the hour.

        Args:
            hour (int): The hour to mark on the timeline.

        Returns:
            str: A string with spaces and a caret (^) marking the
            position of the given hour.
        """
        stage = self.__determine_stage(hour)
        num_indexes = []
        for i, char in enumerate(self.numline):
            if (char.isnumeric() and
                not self.numline[i-1].isnumeric()):
                num_indexes.append(i)
        # Drop the last 6
        num_indexes.pop()
        hour_hash = {i:ind for i, ind in enumerate(num_indexes)}
        marking_line = ""
        mark_index = hour_hash[stage]
        for i, c in enumerate(self.numline):
            if i == mark_index:
                marking_line += "^"
            else:
                marking_line += " "

        return marking_line


    def __moonrise(self) -> str:
        """
        Generates the moonrise string by combining the sun and moon art
        with appropriate padding and adjustments.

        This method calculates the height difference between the sun and
        moon art, then constructs a moonrise scene by adjusting the
        padding and combining the sun and moon elements at the correct
        positions.

        Returns:
            str: The generated moonrise scene as a string.
        """
        __height_diff: int = self.__height_diff(
            self.half_sun_art, self.half_moon_art)
        # sun is bigger
        top_ = ""
        adjustment = (self.x_incr//2)
        top_pad_amount =self. x_incr*self.face_hours
        top_pad = self.pad_ * (top_pad_amount
                               + adjustment
                               - self.sun_pad)
        for top_r in self.half_sun_art[: __height_diff]:
            top_ += top_pad + top_r + "\n"
        mixed = ""
        for i, moon_ray in enumerate(self.half_moon_art):
            line_ = f"{self.pad_*adjustment}{moon_ray}"
            line_ += f"""{self.pad_ 
                          * (top_pad_amount- len(moon_ray)
                            - self.sun_pad)}{
                                self.half_sun_art[i+__height_diff]}"""
            mixed += line_ + "\n"
        result = top_ + mixed + self.timeline.art

        return result


    def __sun_route(self, stage) -> str:
        """
        Generates the sun's position based on the given stage of its
        movement.

        This method calculates the padding required for the sun's
        position based on the stage and updates its position on the
        timeline. The sun's position is adjusted depending on whether it
        is rising or setting.

        Args:
            stage (int): The current stage of the sun's movement,
                         indicating its position on the timeline.

        Returns:
            str: The generated string representing the sun's position at
                 the given stage.
        """
        # Setting how far sun is moving from left to right
        left_pad = self.pad_ * (self.x_incr * stage - self.sun_pad)
        padded_sun = [" " + left_pad + line for line in self.sun.lines]
        padded_sun_str = "\n".join(padded_sun)

        # Sun is rising
        if stage <= self.face_hours//2:
            padded_sun_str += "\n"*(stage)
        # Sun is setting
        else:
            padded_sun_str+= "\n"*(self.face_hours-stage)

        result = padded_sun_str + self.timeline.art
        return result


    def __moon_route(self, stage) -> str:
        """
        Generates the moon's position based on the given stage of its
        movement.

        This method calculates the padding required for the moon's
        position based on the stage and updates its position on the
        timeline. The moon's position is adjusted depending on whether
        it is rising or setting.

        Args:
            stage (int): The current stage of the moon's movement,
                         indicating its position on the timeline.

        Returns:
            str: The generated string representing the moon's position 
                 at the given stage.
        """
        left_pad = self.pad_ * (self.x_incr * stage )
        padded_moon = ["  " + left_pad + line for line
                       in self.moon_art.lines]
        padded_moon_str = "\n".join(padded_moon)

        # Moon is rising
        if stage <= self.face_hours//2:
            padded_moon_str += "\n"*(stage)

        # Moon is setting
        else:
            padded_moon_str+= "\n"*(self.face_hours-stage)
        result = padded_moon_str + self.timeline.art
        return result


    def __is_daytime(self, hour:int) -> bool:
        """
        Determines if the dial should be in the sun face or moon face
        based on the given hour.

        This method checks if the current hour falls within the daytime
        (sun face) or nighttime (moon face) range. It returns `True` if
        it is daytime, otherwise it returns `False`.

        Args:
            hour (int): The current hour to check.

        Returns:
            bool: `True` if it's daytime (sun face), `False` if it's
                  nighttime (moon face).
        """
        if (hour >= 18 or
            hour < 6):
            return False
        return True


    def __determine_stage(self, hour:int) -> int:
        """
        Converts the given hour to the corresponding sun or moon stage.

        This method calculates the stage of the sun or moon based on the
        provided hour. It adjusts the hour based on whether it is
        daytime or nighttime.

        Args:
            hour (int): The current hour to convert into a sun or moon
                        stage.

        Returns:
            int: The corresponding stage of the sun or moon. This is an
                 integer between 0 and 11, because it takes 12 steps for
                 the sun or the moon to get across the cycle.
        """
        if self.__is_daytime(hour):
            stage = hour - 6
            return stage
        else:
            if hour >= 18:
                stage = hour - 18
                return stage
            else:
                stage = hour + 6
                return stage


    def __print_dynamic_top_pad(self, hour, stage):
        """
        Prints the top padding based on the current hour and stage.

        This method prints additional newlines to adjust the positioning
        of the sun or moon depending on the provided hour and stage. It
        adjusts the top padding based on whether it is daytime or
        nighttime and the stage of the sun or moon.

        Args:
            hour (int): The current hour to determine whether it's day
                        or night.
            stage (int): The current stage of the sun or moon.
        """
        if not self.__is_daytime(hour):
            print("\n"*2)
        if stage < 6:
            print((self.top_pad-stage)*"\n")
        else:
            print((stage-self.top_pad)*"\n")


    def animate(self, iterations=int(), print_lag: float = 0.5):
        """
        Runs the dial in a loop starting from __sunrise, simulating the
        movement of the sun and moon across the sky.

        This method animates the dial by cycling through hours of the
        day (24-hour format), clearing the screen, and updating the dial
        for each hour. The animation can run for a specified number of
        iterations or indefinitely. The dial is displayed at a interval
        (print_lag).

        Args:
            iterations (int, optional): 
                        The number of times to run the animation loop.
                        If not provided, the loop runs indefinitely.
            print_lag (float): 
                        The time to wait between each frame of the
                        animation (in seconds).
        """
        start_time = 6 # Sunrise
        if iterations:
            if iterations <= 0 or not isinstance(iterations, int):
                exit("Iterations must be a positive integer")
            while iterations > 0:
                try:
                    for i in range(24):
                        hour = i+start_time % 24
                        subprocess.run("clear", shell=True)
                        self.show_dial(hour)
                        time.sleep(print_lag)
                    iterations -= 1
                except KeyboardInterrupt:
                    exit(f"\nKeyboard interrupt")

        else:
            while True:
                try:
                    for i in range(24):
                        hour = i+start_time % 24
                        subprocess.run("clear", shell=True)
                        self.show_dial(hour)
                        time.sleep(print_lag)

                except KeyboardInterrupt:
                    exit(f"\nKeyboard interrupt")


    def show_dial(self, current_hour=None):
        """
        Creates and prints the dial based on the current hour.

        This method generates and prints the visual representation of
        the dial, adjusting the sun or moon's position based on the
        current hour. It calculates the appropriate stage and determines
        if it is day or night, printing the corresponding __sunrise, sun
        route, __moonrise, or moon route.

        Args:
            current_hour (int, optional): 
                                The current hour to display on the dial.
                                If not provided, the current system hour
                                is used.
        """
        print(self.time_face.horisontal)

        if not current_hour:
            current_hour = datetime.now().hour

        stage = self.__determine_stage(current_hour)

        self.__print_dynamic_top_pad(hour=current_hour, stage=stage)

        if self.__is_daytime(current_hour):
            if stage == 0:
                print(self.__sunrise())
            else:
                print(self.__sun_route(stage=stage))
        else:
            if stage == 0:
                print(self.__moonrise())
            else:
                print(self.__moon_route(stage=stage))
        print(self.__mark_hour(current_hour))

        print(self.time_face.overline)


if __name__ == "__main__":
    dial_ = TimeDial()
    dial_.animate(print_lag=0.1)