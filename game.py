import board
import pwmio
import rotaryio
import digitalio
from adafruit_motor import stepper
import time

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

# DC motor setup
dc_motor_forward = pwmio.PWMOut(board.D8, frequency=2000)
dc_motor_backward = pwmio.PWMOut(board.D9, frequency=2000)

# LED setup using PWM
green_led = pwmio.PWMOut(board.A0, frequency=1000, duty_cycle=0)  # Green LED

# Button setup using analog pin as digital GPIO
goal_button = digitalio.DigitalInOut(board.A3)  # Goal button
goal_button.direction = digitalio.Direction.INPUT
goal_button.pull = digitalio.Pull.UP  # Enable internal pull-up resistor

# Variables to track encoder position
last_position = 0

# State machine states
IDLE = 0
PLAYING = 1
GOAL = 2
state = IDLE

try:
    while True:
        # State: IDLE
        if state == IDLE:
            green_led.duty_cycle = 0  # Turn off green LED
            print("Game is idle. Press the goal button to start...")

            # Wait for goal button press to start the game
            if not goal_button.value:  # Button pressed (active low)
                print("Game starting!")
                state = PLAYING

        # State: PLAYING
        elif state == PLAYING:
            green_led.duty_cycle = 0    # Turn off green LED

            # Move DC motor left (backward)
            dc_motor_forward.duty_cycle = 0
            dc_motor_backward.duty_cycle = 65535  # Full speed backward
            print("DC motor moving left...")
            time.sleep(1)  # Wait for 1 second

            # Move DC motor right (forward)
            dc_motor_forward.duty_cycle = 65535  # Full speed forward
            dc_motor_backward.duty_cycle = 0
            print("DC motor moving right...")
            time.sleep(1)  # Wait for 1 second

            # Check for goal button press
            if not goal_button.value:  # Button pressed (active low)
                print("Goal detected!")
                state = GOAL

            # Control the stepper motor based on encoder position
            position = encoder.position
            if position > last_position:
                motor.onestep(direction=stepper.FORWARD, style=stepper.SINGLE)
            elif position < last_position:
                motor.onestep(direction=stepper.BACKWARD, style=stepper.SINGLE)
            last_position = position

        # State: GOAL
        elif state == GOAL:
            green_led.duty_cycle = 65535  # Brighten green LED
            print("Goal scored! Green LED is ON.")

            # Stop the DC motor temporarily
            dc_motor_forward.duty_cycle = 0
            dc_motor_backward.duty_cycle = 0

            time.sleep(2)  # Keep the green LED on for 2 seconds

            # Transition back to PLAYING state
            state = PLAYING

except KeyboardInterrupt:
    # Release resources when script is interrupted
    motor.release()
    dc_motor_forward.deinit()
    dc_motor_backward.deinit()
    green_led.duty_cycle = 0
    print("Game stopped.")
