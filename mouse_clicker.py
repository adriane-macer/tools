import pynput.mouse
from pynput import mouse
import time
import pyautogui


def start_main_battle():
    controller = mouse.Controller()

    #  main battle
    while 1:
        time.sleep(2)
        is_out_of_the_screen = check_if_out_of_screen(controller)
        if is_out_of_the_screen:
            break

        # Battle Button
        pyautogui.click(1717, 874)

        time.sleep(2)
        is_out_of_the_screen = check_if_out_of_screen(controller)
        if is_out_of_the_screen:
            break
        # Level Button
        pyautogui.click(1717, 874)

        time.sleep(2)
        is_out_of_the_screen = check_if_out_of_screen(controller)
        if is_out_of_the_screen:
            break
        # Next button
        pyautogui.click(1766, 719)


def start_headhunt_winter():
    controller = mouse.Controller()

    # Head Hunt
    while 1:
        time.sleep(2)
        is_out_of_the_screen = check_if_out_of_screen(controller)
        if is_out_of_the_screen:
            break
        # ######################
        # Hard Button
        pyautogui.click(1838, 820)
        # ################################

        time.sleep(2)
        is_out_of_the_screen = check_if_out_of_screen(controller)
        if is_out_of_the_screen:
            break
        # Battle Button
        pyautogui.click(1717, 874)

        time.sleep(2)
        is_out_of_the_screen = check_if_out_of_screen(controller)
        if is_out_of_the_screen:
            break
        # Next button
        pyautogui.click(1776, 660)


def start_headhunt_dessert():
    controller = mouse.Controller()

    # Head Hunt
    while 1:
        time.sleep(2)
        is_out_of_the_screen = check_if_out_of_screen(controller)
        if is_out_of_the_screen:
            break

        # ######################
        # Dessert Button
        pyautogui.click(1823, 626)
        ################################

        time.sleep(2)
        is_out_of_the_screen = check_if_out_of_screen(controller)
        if is_out_of_the_screen:
            break
        # Battle Button
        pyautogui.click(1717, 874)

        time.sleep(2)
        is_out_of_the_screen = check_if_out_of_screen(controller)
        if is_out_of_the_screen:
            break
        # Next button
        pyautogui.click(1776, 660)


def check_if_out_of_screen(controller: mouse.Controller):
    location = controller.position
    print(f"location[0] {location[0]}")
    return location[0] < 1500


if __name__ == "__main__":
    print("Select the type of game:")
    print("1 - Main Battle")
    print("2 - Headhunt Winter")
    print("3 - Headhunt Dessert")
    game_type = input("")
    if game_type == "1":
        start_main_battle()
    elif game_type == "2":
        start_headhunt_winter()
    elif game_type == "3":
        start_headhunt_dessert()
    else:
        print("Input not valid")
