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

# Define button pin (using an external pull-up resistor)
button = digitalio.DigitalInOut(board.A3)
button.direction = digitalio.Direction.INPUT

# Define green LED pin
green_led = digitalio.DigitalInOut(board.A0)
green_led.direction = digitalio.Direction.OUTPUT

# Define DC motor pins
dc_motor_pin1 = pwmio.PWMOut(board.D8, frequency=5000, duty_cycle=0)
dc_motor_pin2 = pwmio.PWMOut(board.D9, frequency=5000, duty_cycle=0)

# Define states
INIT = 0
RUN_DC_MOTOR = 1
RUN_STEPPER_MOTOR = 2
GOAL_SCORED = 3

# Initial state
state = INIT


def control_dc_motor():
    # Move DC motor clockwise and counter-clockwise with reduced distance
    dc_motor_pin1.duty_cycle = 0
    dc_motor_pin2.duty_cycle = 16384  # Quarter duty cycle for counter-clockwise
    time.sleep(0.25)
    dc_motor_pin1.duty_cycle = 16384  # Quarter duty cycle for clockwise
    dc_motor_pin2.duty_cycle = 0
    time.sleep(0.25)
    dc_motor_pin1.duty_cycle = 0
    dc_motor_pin2.duty_cycle = 0


def run_stepper_motor(stepper_motor, encoder, button, green_led, game_duration):
    last_position = encoder.position
    start_time = time.time()

    while time.time() - start_time < game_duration:
        position = encoder.position

        # Check if the encoder position has changed
        if position != last_position:
            if position > last_position:
                # Move stepper motor forward
                stepper_motor.onestep(
                    direction=stepper.FORWARD, style=stepper.SINGLE
                )
                print(f"Stepper motor moved forward to position {position}")
            elif position < last_position:
                # Move stepper motor backward
                stepper_motor.onestep(
                    direction=stepper.BACKWARD, style=stepper.SINGLE
                )
                print(f"Stepper motor moved backward to position {position}")

            # Update the last position
            last_position = position

        # Check if the button state has changed
        if not button.value:  # Button is pressed when value is False
            print("Goal scored!")
            green_led.value = True  # Turn on the green LED
            return GOAL_SCORED

        time.sleep(0.01)  # Small delay to prevent high CPU usage

    print("Game session ended")
    return INIT


try:
    game_duration = 1
    while True:
        if state == INIT:
            green_led.value = False  # Turn off the green LED for a new game session
            state = RUN_DC_MOTOR

        elif state == RUN_DC_MOTOR:
            control_dc_motor()
            state = RUN_STEPPER_MOTOR

        elif state == RUN_STEPPER_MOTOR:
            state = run_stepper_motor(
                stepper_motor, encoder, button, green_led, game_duration)

        elif state == GOAL_SCORED:
            # Wait for a short period before starting a new game session
            time.sleep(2)
            state = INIT

except KeyboardInterrupt:
    print("Program interrupted")
