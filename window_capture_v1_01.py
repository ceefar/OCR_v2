# -- imports --
import cv2 as cv # for img manipulation, etc
import numpy as np # for array conversion 
import pyautogui # for interface automation
import os # for file handling
from PIL import ImageGrab # for grabbing images only at present
from time import perf_counter # for performance timing



# -- testing functionality --


# -- update working directory to the folder this file is in --
os.chdir(os.path.dirname(os.path.abspath(__file__)))


# -- initialise performance timer --
processing_timer = perf_counter()

# -- loop until quit --
while True:

    # -- take a full-screen screenshot, convert to matrix (assuming thats what mat stands for anyways, aka a multi dimensional array) for processing using np.array -- 
    screenshot = ImageGrab.grab() # about 3-5 fps improvement on avg vs pyautogui (which uses python image library anyways)
    screenshot = np.array(screenshot)

    # -- convert our screenshot img to bgr from opencv --
    screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR) 

    # -- print current frame rate for debugging, use floating point format string to change decimal precision --
    current_time = perf_counter()
    print(f"FPS : {1 / (current_time - processing_timer):.2f}")
    processing_timer = perf_counter()

    # -- show screenshot in same window --
    cv.imshow('Comp Vision', screenshot)

    # -- if 1ms per loop to check for q press, if pressed close the window --
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

# -- clean up --
print('Complete')
