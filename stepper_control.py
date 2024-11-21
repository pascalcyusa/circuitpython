# to control the stepper motor

import board  # Necessary imports
import digitalio  # For using digital pins
import time  # To control the timing of steps

# Initialize the control pins for the stepper motor
motor_pin1 = digitalio.DigitalInOut(board.D2)  # Change to your specific pin
motor_pin2 = digitalio.DigitalInOut(board.D3)  # Change to your specific pin
motor_pin3 = digitalio.DigitalInOut(board.D4)  # Change to your specific pin
motor_pin4 = digitalio.DigitalInOut(board.D5)  # Change to your specific pin

# Set the direction of all pins to OUTPUT
motor_pin1.direction = digitalio.Direction.OUTPUT
motor_pin2.direction = digitalio.Direction.OUTPUT
motor_pin3.direction = digitalio.Direction.OUTPUT
motor_pin4.direction = digitalio.Direction.OUTPUT

# Define the step sequence for the stepper motor (Full Step Mode)
STEP_SEQUENCE = [
    (True, False, True, False),  # Step 1
    (False, True, True, False),  # Step 2
    (False, True, False, True),  # Step 3
    (True, False, False, True)   # Step 4
]

# Function to stop the motor


def stop():
    motor_pin1.value = False
    motor_pin2.value = False
    motor_pin3.value = False
    motor_pin4.value = False

# Function to step the motor forward


def step_forward(steps, delay=0.01):
    for _ in range(steps):
        for step in STEP_SEQUENCE:
            motor_pin1.value, motor_pin2.value, motor_pin3.value, motor_pin4.value = step
            time.sleep(delay)  # Adjust delay for step speed

# Function to step the motor backward


def step_backward(steps, delay=0.01):
    for _ in range(steps):
        # Reverse the sequence for backward motion
        for step in reversed(STEP_SEQUENCE):
            motor_pin1.value, motor_pin2.value, motor_pin3.value, motor_pin4.value = step
            time.sleep(delay)  # Adjust delay for step speed


# Main loop to demonstrate the stepper motor control
while True:
    # Step forward for 100 steps
    print("Stepping Forward")
    step_forward(steps=100, delay=0.01)  # 100 steps with 10ms delay per step

    # Pause
    print("Stopping")
    stop()
    time.sleep(1)

    # Step backward for 100 steps
    print("Stepping Backward")
    step_backward(steps=100, delay=0.01)  # 100 steps with 10ms delay per step

    # Pause
    print("Stopping")
    stop()
    time.sleep(1)
