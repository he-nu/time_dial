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


    moon_string = sun_and_moon.MOON2
    sun_string = sun_and_moon.SUN
    moon_art = Art(moon_string)
    sun = Art(sun_string)
    timeline = Art(time_line_art)
    numline = time_face.numline

    face_hours = 12 # Clock face indexes
    x_incr = 5 # shift in white space per hour
    sun_pad = 4 # sun needs a negative pad
    top_pad = 6
    pad_ = " "   
    half_sun = sun.lines[: (len(sun.lines) // 2) + 1]
    half_moon_art = moon_art.lines[: (len(moon_art.lines) // 2) + 1]


    def h_diff(self, art1:list, art2:list) -> int:
        return abs(len(art1)-len(art2))

    def sunrise(self) -> str:
        """Generates the sunrise string."""
        # Sunrise, moonset
        # moon_pos = timeline.W - moon_art.W // 2
        height_diff = self.h_diff(self.half_sun, self.half_moon_art)
        top_ = "\n" * 3
        # adjusting for the sun art is bigger
        for top_r in self.half_sun[: height_diff]:
            top_ += top_r[self.sun_pad:] + "\n"
        mixed = ""
        for i, sun_ray in enumerate(self.half_sun[height_diff:]):
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

    def mark_hour(self, hour):
        stage = self.determine_stage(hour)
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

    def moonrise(self) -> str:
        "Genarates the moonrise string."
        height_diff: int = self.h_diff(self.half_sun, self.half_moon_art)
        # sun is bigger
        top_ = ""
        adjustment = (self.x_incr//2)
        top_pad_amount =self. x_incr*self.face_hours
        top_pad = self.pad_* (top_pad_amount + adjustment - self.sun_pad)
        for top_r in self.half_sun[: height_diff]:
            top_ += top_pad + top_r + "\n"
        mixed = ""
        for i, moon_ray in enumerate(self.half_moon_art):
            line_ = f"{self.pad_*adjustment}{moon_ray}"
            line_ += f"""{self.pad_ 
                          * (top_pad_amount- len(moon_ray)
                            - self.sun_pad)}{
                                self.half_sun[i+height_diff]}"""
            mixed += line_ + "\n"
        result = top_ + mixed + self.timeline.art

        return result


    def sun_route(self, stage) -> str:
        """ Generates sun's position based on the stage."""

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


    def moon_route(self, stage) -> str:
        """ Generates moon's position based on the stage."""
        left_pad = self.pad_ * (self.x_incr * stage )
        padded_moon = ["  " + left_pad + line for line in self.moon_art.lines]
        padded_moon_str = "\n".join(padded_moon)

        # Moon is rising
        if stage <= self.face_hours//2:
            padded_moon_str += "\n"*(stage)

        # Moon is setting
        else:
            padded_moon_str+= "\n"*(self.face_hours-stage)
        result = padded_moon_str + self.timeline.art
        return result


    def is_daytime(self, hour:int) -> bool:
        """ 
        Determines if the dial should be in the sun face or moon face.
        """
        if (hour >= 18 or
            hour < 6):
            return False
        return True

    def determine_stage(self, hour) -> int:
        """ Converts hour to the sun/moon stage."""
        if self.is_daytime(hour):
            stage = hour - 6
            return stage
        else:
            if hour >= 18:
                stage = hour - 18
                return stage
            else:
                stage = hour + 6
                return stage


    def print_dynamic_top_pad(self, hour, stage):
        """ Prints top pad based on hour and stage"""
        if not self.is_daytime(hour):
            print("\n"*2)
        if stage < 6:
            print((self.top_pad-stage)*"\n")
        else:
            print((stage-self.top_pad)*"\n")

    def animate(self, iterations=None ,sleep_time=0.5):
        """ Runs the dial in a loop starting from sunrise."""
        start_time = 6
        if iterations:
            if iterations <= 0 or not isinstance(iterations, int):
                exit("Iterations must be a positive integer")
            while iterations > 0:
                try:
                    for i in range(24):
                        hour = i+start_time % 24
                        subprocess.run("clear", shell=True)
                        self.show_dial(hour)
                        time.sleep(sleep_time)
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
                        time.sleep(sleep_time)

                except KeyboardInterrupt:
                    exit(f"\nKeyboard interrupt")


    def show_dial(self, current_hour=None):
        """ Creates the dial print based on the current hour. """

        print(self.time_face.horisontal)

        if not current_hour:
            current_hour = datetime.now().hour

        stage = self.determine_stage(current_hour)

        self.print_dynamic_top_pad(hour=current_hour, stage=stage)

        if self.is_daytime(current_hour):
            if stage == 0:
                print(self.sunrise())
            else:
                print(self.sun_route(stage=stage))
        else:
            if stage == 0:
                print(self.moonrise())
            else:
                print(self.moon_route(stage=stage))
        print(self.mark_hour(current_hour))

        print(self.time_face.overline)


if __name__ == "__main__":
    dial_ = TimeDial()
    dial_.animate(1)