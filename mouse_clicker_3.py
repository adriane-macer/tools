import pynput.mouse
from pynput import mouse
import time
import pyautogui
from datetime import datetime
import random


def start_main():
    controller = mouse.Controller()
    # time.sleep(5)
    # location = controller.position
    # # print(f"{location[0], location[1]}")
    x = 0
    while 1:
        # get queue number
        pyautogui.click(273, 786)

        time.sleep(0.4)
        x = x + 1
        if x % 10 == 0:
            location = controller.position
            # print(f"location[0] {location[0]}")
            if location[0] > 280:
                return


def click(x: int, y: int, controller: mouse.Controller):
    pyautogui.click(x, y)
    return False


def check_if_out_of_screen(controller: mouse.Controller):
    location = controller.position
    # print(f"location[0] {location[0]}")
    return location[0] < 1500


if __name__ == "__main__":
    # print("Select the type of game:")
    # print("1 - Main click")
    # game_type = input("")
    #
    # now = datetime.now()
    # current_time = now.strftime("%H:%M:%S")
    # print("started time:", current_time)
    #
    # if game_type == "1":
    #     start_main()
    # else:
    #     print("Input not valid")

    # now = datetime.now()
    # current_time = now.strftime("%H:%M:%S")
    # print("ended time:", current_time)

    not_yet_time = True
    current_time = ""
    print("...===>")
    while not_yet_time:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        split_time = current_time.split(":")

        if int(split_time[0]) == 8:
            if int(split_time[1]) >= 0:
                not_yet_time = False
    print(f"start clicking: {current_time}")
    start_main()
    print("Done")
