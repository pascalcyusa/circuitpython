import board
import pwmio
import rotaryio
import digitalio
from adafruit_motor import stepper
import random
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

# Rotary encoder button setup
encoder_button = digitalio.DigitalInOut(board.A3)
encoder_button.direction = digitalio.Direction.INPUT
encoder_button.pull = digitalio.Pull.UP  # Enable internal pull-up resistor

# DC motor setup
dc_motor_forward = pwmio.PWMOut(board.D8, frequency=2000)
dc_motor_backward = pwmio.PWMOut(board.D9, frequency=2000)

# LED setup using PWM for smooth transitions
green_led = pwmio.PWMOut(board.A0, frequency=1000, duty_cycle=0)  # Green LED
red_led = pwmio.PWMOut(board.A1, frequency=1000, duty_cycle=0)    # Red LED

# Button setup using analog pin as digital GPIO
goal_button = digitalio.DigitalInOut(board.A2)  # Goal button
goal_button.direction = digitalio.Direction.INPUT
goal_button.pull = digitalio.Pull.UP  # Enable internal pull-up resistor

# Variables to track encoder position
last_position = 0

# State machine states
IDLE = 0
PLAYING = 1
GOAL = 2
state = IDLE

# Function for smooth LED fading


def smooth_led_transition(led, start, end, steps=50, delay=0.01):
    step_size = (end - start) / steps
    for i in range(steps):
        led.duty_cycle = int(start + step_size * i)
        time.sleep(delay)


try:
    while True:
        # State: IDLE
        if state == IDLE:
            smooth_led_transition(
                red_led, red_led.duty_cycle, 0)  # Turn off red LED
            # Turn off green LED
            smooth_led_transition(green_led, green_led.duty_cycle, 0)
            print("Game is idle. Press encoder button to start...")

            # Wait for encoder button press to start the game
            if not encoder_button.value:  # Button pressed (active low)
                print("Game starting!")
                state = PLAYING

        # State: PLAYING
        elif state == PLAYING:
            smooth_led_transition(
                red_led, red_led.duty_cycle, 65535)  # Brighten red LED
            # Turn off green LED
            smooth_led_transition(green_led, green_led.duty_cycle, 0)

            # Randomly move the DC motor to confuse the player
            direction = random.choice(["forward", "backward"])
            if direction == "forward":
                dc_motor_forward.duty_cycle = 65535  # Full speed forward
                dc_motor_backward.duty_cycle = 0
            else:
                dc_motor_forward.duty_cycle = 0
                dc_motor_backward.duty_cycle = 65535  # Full speed backward

            time.sleep(0.5)  # Change direction every 0.5 seconds

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
            smooth_led_transition(
                red_led, red_led.duty_cycle, 0)  # Turn off red LED
            # Brighten green LED
            smooth_led_transition(green_led, green_led.duty_cycle, 65535)
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
    red_led.duty_cycle = 0
    green_led.duty_cycle = 0
    print("Game stopped.")
