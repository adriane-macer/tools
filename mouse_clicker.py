import pynput.mouse
from pynput import mouse
import time
import pyautogui


def start():
    controller = mouse.Controller()
    # time.sleep(2)
    # location = controller.position
    # print(f"Location {location[0]}, {location[1]}")

    #  main battle
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

    # Head Hunt
    # while 1:
    #     time.sleep(2)
    #     # ######################
    #     # Hard Button
    #     # pyautogui.click(1838, 820)
    #     # ################################
    #
    #     # ######################
    #     # Dessert Button
    #     pyautogui.click(1823, 626)
    #     # ################################
    #
    #     time.sleep(2)
    #     # Battle Button
    #     pyautogui.click(1717, 874)
    #
    #     time.sleep(2)
    #     # Next button
    #     pyautogui.click(1776, 660)


if __name__ == "__main__":
    start()

# battle button
# 1717, 874

# Level button
# 1717, 874

# Next button
# 1766, 719


# Head Hunt hard attack button
# 1838, 820

# Head Hunt dessert attack button
# 1823, 626

# Fight button
# 1717, 874
