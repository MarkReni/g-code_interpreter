import unittest
from io import StringIO
import sys
import gcode_interpreter as gcode


class Test(unittest.TestCase):
    def test_syntax_1(self):
        self.input_file = StringIO()
        self.input_file.write("\n\n\n%\n\n\n")
        self.input_file.write("N1 G00 G17 G21 G40 G49 G80 G94")
        self.input_file.seek(0, 0)

        self.interpreter_output = StringIO()
        sys.stdout = self.interpreter_output

        gcode.interpreter(self.input_file)
        self.input_file.close()

        self.assertEqual(
            '''\nN1
Interpretation of commands are now as mm/minute for linear moves.
Canned cycle has been cancelled.
Tool length compensation has been cancelled.
Cutter compensation has been turned off.
Machine has been switched into metric mode.
XY plane selected as rotational axis.
Rapid positioning turned on.\n''', self.interpreter_output.getvalue())

    def test_syntax_2(self):
        self.input_file = StringIO()
        self.input_file.write("\n")
        self.input_file.write("N5 G90 G01 X-12.000 Y-12.000\n")
        self.input_file.write("N6 G01 Y-12.000\n")
        self.input_file.seek(0, 0)

        with self.assertRaises(Exception):
            gcode.interpreter(self.input_file)

        self.input_file.close()

    def test_syntax_3(self):
        self.input_file = StringIO()
        self.input_file.write("\n")
        self.input_file.write("N5 G90 G01 X-12.000 Y-12.000\n")
        self.input_file.write("N6 A01 Y-12.000\n")
        self.input_file.seek(0, 0)

        with self.assertRaises(Exception):
            gcode.interpreter(self.input_file)

        self.input_file.close()

    def test_syntax_4(self):
        self.input_file = StringIO()
        self.input_file.write("%\n")
        self.input_file.write("N5 G90 G01 X-12.000 Y-12.000\n")
        self.input_file.write("N6 G01 Y.-12.000\n")
        self.input_file.seek(0, 0)

        with self.assertRaises(Exception):
            gcode.interpreter(self.input_file)

        self.input_file.close()

    def test_absolute_positioning(self):
        self.input_file = StringIO()
        self.input_file.write("%\n")
        self.input_file.write("N5 G90 G01 X-12.000 Y-12.000\n")
        self.input_file.write("N6 G01 X90.000 Y-90.000 Z30.000\n")
        self.input_file.write("N7 G01 Y-12.000\n")
        self.input_file.seek(0, 0)

        self.interpreter_output = StringIO()
        sys.stdout = self.interpreter_output

        gcode.interpreter(self.input_file)
        self.input_file.close()

        self.assertIn("Moving to X=-12.000 Y=-12.000 Z=0.000 [mm].", self.interpreter_output.getvalue().split('\n'))
        self.assertIn("Moving to X=90.000 Y=-90.000 Z=30.000 [mm].", self.interpreter_output.getvalue().split('\n'))
        self.assertIn("Moving to X=90.000 Y=-12.000 Z=30.000 [mm].", self.interpreter_output.getvalue().split('\n'))

    def test_incremental_positioning(self):
        self.input_file = StringIO()
        self.input_file.write("%\n")
        self.input_file.write("N5 G91 G01 X-20.000 Y-10.000\n")
        self.input_file.write("N6 G01 X-20.000 Y-10.000 Z15.000\n")
        self.input_file.write("N7 G00 Z-10.000\n")
        self.input_file.seek(0, 0)

        self.interpreter_output = StringIO()
        sys.stdout = self.interpreter_output

        gcode.interpreter(self.input_file)
        self.input_file.close()

        self.assertIn("Moving to X=-20.000 Y=-10.000 Z=0.000 [mm].", self.interpreter_output.getvalue().split('\n'))
        self.assertIn("Moving to X=-40.000 Y=-20.000 Z=15.000 [mm].", self.interpreter_output.getvalue().split('\n'))
        self.assertIn("Moving Z to 5.000 [mm].", self.interpreter_output.getvalue().split('\n'))

    def test_work_offset(self):
        self.input_file = StringIO()
        self.input_file.write("%\n")
        self.input_file.write("N5 G90 G01 X-12.000 Y-12.000\n")
        self.input_file.write("N6 G01 G54 X20.000 Y10.000\n")
        self.input_file.seek(0, 0)

        self.interpreter_output = StringIO()
        sys.stdout = self.interpreter_output

        gcode.interpreter(self.input_file)
        self.input_file.close()

        self.assertIn("Moving to X=-12.000 Y=-12.000 Z=0.000 [mm].", self.interpreter_output.getvalue().split('\n'))
        self.assertIn("Changing work offset to 'G54' having fixed point at X = 10, Y = 10, Z = 10.",
                      self.interpreter_output.getvalue().split('\n'))
        self.assertIn("Moving to X=30.000 Y=20.000 Z=10.000 [mm].", self.interpreter_output.getvalue().split('\n'))

    def test_positions_together(self):
        self.input_file = StringIO()
        self.input_file.write("%\n")
        self.input_file.write("N5 G90 G01 X-20.000 Y-15.000 Z10.000\n")
        self.input_file.write("N5 G91 G01 X-20.000 Y-10.000 Z50.000\n")
        self.input_file.write("N6 G01 G54 X20.000 Y10.000 Z-20.00\n")
        self.input_file.seek(0, 0)

        self.interpreter_output = StringIO()
        sys.stdout = self.interpreter_output

        gcode.interpreter(self.input_file)
        self.input_file.close()

        self.assertIn("Moving to X=-20.000 Y=-15.000 Z=10.000 [mm].", self.interpreter_output.getvalue().split('\n'))
        self.assertIn("Moving to X=-40.000 Y=-25.000 Z=60.000 [mm].", self.interpreter_output.getvalue().split('\n'))
        self.assertIn("Moving to X=-10.000 Y=-5.000 Z=50.000 [mm].", self.interpreter_output.getvalue().split('\n'))