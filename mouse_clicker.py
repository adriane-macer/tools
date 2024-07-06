import pynput.mouse
from pynput import mouse
import time
import pyautogui


def start_main_battle():
    controller = mouse.Controller()

    #  main battle
    while 1:
        time.sleep(2)

        # Battle Button
        if click(1717, 874, controller=controller):
            break

        time.sleep(2)
        # Level Button
        if click(1717, 874, controller=controller):
            break

        time.sleep(2)
        # Next button
        if click(1766, 719, controller=controller):
            break


def start_headhunt_winter():
    controller = mouse.Controller()

    # Head Hunt
    while 1:
        time.sleep(2)
        # ######################
        # Hard Button
        if click(1838, 820, controller=controller):
            break
        # ################################

        time.sleep(2)

        # Battle Button
        if click(1717, 874, controller=controller):
            break

        time.sleep(2)
        # Next button
        if click(1776, 660, controller=controller):
            break


def click(x: int, y: int, controller: mouse.Controller):
    if check_if_out_of_screen(controller=controller):
        return True

    pyautogui.click(x, y)
    return False


def start_headhunt_dessert():
    controller = mouse.Controller()

    # Head Hunt
    while 1:
        time.sleep(2)

        # ######################
        # Dessert Button
        if click(1823, 626, controller=controller):
            break
        ################################

        time.sleep(2)
        # Battle Button
        if click(1717, 874, controller=controller):
            break

        time.sleep(2)
        # Next button
        if click(1776, 660, controller=controller):
            break


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
