'''
    The pynnacle-genesis module provides a beginner-friendly programming experience in Python, inspired by popular development board environments (see full description below).

    Copyright (C) 2025 Rafael Red Angelo M. Hizon, Jenel M. Justo, and Serena Mae C.S. Lee

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

    This module was built on top of Pymata4 by Alan Yorinks - <https://github.com/MrYsLab/pymata4/>
'''

'''
    The pynnacle-genesis module was initially crafted for the readers of Python Odyssey: Into the World of Robotics by Team Pinnacle, 
    complementing the Pinnacle Genesis board featured in the book. Built on the robust foundation of Pymata4 by Alan Yorinks, it provides
    novice enthusiasts with a hands-on coding experience in Python that mirrors the structure and functionality of popular development 
    board environments. The primary motivation behind its creation is to facilitate a smoother transition for learners as they delve into
    the complexities of robotics programming, bridging the gap between beginner-friendly Python and the more intricate structures found in
    languages for widely-used development boards.

    DISCLAIMER:
        Some functions within this module have been adjusted to produce specific outcomes that align with the book's content and 
        teaching objectives. Additionally, certain functions in this module may not be available in other development board environments.
        These adaptations were implemented to harmonize with the book's mission: to introduce robotics to absolute beginners in a simplified
        and intuitive way.

    TEAM PINNACLE:
        1. Red Hizon
        2. Jenel Justo
        3. Serena Lee
'''

# IMPORTS
from time import sleep
import re, serial, os, sys, atexit, signal


# --- BEGIN: SERIAL DTR PATCH ---
_original_serial_init = serial.Serial.__init__

def _patched_serial_init(self, *args, **kwargs):
    _original_serial_init(self, *args, **kwargs)
    self.setDTR(False)  # Disable reset on connection

serial.Serial.__init__ = _patched_serial_init
# --- END: SERIAL DTR PATCH ---

# --- BEGIN: STYLING ---
# Original stdout (so we can restore it later)
_original_stdout = sys.stdout

# Function to disable printing
def _suppress_print():
    sys.stdout = open(os.devnull, 'w')

# Function to enable printing again
def _enable_print():
    sys.stdout = _original_stdout

# Text styles for the info function
class _Style:
    _BOLD = '\033[1m'
    _ITALIC = '\033[3m'
    _UNDERLINE = '\033[4m'
    _COLOR_BLUE = '\033[94m'
    _COLOR_RED = '\033[91m'
    _COLOR_DARK_GRAY = '\033[90m'  # Bright Black / Dark Gray
    _COLOR_LIGHT_CYAN = '\033[96m'  # Light Cyan for system notifications
    _RESET = '\033[0m'  # Reset to default

    @staticmethod
    def info():
        print("\n")
        formatted_text = (
            f"\n{_Style._COLOR_DARK_GRAY}pymata: Version 1.15"
            f"\nCopyright (c) 2020 Alan Yorinks All Rights Reserved.\n\n\n\n"
            f"\n{_Style._COLOR_BLUE}{_Style._BOLD}THE PYNNACLE-GENESIS{_Style._RESET}\n\n"
            f"This module is tailored for beginners in robotics and programming,\n"
            f'originally for readers of "{_Style._COLOR_BLUE}{_Style._ITALIC}Python Odyssey: Into the World of Robotics{_Style._RESET}" by {_Style._BOLD}{_Style._COLOR_BLUE}Team Pinnacle{_Style._RESET}.\n'
            f"Based on {_Style._ITALIC}Pymata4{_Style._RESET}, it provides a Python-based robotics coding experience inspired by popular development board environments.\n"
            f"The main goal is to ease the learning curve for beginners by bridging the gap between Python's simplicity\n"
            f"and the more complex structures often found in other board programming environments.\n\n"
            f"{_Style._ITALIC}This work requires attribution if you modify and distribute it and its derivatives.\nYou can find the attribution requirement towards the end of the license document.{_Style._RESET}\n\n"
            f"{_Style._COLOR_BLUE}{_Style._BOLD}Copyright (c) 2025 {_Style._RESET}{_Style._COLOR_BLUE}{_Style._UNDERLINE}Rafael Red Angelo M. Hizon{_Style._RESET}, {_Style._COLOR_BLUE}{_Style._UNDERLINE}Jenel M. Justo{_Style._RESET}, {_Style._COLOR_BLUE}{_Style._UNDERLINE}Serena Mae C.S. Lee\n{_Style._RESET}"
        )
        print(formatted_text)

    @staticmethod
    def print_error_message(err=None):
        error_prompt = f"\n{_Style._BOLD}{_Style._COLOR_RED}Error:{_Style._RESET} The computer failed to communicate with the board."
        possible_solutions = [
            "1. Check the board connection (ensure USB cable is firmly plugged in).",
            "2. Ensure the board is properly powered (check the board's power light).",
            "3. Verify that the board's driver is properly installed.",
            "4. Check for any hardware failures or conflicts.",
            "5. Disconnect the components before you run your code.",
            "6. Press the reset button on the Genesis board before running your code.",
            "7. If problems persist, try restarting your computer."
        ]
        print(error_prompt)
        print(f"\n{_Style._COLOR_BLUE}{_Style._BOLD}Possible Solutions:{_Style._RESET}")
        for solution in possible_solutions:
            print(f"  {solution}")

        # Uncomment this if-statement for debugging; comment out before deploying to avoid confusing beginners.
        if err and os.path.exists("debug_config.txt"):
            print(f"\nInternal error details (for advanced users/troubleshooting): {err}")

    @staticmethod
    def print_function_error(func_name, err=None):
        error_prompt = f"\n{_Style._BOLD}{_Style._COLOR_RED}Error:{_Style._RESET} An unexpected error occurred inside {func_name}. Please check your function parameters."
        print(error_prompt)
        if err and os.path.exists("debug_config.txt"):
            print(f"\nInternal error details (for advanced users/troubleshooting): {err}")
        # Always attempt to shut down on function error before exiting
        _cleanup_board_on_exit()
        sys.exit(1)
# --- END: STYLING ---

# --- BEGIN: BOARD MANAGEMENT & INSTANTIATION ---
_board = None
_analog_input_pins = set()
_digital_input_pins = set()
_ultrasonic_trigger_pins = set()


def _cleanup_board_on_exit():
    global _board
    if _board:
        # Re-enable printing for shutdown messages, but don't force it if already enabled
        # This prevents breaking user's print output if they manually re-enable print
        current_stdout = sys.stdout
        sys.stdout = _original_stdout  # Ensure output goes to console during shutdown
        print(f"\n{_Style._COLOR_LIGHT_CYAN}{_Style._COLOR_LIGHT_CYAN}[Pynnacle-Genesis]{_Style._RESET}{_Style._RESET} Shutting down board connection gracefully...")

        # Explicitly disable reporting for digital input pins
        for pin in list(_digital_input_pins):
            try:
                print(f"{_Style._COLOR_LIGHT_CYAN}[Pynnacle-Genesis]{_Style._RESET} Disabling digital input reporting on pin D{pin}...")
                _board.disable_digital_reporting(pin)
                _digital_input_pins.remove(pin)
            except Exception:
                print(f"{_Style._COLOR_LIGHT_CYAN}[Pynnacle-Genesis]{_Style._RESET} Warning: Could not disable digital input reporting on pin D{pin}")

        # Explicitly disable reporting for analog input pins
        for pin in list(_analog_input_pins):
            try:
                print(f"{_Style._COLOR_LIGHT_CYAN}[Pynnacle-Genesis]{_Style._RESET} Disabling analog input reporting on pin A{pin}...")
                _board.disable_analog_reporting(pin)
                _analog_input_pins.remove(pin)
            except Exception:
                print(f"{_Style._COLOR_LIGHT_CYAN}[Pynnacle-Genesis]{_Style._RESET} Warning: Could not disable analog input reporting on pin A{pin}")

        # Explicitly stop sonar reporting for any active sonar pins
        for trigger_pin in list(_ultrasonic_trigger_pins):
            try:
                print(f"{_Style._COLOR_LIGHT_CYAN}[Pynnacle-Genesis]{_Style._RESET} Stopping sonar on pin D{trigger_pin}...")
                # Setting pin back to digital input should stop sonar reporting
                _board.set_pin_mode_digital_input(trigger_pin)
                _board.disable_digital_reporting(trigger_pin)
                _ultrasonic_trigger_pins.remove(trigger_pin)
            except Exception:
                print(f"{_Style._COLOR_LIGHT_CYAN}[Pynnacle-Genesis]{_Style._RESET} Warning: Could not stop sonar on pin {trigger_pin}")

        # Add a small delay here before shutdown, to ensure any last commands are sent
        sleep(0.5)
        _board.shutdown()

        print(f"{_Style._COLOR_LIGHT_CYAN}[Pynnacle-Genesis]{_Style._RESET} Board connection closed.")
        _board = None

# Register the cleanup function to run automatically when Python exits
atexit.register(_cleanup_board_on_exit)


# Handle Ctrl+C (SIGINT) to ensure a clean exit and atexit call
def _signal_handler(signum, frame):
    # sys.exit(0) will trigger atexit handlers
    sys.exit(0)

signal.signal(signal.SIGINT, _signal_handler)

print(f"\n{_Style._COLOR_LIGHT_CYAN}[Pynnacle-Genesis]{_Style._RESET} Setting things up for you. Hang tight...")
_suppress_print()  # Suppress internal output to maintain clarity for beginners and avoid exposing unnecessary implementation details

from pymata4 import pymata4  # Import pymata4 AFTER the patch

_max_retries = 3
_retry_delay = 2  # seconds

for attempt in range(_max_retries):
    try:
        # Add a small delay before trying to connect, especially on first attempt
        # This gives the OS/driver time to fully release the port if it was held
        # or for the board to finish its power-up sequence.
        sleep(0.5 if attempt == 0 else _retry_delay)

        _board = pymata4.Pymata4()

        _enable_print()  # Re-enable print after successful connection
        _Style.info()  # Display your welcome info
        print(f"{_Style._COLOR_LIGHT_CYAN}[Pynnacle-Genesis]{_Style._RESET} Board connected successfully!")
        break  # Connection successful, break out of retry loop
    except serial.SerialException as e:  # Catch specific serial errors
        _enable_print()
        _Style.print_error_message(e)
        if attempt < _max_retries - 1:
            print(f"Retrying connection in {_retry_delay} seconds...")
            _suppress_print()  # Re-suppress for the next retry
        else:
            print("\nAll connection attempts failed. Please fix the issue and try again.")
            _cleanup_board_on_exit()  # Attempt cleanup even if connection failed
            sys.exit(1)  # Exit if all retries fail
    except Exception as e:  # Catch any other unexpected errors during initial connection
        _enable_print()
        _Style.print_error_message(e)
        _cleanup_board_on_exit()  # Attempt cleanup
        sys.exit(1)
    finally:
        _enable_print()  # Ensure print is always re-enabled after the connection block finishes

    if _board is None:  # This check is mostly for safety, should be caught by sys.exit(1)
        _Style.print_error_message()
        sys.exit(1)
# --- END: Board Management & Instantiation ---

# --- BEGIN:  CONSTANTS ---
# Delay in ms before performing a write operation
_DELAY_WRITE = 10

# Digital States
HIGH = 1
LOW = 0

# Modes
OUTPUT = 'O'
INPUT = 'I'
INPUT_PULLUP = 'IP'

# Maximum number of digital pins on the Pinnacle Genesis
_DIGITAL_PINS_COUNT = 14

# Analog Pins on Pinnacle Genesis.
A0 = 'A0'
A1 = 'A1'
A2 = 'A2'
A3 = 'A3'
A4 = 'A4'
A5 = 'A5'

# Digital Pins on Pinnacle Genesis.
D0 = RX = 0
D1 = TX = 1
D2 = 2
D3 = 3
D4 = 4
D5 = 5
D6 = 6
D7 = 7
D8 = 8
D9 = 9
D10 = 10
D11 = 11
D12 = 12
D13 = 13

# Notes and their corresponding frequencies
# reference: https://gist.github.com/mikeputnam/2820675?permalink_comment_id=3868452
NOTE_B0 = 31
NOTE_C1 = 33
NOTE_CS1 = 35
NOTE_D1 = 37
NOTE_DS1 = 39
NOTE_E1 = 41
NOTE_F1 = 44
NOTE_FS1 = 46
NOTE_G1 = 49
NOTE_GS1 = 52
NOTE_A1 = 55
NOTE_AS1 = 58
NOTE_B1 = 62
NOTE_C2 = 65
NOTE_CS2 = 69
NOTE_D2 = 73
NOTE_DS2 = 78
NOTE_E2 = 82
NOTE_F2 = 87
NOTE_FS2 = 93
NOTE_G2 = 98
NOTE_GS2 = 104
NOTE_A2 = 110
NOTE_AS2 = 117
NOTE_B2 = 123
NOTE_C3 = 131
NOTE_CS3 = 139
NOTE_D3 = 147
NOTE_DS3 = 156
NOTE_E3 = 165
NOTE_F3 = 175
NOTE_FS3 = 185
NOTE_G3 = 196
NOTE_GS3 = 208
NOTE_A3 = 220
NOTE_AS3 = 233
NOTE_B3 = 247
NOTE_C4 = 262
NOTE_CS4 = 277
NOTE_D4 = 294
NOTE_DS4 = 311
NOTE_E4 = 330
NOTE_F4 = 349
NOTE_FS4 = 370
NOTE_G4 = 392
NOTE_GS4 = 415
NOTE_A4 = 440
NOTE_AS4 = 466
NOTE_B4 = 494
NOTE_C5 = 523
NOTE_CS5 = 554
NOTE_D5 = 587
NOTE_DS5 = 622
NOTE_E5 = 659
NOTE_F5 = 698
NOTE_FS5 = 740
NOTE_G5 = 784
NOTE_GS5 = 831
NOTE_A5 = 880
NOTE_AS5 = 932
NOTE_B5 = 988
NOTE_C6 = 1047
NOTE_CS6 = 1109
NOTE_D6 = 1175
NOTE_DS6 = 1245
NOTE_E6 = 1319
NOTE_F6 = 1397
NOTE_FS6 = 1480
NOTE_G6 = 1568
NOTE_GS6 = 1661
NOTE_A6 = 1760
NOTE_AS6 = 1865
NOTE_B6 = 1976
NOTE_C7 = 2093
NOTE_CS7 = 2217
NOTE_D7 = 2349
NOTE_DS7 = 2489
NOTE_E7 = 2637
NOTE_F7 = 2794
NOTE_FS7 = 2960
NOTE_G7 = 3136
NOTE_GS7 = 3322
NOTE_A7 = 3520
NOTE_AS7 = 3729
NOTE_B7 = 3951
NOTE_C8 = 4186
NOTE_CS8 = 4435
NOTE_D8 = 4699
NOTE_DS8 = 4978
# --- END:  CONSTANTS ---

# --- BEGIN: HELPER FUNCTIONS FOR PUBLIC FUNCTIONS ---
# This function accepts a pin as a parameter.
# This function converts the analog pin to its digital pin equivalent.
# It returns the calculated digital pin equivalent.
def _analogToDigital(pin):
    integer_only = int(pin[1:])
    pin = _DIGITAL_PINS_COUNT + integer_only
    return pin
# --- END: HELPER FUNCTIONS FOR PUBLIC FUNCTIONS ---


# --- BEGIN: PUBLIC FUNCTIONS ---
# This function sets the pin mode of a given pin.
# This function takes in 2 parameters:
#   1. pin
#   2. mode (INPUT, OUTPUT, or INPUT_PULLUP)
def pinMode(pin, mode):
    try:
        # Check if pin is an integer only. If so, it must be a digital pin.
        if re.match(r'^\d+$', str(pin)):
            if mode == INPUT:
                _board.set_pin_mode_digital_input(pin)
                _digital_input_pins.add(pin)
                _ultrasonic_trigger_pins.discard(pin)
            elif mode == OUTPUT:
                _board.set_pin_mode_digital_output(pin)
                _digital_input_pins.discard(pin)
                _ultrasonic_trigger_pins.discard(pin)
            elif mode == INPUT_PULLUP:
                _board.set_pin_mode_digital_input_pullup(pin)
                _digital_input_pins.add(pin)
                _ultrasonic_trigger_pins.discard(pin)
            else:
                raise Exception('Not a valid pin mode.')

        # Else if pin starts with an 'A', then it must be an analog pin.
        # Analog pins are usually used for analog inputs, but they can also be used as digital pins for input and output devices.
        elif pin.startswith('A'):
            integer_only = int(pin[1:])
            if mode == INPUT:
                _board.set_pin_mode_analog_input(integer_only)
                _analog_input_pins.add(integer_only)

            else:
                digital_pin_equivalent = _analogToDigital(pin)
                if mode == OUTPUT:
                    _board.set_pin_mode_digital_output(digital_pin_equivalent)
                    _digital_input_pins.discard(digital_pin_equivalent)
                    _ultrasonic_trigger_pins.discard(digital_pin_equivalent)

                elif mode == INPUT_PULLUP:
                    _board.set_pin_mode_digital_input_pullup(digital_pin_equivalent)
                    _digital_input_pins.add(digital_pin_equivalent)
                    _ultrasonic_trigger_pins.discard(digital_pin_equivalent)


                else:
                    raise Exception('Not a valid pin mode.')
        else:
            raise Exception('Wrong parameter in pinMode().')
    except Exception as err:
        _Style.print_function_error('pinMode()', err)


# This simulates the delay function used in coding some of the popular development boards.
# This function takes a delay time in milliseconds.
# It is implemented here using the sleep method.
def delay(ms):
    try:
        sleep(ms / 1000)  # The sleep method takes a delay time in seconds so we divide by 1000.
    except Exception as err:
        _Style.print_function_error('delay()', err)


# This function sets (writes) a digital pin's state into HIGH or LOW.
# This function takes in 2 parameters:
#   1. pin
#   2. state (HIGH or LOW)
def digitalWrite(pin, state):
    try:
        delay(_DELAY_WRITE)
        if isinstance(pin, str) and pin.startswith('A'):
            pin = _analogToDigital(pin)  # convert analog pin to digital pin equivalent
        _board.digital_write(pin, state)
    except Exception as err:
        _Style.print_function_error('digitalWrite()', err)


# This function allows users to write PWM wave (analog value) to a pin.
# This function takes in 2 parameters:
#   1. pin
#   2. val (ranges from 0-255)
# In some popular development boards, the analogWrite() function does not require the programmer to
# invoke pinMode() in order to set the pin as OUTPUT. We simulate this effect for the Pinnacle Genesis board
# using the set_pin_mode_pwm_output method before calling pwm_write.
def analogWrite(pin, val):
    try:
        delay(_DELAY_WRITE)
        if isinstance(pin, str) and pin.startswith('A'):
            pin = _analogToDigital(pin)  # convert analog pin to digital pin equivalent
        _board.set_pin_mode_pwm_output(pin)  # set the pin's mode as a pwm output pin
        _board.pwm_write(pin, val)  # write an output value
    except Exception as err:
        _Style.print_function_error('analogWrite()', err)


# This function accepts a pin as a parameter.
# This function allows to read a digital pin's state whether HIGH or LOW.
# This returns the last digital value change.
def digitalRead(pin):
    try:
        if isinstance(pin, str) and pin.startswith('A'):
            pin = _analogToDigital(pin)  # convert analog pin to digital pin equivalent
            _board.set_pin_mode_digital_input(pin)  # set the pin's mode as a digital input pin
            _digital_input_pins.add(pin)
            _ultrasonic_trigger_pins.discard(pin)
        val = _board.digital_read(pin)[0]  # store the digital reading
        return val
    except Exception as err:
        _Style.print_function_error('digitalRead()', err)


# This function accepts a pin as a parameter.
# This function allows to read the value from an analog pin.
# This returns the last analog value change.
def analogRead(pin):
    try:
        if isinstance(pin, str) and pin.startswith('A'):
            pin = int(pin[1:])
        val = _board.analog_read(pin)[0]  # store the analog reading
        return val
    except Exception as err:
        _Style.print_function_error('analogRead()', err)


# This initializes the pins that will be used by an ultrasonic sensor (HC-SR04 type).
# This accepts 2 parameters:
#   1. trigger_pin
#   2. echo_pin
# This function may not be commonly used in some popular development boards.
# It is added here for educational purposes in line with the authors' book.
def ultrasonicAttach(trigger_pin, echo_pin):
    try:
        _board.set_pin_mode_sonar(trigger_pin, echo_pin)
        _ultrasonic_trigger_pins.add(trigger_pin)
        _digital_input_pins.discard(trigger_pin)
    except Exception as err:
        _Style.print_function_error('ultrasonicAttach()', err)


# This function accepts a trigger_pin as a parameter.
# This function retrieves ping data from the ultrasonic (HC-SR04 type).
# This returns the last read value.
# This function may not be commonly used in some popular development boards.
# It is added here for educational purposes in line with the authors' book.
def ultrasonicRead(trigger_pin):
    try:
        val = _board.sonar_read(trigger_pin)[0]  # store the ultrasonic sensor's reading
        return val
    except Exception as err:
        _Style.print_function_error('ultrasonicRead()', err)


# That pin will then be set for servo operations.
# This accepts 3 parameters:
#   1. pin of the servo
#   2. min pulse width in ms. (if no value was passed, value is 544)
#   3. max pulse width in ms. (if no value was passed, value is 2400)
def servoAttach(pin, min_pulse=544, max_pulse=2400):
    try:
        _board.set_pin_mode_servo(pin)
    except Exception as err:
        _Style.print_function_error('servoAttach()', err)


# This function controls the shaft of the servo according to the position parameter.
# This accepts 2 parameters:
#   1. pin of the buzzer
#   2. frequency
def servoWrite(pin, position):
    try:
        delay(_DELAY_WRITE)
        _board.servo_write(pin, int(position))
    except Exception as err:
        _Style.print_function_error('servoWrite()', err)


# This function accepts a pin as a parameter.
# That pin will then be set for tone operations.
# This function may not be commonly used in some popular development boards.
# It is added here for educational purposes in line with the authors' book.
def buzzerAttach(pin):
    try:
        _board.set_pin_mode_tone(pin)
    except Exception as err:
        _Style.print_function_error('buzzerAttach()', err)


# This function plays a sound based on the frequency passed as a parameter.
# This accepts 2 parameters:
#   1. pin of the buzzer
#   2. frequency
def play(pin, frequency):
    try:
        delay(_DELAY_WRITE)
        _board.play_tone_continuously(pin, frequency)
    except Exception as err:
        _Style.print_function_error('play()', err)


# This function accepts a pin as a parameter.
# This function turns off the tone being played on the pin that was passed as a parameter.
def stop(pin):
    try:
        delay(_DELAY_WRITE)
        _board.play_tone_off(pin)
    except Exception as err:
        _Style.print_function_error('stop()', err)


# This function is for mapping a range of values to target range.
# Example: Mapping potentiometer inputs to the standard servo's range (0-180).
# This accepts 5 parameters:
#   1. input value
#   2. minimum possible input value
#   3. maximum possible input value
#   4. minimum output value of the target range
#   5. maximum output value of the target range
def mapValues(value_input, min_input, max_input, min_output, max_output):
    try:
        # Normalize the input value
        normalized_value = (value_input - min_input) / (max_input - min_input)

        # Scale to the output range
        mapped_value = normalized_value * (max_output - min_output) + min_output

        return int(mapped_value)
    except Exception as err:
        _Style.print_function_error('mapValues()', err)
# --- END: PUBLIC FUNCTIONS ---