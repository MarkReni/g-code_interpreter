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

        print(
            "Changing work offset to '{:s}' having fixed point at X = {:d}, Y = {:d}, Z = {:d}."
                .format(gcode, datum[0], datum[1], datum[2]))

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
        self.coolant_off()
        self.stop_spindle()
        self.home()
        sys.exit()
