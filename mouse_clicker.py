import pynput.mouse
from pynput import mouse
import time
import pyautogui


def start() :
    controller = mouse.Controller()
    # time.sleep(2)
    # location = controller.position
    # print(f"Location {location[0]}, {location[1]}")
    # controller.move( 100, 20, )
    # location = controller.position
    # print(f"Location {location[0]}, {location[1]}")
    # time.sleep(2)
    # controller.move( 10, 200, )
    # location = controller.position
    # print(f"Location {location[0]}, {location[1]}")
    # time.sleep(2)
    # controller.move( 150, 60, )
    # location = controller.position
    # print(f"Location {location[0]}, {location[1]}")

    while 1:
        time.sleep(2)
        # Battle Button
        pyautogui.click(1717, 874)

        time.sleep(2)
        # Level Button
        pyautogui.click(1717, 874)

        time.sleep(2)
        # Next button
        pyautogui.click(1766, 719)


if __name__ == "__main__":
    start()


# battle button
# 1717, 874

# Level button
# 1717, 874

# Next button
# 1766, 719
