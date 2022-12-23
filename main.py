# -- external imports --
import cv2 as cv # for img manipulation, etc
import numpy as np # for array conversion 
import pyautogui # for interface automation
import os # for file handling
from PIL import ImageGrab # for grabbing images only at present
from time import perf_counter, sleep # for performance timing, sleeping

# -- internal imports --
from cls_windowCap import WindowCap
from comp_vision import get_click_positions


# -- temp ongoing notes --
# so really what i want first is it to detect this login page and then prompt us, so to start do sumnt like this
# - wait for login page
# - use the google riot and facebook symbols since they are also login buttons bosh
# - consider a pyqt5 menu when you CAN login, to prompt for which account etc
# - remember this is just guna be the data extraction and analytics part

# optional but mays well...
# so initially it may be worth only checking the area the we expect those log in buttons to be
# then add in a check everywhere if it doesnt find a match after a set amount of time

# for write up
# - note that this particular bit could obvs have been done pretty easy just doing it manually (if on screen then use console to run functionalities)
# - but imo its much better to do things dynamically from the start, then minor ui changes shouldnt affect the functionality
# - and the likelihood of the functionality being compatible with a large array of different device sizes is much more likely doing it this way too




# -- test main --
def main():

    # -- create a new instance of our screen capture class using the Max Performance window (which is the name of the Bluestacks game)
    wincap = WindowCap('Max Performance')

    # -- initialise performance timer --
    processing_timer = perf_counter()

    # -- loop until quit --
    while True:

        # -- get game window screencap -- 
        screenshot = wincap.get_screencap()
        points = get_click_positions("test_imgs/login_rito.png", screenshot, 0.94, "rectangles")

        # -- print current frame rate for debugging, use floating point format string to change decimal precision --
        current_time = perf_counter()
        print(f"FPS : {1 / (current_time - processing_timer):.2f}")
        processing_timer = perf_counter()

        # -- if 1ms per loop to check for q press, if pressed close the window --
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break
 
    # -- clean up --
    print('Complete')


# -- driver -- 
if __name__ == "__main__":
    main()





# -- add this in write up --
# - despite not knowing it at the time, the last 2 pygame projects have been insanely useful as insanely similar and functionalities 
# - in libraries like opencv, win32ui/gui, and even helps being brushed up with arrays in relation to images (as per pygame projects) 
# - since its basically the same interaction with numpy
# - and 
# - funnily enough, about contiguous arrays in google foobar
