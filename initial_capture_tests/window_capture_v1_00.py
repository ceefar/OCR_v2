# -- imports --
import cv2 as cv # for img manipulation, etc
import numpy as np # for array conversion 
import pyautogui # for interface automation
import os # for file handling
import PIL # for img manipulation, etc
from time import perf_counter # for performance timing


# -- testing functionality --


# -- update working directory to the folder this file is in --
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# -- loop until quit --
while True:

    # -- take a full-screen screenshot, convert to matrix (assuming thats what mat stands for anyways, aka a multi dimensional array) for processing using np.array -- 
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)

    # -- convert our screenshot img to bgr from opencv --
    screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR) # 0.0035s
    # screenshot = screenshot[:, :, ::-1].copy() # 0.0148s # i guess this is just reordering the array by flipping the blue to the front using ::-1 array slice

    # -- show screenshot in same window --
    cv.imshow('Comp Vision', screenshot)

    # -- if 1ms per loop to check for q press, if pressed close the window --
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

# -- clean up --
print('Complete')
