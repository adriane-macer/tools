import pynput.mouse
from pynput import mouse
import time
import pyautogui

controller = mouse.Controller()
time.sleep(2)
location = controller.position
print(f"{location[0], location[1]}")

# start
# [(42, 667),(121, 661),(241, 667),(342, 661)]

# tiles
# [(42, 396),(121, 396),(241, 396),(342, 396)]
