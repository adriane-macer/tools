# liker for just specific plant
from pynput.mouse import Controller
import time
# import threading
# import os
import pyautogui

import cv2


# import random


def get_location(filename, grayscale=False, confidence=0.9):
    try:
        # found_image = has_image(filename, 0, 300, 444, 600)
        # if not found_image:
        #     return None, None
        c = pyautogui.locateCenterOnScreen(filename, grayscale=grayscale, confidence=confidence,
                                        # region=(-1920,556, -1600, 300)
                                        region=(0, 556, 444, 300)
                                        # region=(11, 556, 200, 300)
                                        # region=(11, 556, 400, 500)
                                        )
        # x, y = pyautogui.locateOnScreen(filename, grayscale=grayscale, confidence=confidence,
        #                                 region=(0, 556, 444, 300))
        # pyautogui.screenshot(region=(11, 556, 300, 600))
        return c.x, c.y
    except Exception as e:
        print(e)
        return None, None


def get_tile_location():
    list = [
        # "piano_tiles_images/black_tile.png",
        # "piano_tiles_images/black_tile_2.png",
        # "piano_tiles_images/black_tile_3.png",
        "piano_tiles_images/black_tile_4.png",
        # "piano_tiles_images/start_tile.png",
        "piano_tiles_images/start_tile_2.png"
    ]

    for f in list:
        x, y = get_location(f, grayscale=True)
        if x is not None:
            return x, y

    return None, None


def has_image(image_filename, x, y, w, h):
    template = cv2.imread(image_filename)
    template_gray = cv2.cvtColor(template, cv2.COLOR_RGB2GRAY)
    template_w, template_h = template_gray.shape[::-1]

    pyautogui.screenshot("tmp/ss.png", (x, y, w, h))

    img = cv2.imread("tmp/ss.png")

    image_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(
        image=image_gray,
        templ=template_gray,
        method=cv2.TM_CCOEFF_NORMED
    )

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    found = max_val >= 0.8

    #         print("{} found {}".format(image_filename, found))
    return found


def click_position(posX, posY):
    pyautogui.click(posX, posY)


class ClickMouse:

    # delay and button is passed in class
    # to check execution of auto-clicker
    def __init__(self):
        super(ClickMouse, self).__init__()
        self.mouse = Controller()

    def start_click(self):

        print("=== STARTED CLICKER ===")

        pos_x_check_count = 0
        number_of_no_tile_check = 0
        while 1:
            tile_x, tile_y = get_tile_location()
            if tile_x is None:
                number_of_no_tile_check = number_of_no_tile_check + 1
                if number_of_no_tile_check >= 30:
                    print("exited due to no tile detected")
                    break
                continue

            print(f"tile coordinate: {tile_x},{tile_y}")
            click_position(tile_x, tile_y)
            number_of_no_tile_check = 0
            time.sleep(0.03)
            pos_x_check_count = pos_x_check_count + 1
            if pos_x_check_count % 10 == 0:
                location = self.mouse.position
                # print(f"location[0] {location[0]}")
                if location[0] > 400:
                    break

    #   region=(-1920,556, -1600, 300)
    #                                 region=(-960,556, 400, 300)
    #                                 # region=(11, 556, 200, 300)
    #                                 # region=(11, 556, 400, 500)


if __name__ == "__main__":
    time.sleep(5)
    # pyautogui.screenshot("tmp/ss.png", (0, 556, 444, 300))

    #
    # m = Controller()
    #
    # location = m.position
    # print(f"{location[0], location[1]}")
    # m.move(47,622)
    # print("moved")
    clicker = ClickMouse()
    clicker.start_click()
    print("=== DONE ===")

# (11, 556)
# (455, 548)
# (458, 773) 450 240
# (1919, 503) 1920,
# (1910, 1076)
