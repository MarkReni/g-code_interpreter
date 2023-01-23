# g-code_interpreter                                                                     Author: Mark Renssi 23.01.2023


## G-Code Interpreter Task

Implemented partially compliant G-Code interpreter with a limited subset of functions required to carry out the given
tasks. Stub functions which simply print out comments, have been set for all G-Code commands presented in the 
assignment file. 

Three files have been created for this assignment:
- gcode_interpreter.py contains interpreter function which in limited extend checks that the opened file is in 
  accordance with gcode syntax rules, and then parses the instructions/commands to MachineClient. Also, 
  __name__ == "__main__": is located here. 
- auxiliary.py file contains some auxiliary functions that have been created mainly for the reasons of refactoring, 
  value conversion and maintainability. 
- test.py contains unit tests for syntax error detection and positioning. 

## Other info
- Conda environment and Python 3.9 were used for this task.



