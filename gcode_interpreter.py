import sys
from typing import TextIO
from auxiliary import *
from machineClient import MachineClient


G54_FIXED_POINT = (10, 10, 10)  # constant (X, Y, Z) that changes coordinate's fixed point when G54 is called


def interpreter(gcode: TextIO) -> None:
    count: int = 0  # Counter variable
    home_position: tuple[float, float, float] = (0.0, 0.0, 0.0)
    X, Y, Z = home_position
    X_temp, Y_temp, Z_temp = home_position  # Temporary values
    datum: tuple = home_position  # Initially datum == home_position

    # Variables for modal commands
    spindle_speed: int = 0
    tool_name: str = ""
    feed_rate: float = 0.0
    absolute_mode: bool = False  # Absolute mode on
    rapid_mode: bool = False  # Rapid mode on

    # Parsing
    for line in gcode:
        X_set: bool = False  # Line contains variable X
        Y_set: bool = False  # Line contains variable Y
        Z_set: bool = False  # Line contains variable Z
        # Skip possible empty lines
        if line == '\n':
            continue
        # Check for '%' in the beginning
        if count == 0:
            if line.strip() != '%':
                raise Exception("Gcode syntax incorrect: No '%' found.")
            count += 1
        # Skip comments
        if line.strip().startswith('('):
            continue
        # Process O header
        elif line.strip().startswith('O') and count == 1:
            print(f"Executing program {line.strip()}...")
            count += 1
        # Process N commands
        else:
            if line.strip().startswith('N'):
                print('\n' + line.split()[0])
                parameters: list[str] = line[1:].lstrip("0123456789.- ").split()
                # Parse instructions
                parameters: list[str] = sorted(parameters, reverse=True)
                for parameter in parameters:
                    first_letter: str = parameter[0]
                    num: str = parameter[1:]
                    if first_letter == 'G':
                        if num == '00':
                            if not rapid_mode:
                                rapid_mode = True
                                MachineClient().rapid_mode()
                            if absolute_mode:
                                X = X_temp + datum[0]
                                Y = Y_temp + datum[1]
                                Z = Z_temp + datum[2]
                            else:
                                X += X_temp
                                Y += Y_temp
                                Z += Z_temp
                            if X_set:
                                MachineClient().move_x(X)
                                if Y_set:
                                    MachineClient().move_y(Y)
                                elif Z_set:
                                    MachineClient().move_z(Z)
                            elif Y_set:
                                MachineClient().move_y(Y)
                                if Z_set:
                                    MachineClient().move_z(Z)
                            elif Z_set:
                                MachineClient().move_z(Z)
                            else:
                                pass
                            X_set = False
                            Y_set = False
                            Z_set = False
                        elif num == '01':
                            if rapid_mode:
                                rapid_mode = False
                                MachineClient().interpolation_mode()
                            if absolute_mode:
                                X = X_temp + datum[0]
                                Y = Y_temp + datum[1]
                                Z = Z_temp + datum[2]
                            else:
                                X += X_temp
                                Y += Y_temp
                                Z += Z_temp
                            MachineClient().move(X, Y, Z)
                        elif num == '17':
                            MachineClient().plane_selection("XY")
                        elif num == '21':
                            MachineClient().metric_mode()
                        elif num == '28':
                            X, Y, Z = home_position
                            MachineClient().home()
                        elif num == '40':
                            MachineClient().canel_cutter()
                        elif num == '49':
                            MachineClient().cancel_tool_length()
                        elif num == '54':
                            datum = G54_FIXED_POINT  # A new fixed point
                            X, Y, Z = change_datum(datum, X, Y, Z)  # Auxiliary function that switches coordinate
                            # positions in accordance with the new datum
                            MachineClient().work_offset('G54', datum)
                        elif num == '80':
                            MachineClient().cancel_canned_cycle()
                        elif num == '90':
                            absolute_mode = True
                            MachineClient().absolute_mode()
                        elif num == '91':
                            absolute_mode = False
                            MachineClient().incremental_mode()
                        elif num == '94':
                            MachineClient().command_interpret()
                    elif first_letter == 'X':
                        X_set = True
                        X_temp = error_check(num)
                    elif first_letter == 'Y':
                        Y_set = True
                        Y_temp = error_check(num)
                    elif first_letter == 'Z':
                        Z_set = True
                        Z_temp = error_check(num)
                    elif first_letter == 'F':
                        feed_rate = error_check(num)
                        MachineClient().set_feed_rate(feed_rate)
                    elif first_letter == 'T':
                        tool_name = parameter
                    elif first_letter == 'M':
                        if num == '03':
                            MachineClient().set_spindle_speed(spindle_speed)
                            MachineClient().coolant_on()
                        elif num == '05':
                            MachineClient().stop_spindle()
                        elif num == '06':
                            MachineClient().change_tool(tool_name)
                        elif num == '09':
                            MachineClient().coolant_off()
                        elif num == '30':
                            MachineClient().program_quit()
                    elif first_letter == 'S':
                        spindle_speed = error_check(num)
                    else:
                        raise Exception("Gcode syntax incorrect: Command letter not recognized.")


if __name__ == "__main__":
    sys.tracebacklimit = 0  # Remove error traceback information
    gcode_file = None
    file_name: str = arg_parser()

    if not file_name.endswith("gcode"):
        print("Add a gcode file")
    else:
        with open(file_name, "r") as gcode_file:
            interpreter(gcode_file)

