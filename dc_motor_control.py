# to control the DC motor

import board  # necessary imports
import digitalio  # in order to use digital pins
import time  # so u can do time.sleep and such

# Initialize the control pins
motor_a = digitalio.DigitalInOut(board.D8)
motor_b = digitalio.DigitalInOut(board.D9)
# Starts up the pins so you can control the direction of the motor-
motor_a.direction = digitalio.Direction.OUTPUT
# -not necessary to change but is important to have
motor_b.direction = digitalio.Direction.OUTPUT


def stop():  # a stop function which you should always have, NEVER SET BOTH TO TRUE, YOULL FRY THE H-BRIDGE
    motor_a.value = False  # sets motor to low or 0
    motor_b.value = False  # sets motor to low or 0


def forward():  # a forward, you can see the direction of the motor and decide your forward and back
    motor_a.value = True  # sets motor to high or 1
    motor_b.value = False  # sets motor to low or 0


def reverse():  # you can even change it to clockwise or counterclockwise
    motor_a.value = False  # sets motor to low or
    motor_b.value = True  # sets motor to low


while True:  # Main control loop
    # Forward
    print("Forward")  # tells you which direction it goes to
    forward()  # calls the forward function
    time.sleep(3)  # sleeps for 3 secs

    # Stop
    print("Stop")  # tells you which direction it goes to
    stop()  # calls the stop function
    time.sleep(1)  # sleeps for 1 secs

    # Reverse
    print("Reverse")  # tells you which direction it goes to
    reverse()  # calls the reverse function
    time.sleep(3)  # sleeps for 3 secs

    # Stop
    print("Stop")  # tells you which direction it goes to
    stop()  # calls the stop function
    time.sleep(1)  # sleeps for 3 secs
