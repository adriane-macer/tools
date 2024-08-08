import pynput.mouse
from pynput import mouse
import time
import pyautogui
from datetime import datetime
import random


def start_main():
    controller = mouse.Controller()
    location = controller.position
    print(f"{location[0], location[1]}")
    x = 0
    #  main battle
    while 1:
        # (1686, 619)
        # (1768, 601)
        # (1732, 640)
        # Battle Button

        # num = random.random()
        # x_or_y_offset = bool(random.getrandbits(1))
        # x_or_y_offset = False
        # x_offset = (num * 60) if x_or_y_offset else 0
        # y_offset = (num * 60) if not x_or_y_offset else 0
        # pyautogui.click(1686 + x_offset, 461 + y_offset)
        pyautogui.click(205, 552)
        # pyautogui.click(249, 552)
        # num = random.random()
        # x_or_y_offset = bool(random.getrandbits(1))
        # x_offset = (num * 4) if x_or_y_offset else 0
        # y_offset = (num * 4) if not x_or_y_offset else 0
        # pyautogui.click(1768 + x_offset, 478 + y_offset)
        # pyautogui.click(1732, 640)
        # cycle_date_time = datetime.now()
        # cycle_time = cycle_date_time.strftime("%H:%M:%S")
        # print(cycle_time)
        time.sleep(0.005)
        x = x + 1
        if x % 10 == 0:
            location = controller.position
            # print(f"location[0] {location[0]}")
            if location[0] > 400:
                return


def click(x: int, y: int, controller: mouse.Controller):
    if check_if_out_of_screen(controller=controller):
        return True
    # return True
    pyautogui.click(x, y)
    return False


def check_if_out_of_screen(controller: mouse.Controller):
    location = controller.position
    # print(f"location[0] {location[0]}")
    return location[0] < 1500


if __name__ == "__main__":
    print("Select the type of game:")
    print("1 - Main click")
    game_type = input("")

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("started time:", current_time)

    if game_type == "1":
        start_main()
    else:
        print("Input not valid")

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("ended time:", current_time)

# (1686, 619)
# (1768, 601)
# (1732, 640)
