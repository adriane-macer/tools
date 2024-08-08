import pyautogui
import win32api, win32con
import time
from pynput import mouse

# start
# [(42, 667),(121, 661),(241, 667),(342, 661)]

# tiles
# [(42, 396),(121, 396),(241, 396),(342, 396)]

start_coordinates = [(42, 667), (121, 661), (241, 667), (342, 661)]
tiles_coordinates = [(42, 500), (136, 500), (256, 500), (356, 500)]
tiles_coordinates_2 = [(50, 500), (146, 500), (266, 500), (366, 500)]
pyautogui.PAUSE = 0


def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.001)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


click(start_coordinates[0][0], start_coordinates[0][1])
click(start_coordinates[1][0], start_coordinates[1][1])
click(start_coordinates[2][0], start_coordinates[2][1])
click(start_coordinates[3][0], start_coordinates[3][1])

controller = mouse.Controller()
counter = 0

while True:
    px = pyautogui.screenshot()
    color = px.getpixel((tiles_coordinates[0][0], tiles_coordinates[0][1]))
    color_2 = px.getpixel((tiles_coordinates_2[0][0], tiles_coordinates_2[0][1]))
    if color[0] < 4 and color[1] < 4 and color[2] < 4 and color_2[0] < 4 and color_2[1] < 4 and color_2[2] < 4:
        click(tiles_coordinates[0][0], tiles_coordinates[0][1])
    color = px.getpixel((tiles_coordinates[1][0], tiles_coordinates[1][1]))
    color_2 = px.getpixel((tiles_coordinates_2[1][0], tiles_coordinates_2[1][1]))
    if color[0] < 4 and color[1] < 4 and color[2] < 4 and color_2[0] < 4 and color_2[1] < 4 and color_2[2] < 4:
        click(tiles_coordinates[1][0], tiles_coordinates[1][1])
    color = px.getpixel((tiles_coordinates[2][0], tiles_coordinates[2][1]))
    color_2 = px.getpixel((tiles_coordinates_2[2][0], tiles_coordinates_2[2][1]))
    if color[0] < 4 and color[1] < 4 and color[2] < 4 and color_2[0] < 4 and color_2[1] < 4 and color_2[2] < 4:
        click(tiles_coordinates[2][0], tiles_coordinates[2][1])
    color = px.getpixel((tiles_coordinates[3][0], tiles_coordinates[3][1]))
    color_2 = px.getpixel((tiles_coordinates_2[3][0], tiles_coordinates_2[3][1]))
    if color[0] < 4 and color[1] < 4 and color[2] < 4 and color_2[0] < 4 and color_2[1] < 4 and color_2[2] < 4:
        click(tiles_coordinates[3][0], tiles_coordinates[3][1])
    counter = counter + 1
    if counter % 10 == 0:
        location = controller.position
        if location[0] > 400:
            break
