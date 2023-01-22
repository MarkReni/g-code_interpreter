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

    def absolute_mode(self):
        """ Turns absolute mode on (G90). """

        print("Absolute positioning turned on.")

    def incremental_mode(self):
        """ Turns incremental mode on G(91). """

        print("Incremental positioning turned on.")

    def rapid_mode(self):
        """ Turns rapid positioning mode on (G00). """

        print("Rapid positioning turned on.")

    def interpolation_mode(self):
        """ Turns linear interpolation mode on (G01). """

        print("Linear interpolation turned on.")

    def stop_spindle(self):
        """ Stops spindle from turning (M05). """

        print("Spindle stopped from turning.")

    def work_offset(self, gcode: str, datum: tuple):
        """ Changes work offset and datum (G54 - G59). """

        print("Changing work offset to '{:s}' having fixed point at X = {:d}, Y = {:d}, Z = {:d}.".format(gcode, datum[0], datum[1], datum[2]))

    def command_interpret(self):
        """ Instruct the control to interpret feed commands as mm/minute for linear moves. """

        print("Interpretation of commands are now as mm/minute for linear moves.")

    def cancel_canned_cycle(self):
        """ Cancels any fixed cycle. """

        print("Canned cycle has been cancelled.")

    def cancel_tool_length(self):
        """ Cancels tool length compensation. """

        print("Tool length compensation has been cancelled.")

    def canel_cutter(self):
        """ Turn off cutter compensation. """

        print("Cutter compensation has been turned off.")

    def metric_mode(self):
        """ Switch the CNC into metric mode. """

        print("Machine has been switched into metric mode.")

    def plane_selection(self, plane: str):
        """ Select the working plane.  """

        print(f"{plane} plane selected as rotational axis.")

    def program_quit(self):
        print("Program quitting...")
        CNC_machine.coolant_off()
        CNC_machine.stop_spindle()
        CNC_machine.home()
        quit()


# Auxiliary functions
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
    # variables for modal commands
    spindle_speed = 0
    tool_name = ""
    feed_rate = 0.0
    absolute_mode = False  # absolute mode on
    rapid_mode = False
    home_position = (0.0, 0.0, 0.0)
    X, Y, Z = home_position
    datum = home_position

    # Auxiliary function for G54
    def change_datum(datum, X, Y, Z):
        X, Y, Z = X + datum[0], Y + datum[1], Z + datum[2]
        return (X, Y, Z)

    for line in gcode:
        X_set = False
        Y_set = False
        Z_set = False
        # Check '#' in the beginning
        if count == 0:
            if line.strip() != '%':
                raise Exception("Gcode syntax incorrect")
            count += 1
        # Skip comments
        if line.strip()[0] == "(":
            continue
        # Process N commands
        elif line.strip()[0] == 'O' and count == 1:
            print(f"Executing program {line.strip()}...")
            count += 1
        else:
            if line.strip()[0] == 'N':
                print(line.split()[0])
                parameters = line[1:].lstrip('0123456789.- ').split()
                # parse instructions
                parameters = sorted(parameters, reverse=True)
                for parameter in parameters:
                    first_letter = parameter[0]
                    num = parameter[1:]
                    if first_letter == 'G':
                        if num == '00':
                            if not rapid_mode:
                                rapid_mode = True
                                CNC_machine.rapid_mode()
                            if absolute_mode:
                                if X_set:
                                    CNC_machine.move_x(X)
                                    if Y_set:
                                        CNC_machine.move_y(Y)
                                    elif Z_set:
                                        CNC_machine.move_z(Z)
                                elif Y_set:
                                    CNC_machine.move_y(Y)
                                    if Z_set:
                                        CNC_machine.move_z(Z)
                                elif Z_set:
                                    CNC_machine.move_z(Z)
                                else:
                                    pass
                            X_set = False
                            Y_set = False
                            Z_set = False
                        elif num == '01':
                            if rapid_mode:
                                rapid_mode = False
                                CNC_machine.interpolation_mode()
                            if absolute_mode:
                                CNC_machine.move(X, Y, Z)
                        elif num == '17':
                            CNC_machine.plane_selection("XY")
                        elif num == '21':
                            CNC_machine.metric_mode()
                        elif num == '28':
                            X, Y, Z = home_position
                            CNC_machine.home()
                        elif num == '40':
                            CNC_machine.canel_cutter()
                        elif num == '49':
                            CNC_machine.cancel_tool_length()
                        elif num == '54':
                            datum = (10, 10, 10)    # new fixed point, trivially selected
                            X, Y, Z = change_datum(datum, X, Y, Z)  # auxiliary function that switches coordinate positions in accordance with the new datum
                            CNC_machine.work_offset('G54', datum)
                        elif num == '80':
                            CNC_machine.cancel_canned_cycle()
                        elif num == '90':
                            absolute_mode = True
                            CNC_machine.absolute_mode()
                        elif num == '91':
                            absolute_mode = False
                            CNC_machine.incremental_mode()
                        elif num == '94':
                            CNC_machine.command_interpret()
                    elif first_letter == 'X':
                        X_set = True
                        X_temp = error_check(num)
                        X = X_temp + datum[0]
                    elif first_letter == 'Y':
                        Y_set = True
                        Y_temp = error_check(num)
                        Y = Y_temp + datum[1]
                    elif first_letter == 'Z':
                        Z_set = True
                        Z_temp = error_check(num)
                        Z = Z_temp + datum[2]
                    elif first_letter == 'F':
                        feed_rate = error_check(num)
                        CNC_machine.set_feed_rate(feed_rate)
                    elif first_letter == 'T':
                        tool_name = parameter
                    elif first_letter == 'M':
                        if num == '03':
                            CNC_machine.set_spindle_speed(spindle_speed)
                            CNC_machine.coolant_on()
                        elif num == '05':
                            CNC_machine.stop_spindle()
                        elif num == '06':
                            CNC_machine.change_tool(tool_name)
                        elif num == '09':
                            CNC_machine.coolant_off()
                        elif num == '30':
                            CNC_machine.program_quit()
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

