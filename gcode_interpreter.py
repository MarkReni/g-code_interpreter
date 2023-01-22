import argparse
import sys


class MachineClient:
    def home(self):
        """ Moves machine to home position. """

        print("Moving to home.")

    def move(self, x, y, z):
        """ Uses linear movement to move spindle to given XYZ
        coordinates.
        Args:
        x (float): X axis absolute value [mm]
        y (float): Y axis absolute value [mm]
        z (float): Z axis absolute value [mm]
        """

        print("Moving to X={:.3f} Y={:.3f} Z={:.3f} [mm].".format(x, y,
                                                                  z))

    def move_x(self, value):
        """ Move spindle to given X coordinate. Keeps current Y and Z
        unchanged.
        Args:
        value (float): Axis absolute value [mm]
        """

        print("Moving X to {:.3f} [mm].".format(value))

    def move_y(self, value):
        """ Move spindle to given Y coordinate. Keeps current X and Z
        unchanged.
        Args:
        value(float): Axis absolute value [mm]
        """

        print("Moving Y to {:.3f} [mm].".format(value))

    def move_z(self, value):
        """ Move spindle to given Z coordinate. Keeps current X and Y
        unchanged.
        Args:
        value (float): Axis absolute value [mm]
        """

        print("Moving Z to {:.3f} [mm].".format(value))

    def set_feed_rate(self, value):
        """ Set spindle feed rate.
        Args:
        value (float): Feed rate [mm/s]
        """

        print("Using feed rate {} [mm/s].".format(value))

    def set_spindle_speed(self, value):
        """ Set spindle rotational speed.
        Args:
        value (int): Spindle speed [rpm]
        """

        print("Using spindle speed {} [mm/s].".format(value))

    def change_tool(self, tool_name):
        """ Change tool with given name.
        Args:
        tool_name (str): Tool name.
        """

        print("Changing tool '{:s}'.".format(tool_name))

    def coolant_on(self):
        """ Turns spindle coolant on. """

        print("Coolant turned on.")

    def coolant_off(self):
        """ Turns spindle coolant off. """

        print("Coolant turned off.")


def argParser() -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument("gcode_file", type=str)

    args = parser.parse_args()

    file_name = args.gcode_file
    print("A file with the following ending has been added:", file_name[-5:])

    return file_name


def error_check(literal: str) -> float:
    try:
        conversion = float(literal)
    except ValueError:
        raise Exception("Gcode syntax incorrect")
    else:
        return conversion


def interpreter(gcode):
    count = 0
    for line in gcode:
        # check '#' in the beginning
        if count == 0:
            if line.strip() != '%':
                raise Exception("Gcode syntax incorrect")
            count += 1
        if line.strip()[0] == "(" or line.strip()[
                                     0:3] == "N1 ":  # also skippern machine initialisation gcode "N1 G00 G17 G21 G40 G49 G80 G94"
            continue
        else:
            if line[0] == 'N':
                # parameters
                spindle_speed = 0
                tool_name = ""
                feed_rate = 0
                X = 0.0
                Y = 0.0
                Z = 0.0

                print(f"Line {line[0:3]}")

                parameters = line[1:].lstrip('0123456789.- ').split()

                # parse instructions
                for parameter in parameters:
                    first_letter = parameter[0]
                    num = parameter[1:]

                    if first_letter == 'G':
                        if num == '00':
                            pass
                        elif num == '01':
                            pass
                        elif num == '28':
                            CNC_machine.home()
                        elif num == '54':
                            pass
                        elif num == '90':
                            pass
                        elif num == '91':
                            pass
                    elif first_letter == 'X':
                        X = error_check(num)
                    elif first_letter == 'Y':
                        Y = error_check(num)
                    elif first_letter == 'Z':
                        Z = error_check(num)
                    elif first_letter == 'F':
                        feed_rate = error_check(num)
                        CNC_machine.set_feed_rate(feed_rate)
                    elif first_letter == 'T':
                        tool_name = parameter
                    elif first_letter == 'M':
                        if num == '03':
                            CNC_machine.set_spindle_speed(spindle_speed)
                        elif num == '05':
                            pass
                        elif num == '06':
                            CNC_machine.change_tool(tool_name)
                        elif num == '09':
                            CNC_machine.coolant_off()
                        elif num == '30':
                            pass
                    elif first_letter == 'S':
                        try:
                            spindle_speed = int(num)
                        except ValueError:
                            raise Exception("Gcode syntax incorrect")


if __name__ == "__main__":
    sys.tracebacklimit = 0  # remove error traceback information
    CNC_machine = MachineClient()
    gcode_file = None
    file_name = argParser()

    if file_name[-5:] != "gcode":
        print("Add a gcode file")
    else:
        with open(file_name, "r") as gcode:
            interpreter(gcode)

