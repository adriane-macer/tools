import pyautogui
import win32api, win32con
import time
from pynput import mouse

# start
# [(42, 667),(121, 661),(241, 667),(342, 661)]

# tiles
# [(42, 396),(121, 396),(241, 396),(342, 396)]

# region (0, 354, 440, 270)
start_coordinates = [(42, 667), (121, 661), (241, 667), (342, 661)]
tiles_coordinates = [(42, 500), (130, 500), (256, 500), (350, 500)]
# tiles_coordinates = [(42, 1), (136, 1), (256, 1), (356, 1)]  # offset values
tiles_coordinates_2 = [(50, 505), (146, 505), (266, 505), (353, 505)]
# tiles_coordinates_2 = [(50, 1), (146, 1), (266, 1), (366, 1)]  # offset values
tiles_coordinates_3 = [(55, 510), (140, 510), (260, 510), (354, 510)]
pyautogui.PAUSE = 0


def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.4)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    # time.sleep(0.00001)
    # pyautogui.click(205, 552)
    # time.sleep(0.00001)


start_tile = input("Position of start:\n")
if str(start_tile) == "1":
    click(start_coordinates[0][0], start_coordinates[0][1])
if str(start_tile) == "2":
    click(start_coordinates[1][0], start_coordinates[1][1])
if str(start_tile) == "3":
    click(start_coordinates[2][0], start_coordinates[2][1])
if str(start_tile) == "4":
    click(start_coordinates[3][0], start_coordinates[3][1])

controller = mouse.Controller()
counter = 0

while True:
    px = pyautogui.screenshot(region=(0, 500, 440, 6))
    color = px.getpixel((tiles_coordinates[0][0], 0))
    # color = px.getpixel((tiles_coordinates[0][0], tiles_coordinates[0][1]))
    color_2 = px.getpixel((tiles_coordinates_2[0][0], 0))
    # color_2 = px.getpixel((tiles_coordinates_2[0][0], tiles_coordinates_2[0][1]))
    # color_3 = px.getpixel((tiles_coordinates_3[0][0], 0))
    if (color[0] < 16 and color[1] < 16 and color[2] < 16) or (color_2[0] < 16 and color_2[1] < 16 and color_2[2] < 16):
        # if color[0] < 16 and color[1] < 16 and color[2] < 16:
        click(tiles_coordinates[0][0], tiles_coordinates[0][1] + 10)

    color = px.getpixel((tiles_coordinates[1][0], 0))
    # color = px.getpixel((tiles_coordinates[1][0], tiles_coordinates[1][1]))
    color_2 = px.getpixel((tiles_coordinates_2[1][0], 0))
    # color_2 = px.getpixel((tiles_coordinates_2[1][0], tiles_coordinates_2[1][1]))
    # color_3 = px.getpixel((tiles_coordinates_3[1][0], 0))
    if (color[0] < 16 and color[1] < 16 and color[2] < 16) or (color_2[0] < 16 and color_2[1] < 16 and color_2[2] < 16):
        # if color[0] < 16 and color[1] < 16 and color[2] < 16:
        click(tiles_coordinates[1][0], tiles_coordinates[1][1] + 10)

    color = px.getpixel((tiles_coordinates[2][0], 0))
    # color = px.getpixel((tiles_coordinates[2][0], tiles_coordinates[2][1]))
    color_2 = px.getpixel((tiles_coordinates_2[2][0], 0))
    # color_2 = px.getpixel((tiles_coordinates_2[2][0], tiles_coordinates_2[2][1]))
    # color_3 = px.getpixel((tiles_coordinates_3[2][0], 0))
    if (color[0] < 16 and color[1] < 16 and color[2] < 16) or (color_2[0] < 16 and color_2[1] < 16 and color_2[2] < 16):
        # if color[0] < 16 and color[1] < 16 and color[2] < 16:
        click(tiles_coordinates[2][0], tiles_coordinates[2][1] + 10)

    color = px.getpixel((tiles_coordinates[3][0], 0))
    # color = px.getpixel((tiles_coordinates[3][0], tiles_coordinates[3][1]))
    color_2 = px.getpixel((tiles_coordinates_2[3][0], 0))
    # color_2 = px.getpixel((tiles_coordinates_2[3][0], tiles_coordinates_2[3][1]))
    # color_3 = px.getpixel((tiles_coordinates_3[3][0], 0))
    if (color[0] < 16 and color[1] < 16 and color[2] < 16) or (color_2[0] < 16 and color_2[1] < 16 and color_2[2] < 16):
        # if color[0] < 16 and color[1] < 16 and color[2] < 16:
        click(tiles_coordinates[3][0], tiles_coordinates[3][1] + 3)

    counter = counter + 1
    if counter % 10 == 0:
        location = controller.position
        if location[0] > 400:
            break
