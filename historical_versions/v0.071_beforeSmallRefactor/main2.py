# -- external imports --
import cv2 as cv # for img manipulation, etc
import numpy as np # for array conversion 
import pyautogui # for interface automation
import os # for file handling
from PIL import ImageGrab # for grabbing images only at present
from time import perf_counter, sleep # for performance timing, sleeping
from threading import Thread

# -- internal imports --
from cls_windowCap import WindowCap
from comp_vision import get_click_positions


# -- initialise test vars --
test_state = 0
temp_inc = 0

# -- super duper temp test bot actions using states --
def login_bot_test(screenshot):
    # -- set vars to globals -- 
    global test_state, temp_inc
    # -- start login --
    if test_state == 0:
        temp_inc += 1
        if temp_inc >= 30:
            temp_inc = 0
            test_state = 1
            print(f"\nStarting Login...")
    # -- home page state --
    if test_state == 1:
        # -- get points for login --
        points = get_click_positions("test_imgs/login_rito.png", screenshot, 0.94, "rectangles")
        # -- if we match the login template, move the mouse to the target and click it --
        if points:
            target = wincap.get_true_pos(points[0])
            # -- create a faux pause in action to allow for loading and interaction times --
            temp_inc += 1
            # -- if we hit 100 on our counter, click the login button, and reset the counter --
            if temp_inc >= 30:
                print(f"\nInitialising Login")
                print(f"Rito Login Target Pos = {target}\n")
                pyautogui.moveTo(x = target[0], y = target[1]) # pyautogui.click(x = target[0], y = target[1])
                pyautogui.click()
                temp_inc = 0
                test_state = 2
    # -- login page state --
    if test_state == 2:
        # N0TE - need a funct that can just do the ocr without the return (could just refactor existing tbf, or save for a future, more finalised version)
        login_page_points = get_click_positions("test_imgs/login_text_img.png", screenshot, 0.96, "rectangles")
        if login_page_points:
            test_state = 3
    # -- login page state part 2 : username select --
    if test_state == 3:
        username_points = get_click_positions("test_imgs/login_username_img.png", screenshot, 0.97, "rectangles")
        temp_inc += 1
        if temp_inc >= 30:
            if username_points:  
                print(f"Adding Username")
                target = wincap.get_true_pos(username_points[0])
                pyautogui.moveTo(x = target[0], y = target[1]) # pyautogui.click(x = target[0], y = target[1])
                pyautogui.click()
                temp_inc = 0
                test_state = 4
    # -- login page state part 3 : username entry --
    if test_state == 4:
        temp_inc += 1
        get_click_positions("test_imgs/login_username_selected_img.png", screenshot, 0.999, "points")
        if temp_inc >= 30:
            pyautogui.write(account_username) 
            temp_inc = 0
            test_state = 5
    # -- login page state part 4 : password select --
    if test_state == 5:
        password_points = get_click_positions("test_imgs/login_password_img.png", screenshot, 0.99, "rectangles")
        temp_inc += 1
        if temp_inc >= 30:
            if password_points:
                print(f"Adding Password")
                target = wincap.get_true_pos(password_points[0])
                pyautogui.moveTo(x = target[0], y = target[1])
                pyautogui.click()
                temp_inc = 0
                test_state = 6
    # -- login page state part 5 : password selection --
    if test_state == 6:
        temp_inc += 1
        get_click_positions("test_imgs/login_password_selected_img.png", screenshot, 0.99, "points")
        if temp_inc >= 30:
            pyautogui.write(account_password) 
            temp_inc = 0
            test_state = 7
    # -- login page state part 6 : login confirmation --
    if test_state == 7:
        login_points = get_click_positions("test_imgs/login_confirm_btn_img.png", screenshot, 0.96, "points")
        temp_inc += 1
        if temp_inc >= 30:
            if login_points:
                print("Attempting Log In...")
                target = wincap.get_true_pos(login_points[0])
                pyautogui.moveTo(x = target[0], y = target[1])
                pyautogui.click()
                temp_inc = 0
                test_state = 8
    # -- login page state part 7 : login & chill --
    if test_state == 8:
        cv.imshow("Results", screenshot)
        return True
    # -- then here just sumnt super simple to confirm we are actually logged in? --


def login_bot():
    # confirm if there is a login button first
    pass


# -- actually appropriate global vars --
account_username = "hiitzsenna4" # will make these secrets tho tbf
account_password = "e150upm4n"
is_logged_in = False
is_bot_active = False # bool to ensure we only have one open thread for bot actions

# -- ensure pyautogui failsafe is active --
pyautogui.FAILSAFE = True

# -- create a new instance of our screen capture class using the Max Performance window (which is the name of the Bluestacks game)
wincap = WindowCap('Max Performance')

# -- initialise performance timer --
processing_timer = perf_counter()

# -- loop until quit --
while True:

    # -- get game window screencap -- 
    screenshot = wincap.get_screencap()

    # -- print current frame rate for debugging, use floating point format string to change decimal precision - for proper version use pyqt for info and just have fps in terminal bosh --
    want_framerate = True
    if want_framerate:
        current_time = perf_counter()
        print(f"FPS : {1 / (current_time - processing_timer):.2f}")
        processing_timer = perf_counter()

    if not is_logged_in:
        completed = login_bot_test(screenshot)
        if completed:
            is_logged_in = True

    if is_logged_in:
        cv.imshow("Results", screenshot)
        print("Now Test Multi-Threading")

    # # -- test bot actions using multithreading --
    # if not is_bot_active:
    #     is_bot_active = True
    #     t = Thread(target=login_bot, args=(screenshot,))
    #     t.start()
    
    # -- if 1ms per loop to check for q press, if pressed close the window --
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

# -- clean up --
print('Complete')


# -- driver -- 
if __name__ == "__main__":
    pass



# THEN DO A QUICK LOGIN WHERE IT JUST DETECTS THE BUTTON AND LOGS IN
# THEN CONFIRMS ITS LOGGED IN AND SETS A STATE FOR IT

# THEN DO THE SMALL REFACTOR 
# - WINDOW SHOW IS IN MAIN
# - HAVE THINGS RETURN TO MAIN THAT YOU NEED

# THEN WHEN THAT STATE IS TRIGGERED 
# WE TRIGGER A MULTITHREADING BOT FUNCTION THAT HAS A SMALL SLEEP IN IT TO TEST IT WORKS (IT DOESNT LOCK UP THE SCREEN)

# BOSH!
# THEN 
# JUST CONTINUE TO THE STUFF BELOW LEGIT SAVING ETC



# ok so do wanna quickly confirm multithreading is working fine
# for this just run the log-in script
# then write a bot action thats more appropriate to test threading works fine
# since login only ever happens once, it really doesnt need to be in a thread tbh


# - start by just doing the average rank of each player in a given match, saving their name and rank, and obvs the result of the match
# - then add in a kda var to this too
# - remember and then was even guna consider template matching for champions too!
# - remember saving abd organising the data properly from the start is important


# so we want
# list all of the matches on the current page
# and create all our initial first folders me thinks
# having the match be saved by 
# - the user who's battlelog its from 
# - and then the datetime of the match
# - e.g. match_accountName_080822_1957
#   - obvs considerations for knowing when you've completed a match and scrolling down but just get it to work on the initial page of whatever X matches first
#   - maybe just have some super basic list for this as a var in memory for now too and we'll just use bools to indicate when a match is completed
#   - could use a stack? (will we need to go back through tho?)
#   - maybe deque?... whatever, anyways

# then store the core stuff for the match in a folder like main info with the imgs of all pages
# and a txt file of the info clean laid out (which well then do in json or xsl or even to db with sql idk yet doesnt matter yet either just txt for now)
# - obvs we're doing the result and the avg rank of each team in this file too but we need to get that first
# for getting the info from each player
# we mays well get their kda info page too
# dont process it yet but save it
# save each player in one of two folders (my team / enemy team)
# and give each of them a folder too where we'll put the imgs and a txt file of the basic info we're extracted and saved
# then process the avg rank of the team and save that
# then we do the entire game file thing to final (maybe its 2 files whatever)
# then i guess lets output to terminal (or pyqt5)
# then legit you just do the next one bosh



# - remember do still want a db but imo could just save as xsl or json or whatever for now
# - should check riots own json file yanno!
#   - 100% compatability with any kinda image creator to work with both their data and my data would be insanely awesome



# -- add this in write up --
# - despite not knowing it at the time, the last 2 pygame projects have been insanely useful as insanely similar and functionalities 
# - in libraries like opencv, win32ui/gui, and even helps being brushed up with arrays in relation to images (as per pygame projects) 
# - since its basically the same interaction with numpy
# - and 
# - funnily enough, about contiguous arrays in google foobar

# for write up
# - note that this particular bit could obvs have been done pretty easy just doing it manually (if on screen then use console to run functionalities)
# - but imo its much better to do things dynamically from the start, then minor ui changes shouldnt affect the functionality
# - and the likelihood of the functionality being compatible with a large array of different device sizes is much more likely doing it this way too


