# -- imports --
import cv2 as cv # for img manipulation, etc
import numpy as np # for array conversion 
import pyautogui # for interface automation
import os # for file handling
import PIL 

# update working directory to the folder this file is in
os.chdir(os.path.dirname(os.path.abspath(__file__)))

while True:

    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = screenshot[:, :, ::-1].copy()

    cv.imshow('Comp Vision', screenshot)

    # if 1ms per loop to check for q press, if pressed close the window
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break


# clean up
print('Complete')
