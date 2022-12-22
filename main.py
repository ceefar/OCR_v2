# -- external imports --
import cv2 as cv # for img manipulation, etc
import numpy as np # for array conversion 
import pyautogui # for interface automation
import os # for file handling
from PIL import ImageGrab # for grabbing images only at present
from time import perf_counter # for performance timing

# -- internal imports --
from cls_windowCap import WindowCap
 
# -- test main --
def main():
    # -- create a new instance of our screen capture class using the Max Performance window (which is the name of the Bluestacks game)
    wincap = WindowCap('Max Performance')

    # -- update working directory to the folder this file is in --
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # -- initialise performance timer --
    processing_timer = perf_counter()

    # -- loop until quit --
    while True:

        # -- get a full-screen screenshot -- 
        screenshot = wincap.get_screencap()

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


# -- driver -- 
main()




# -- add this in write up --
# - despite not knowing it at the time, the last 2 pygame projects have been insanely useful as insanely similar and functionalities 
# - in libraries like opencv, win32ui/gui, and even helps being brushed up with arrays in relation to images (as per pygame projects) 
# - since its basically the same interaction with numpy
# - and 
# - funnily enough, about contiguous arrays in google foobar
