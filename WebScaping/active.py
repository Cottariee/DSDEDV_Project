import pyautogui
import math
import time

# Set the center and radius for the circular movement
center_x, center_y = pyautogui.size()[0] // 2, pyautogui.size()[1] // 2  # screen center
radius = 200  # radius of the circle
speed = 0.01  # time delay between movements (controls the speed)

# Function to move the cursor in a circular pattern
def move_cursor_in_circle():
    angle = 0  # starting angle
    while True:
        # Calculate x, y coordinates for the circle
        x = center_x + radius * math.cos(math.radians(angle))
        y = center_y + radius * math.sin(math.radians(angle))

        # Move the cursor to the calculated position
        pyautogui.moveTo(x, y)

        # Increase the angle to move in a circular path
        angle += 5  # adjust the increment for a smoother or faster circle

        # Loop the angle
        if angle >= 360:
            angle = 0

        # Control the speed of the movement
        time.sleep(speed)

# Start the circular movement
move_cursor_in_circle()
