import board
import pwmio
import rotaryio
import digitalio
import time
from adafruit_motor import stepper

# Define PWM pins for the stepper motor with at least 1500 Hz frequency
motor_pins = [
    pwmio.PWMOut(board.D2, frequency=2000),
    pwmio.PWMOut(board.D3, frequency=2000),
    pwmio.PWMOut(board.D4, frequency=2000),
    pwmio.PWMOut(board.D5, frequency=2000),
]

# Create stepper motor object
stepper_motor = stepper.StepperMotor(
    motor_pins[0], motor_pins[1], motor_pins[2], motor_pins[3]
)

# Create rotary encoder object
encoder = rotaryio.IncrementalEncoder(board.D6, board.D7)

# Variables to track encoder position
last_position = 0

# Define DC motor pins
dc_motor_pin1 = pwmio.PWMOut(board.D8, frequency=5000, duty_cycle=0)
dc_motor_pin2 = pwmio.PWMOut(board.D9, frequency=5000, duty_cycle=0)

# Define button pin
button = digitalio.DigitalInOut(board.A3)
button.direction = digitalio.Direction.INPUT

# Define green LED pin
green_led = digitalio.DigitalInOut(board.D10)
green_led.direction = digitalio.Direction.OUTPUT

# State machine states
IDLE = 0
GAME_PLAY = 1
GOAL_SCORED = 2

# Initial state
state = IDLE


def control_dc_motor():
    # Move DC motor clockwise and counter-clockwise
    dc_motor_pin1.duty_cycle = 0
    dc_motor_pin2.duty_cycle = 32767  # Half duty cycle for counter-clockwise
    time.sleep(0.5)
    dc_motor_pin1.duty_cycle = 32767  # Half duty cycle for clockwise
    dc_motor_pin2.duty_cycle = 0
    time.sleep(0.5)
    dc_motor_pin1.duty_cycle = 0
    dc_motor_pin2.duty_cycle = 0


try:
    while True:
        # Read the current position of the encoder
        position = encoder.position

        # Check if the encoder position has changed
        if position != last_position:
            if position > last_position:
                # Move stepper motor forward
                stepper_motor.onestep(
                    direction=stepper.FORWARD, style=stepper.SINGLE)
                print(f"Stepper motor moved forward to position {position}")
            elif position < last_position:
                # Move stepper motor backward
                stepper_motor.onestep(
                    direction=stepper.BACKWARD, style=stepper.SINGLE)
                print(f"Stepper motor moved backward to position {position}")

            # Update the last position
            last_position = position

        # State machine logic
        if state == IDLE:
            if not button.value:  # Button pressed
                state = GAME_PLAY
                green_led.value = False  # Turn off green LED
                print("Game started")

        elif state == GAME_PLAY:
            control_dc_motor()
            if not button.value:  # Button pressed
                state = GOAL_SCORED
                green_led.value = True  # Turn on green LED
                print("Goal scored!")

        elif state == GOAL_SCORED:
            if not button.value:  # Button pressed
                state = IDLE
                green_led.value = False  # Turn off green LED
                print("Game reset")

        # Small delay to debounce the button
        time.sleep(0.5)

except KeyboardInterrupt:
    # Release the motors when the script is interrupted
    stepper_motor.release()
    dc_motor_pin1.duty_cycle = 0
    dc_motor_pin2.duty_cycle = 0
    print("Motors released.")
