# code to control a stepper motor using a rotary encoder

import board
import pwmio
import rotaryio
from adafruit_motor import stepper

# Define PWM pins for the stepper motor with at least 1500 Hz frequency
motor_pins = [
    pwmio.PWMOut(board.D2, frequency=2000),
    pwmio.PWMOut(board.D3, frequency=2000),
    pwmio.PWMOut(board.D4, frequency=2000),
    pwmio.PWMOut(board.D5, frequency=2000),
]

# Create stepper motor object
motor = stepper.StepperMotor(
    motor_pins[0], motor_pins[1], motor_pins[2], motor_pins[3]
)

# Create rotary encoder object
encoder = rotaryio.IncrementalEncoder(board.D6, board.D7)

# Variables to track encoder position
last_position = 0

try:
    while True:
        # Read the current position of the encoder
        position = encoder.position

        # Check if the encoder position has changed
        if position > last_position:
            # Move stepper motor forward
            motor.onestep(direction=stepper.FORWARD, style=stepper.SINGLE)
            print(f"Stepper motor moved forward to position {position}")
        elif position < last_position:
            # Move stepper motor backward
            motor.onestep(direction=stepper.BACKWARD, style=stepper.SINGLE)
            print(f"Stepper motor moved backward to position {position}")

        # Update the last position
        last_position = position

except KeyboardInterrupt:
    # Release the motor when the script is interrupted
    motor.release()
    print("Stepper motor released.")
