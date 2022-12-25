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
from comp_vision import *

# new test
import queue
my_queue = queue.Queue()

def storeInQueue(f):
  def wrapper(*args):
    my_queue.put(f(*args))
  return wrapper

# -- initialise test vars --
test_state = 0
temp_inc = 0


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


# -- test bot to check if we are logged in and on the home page --
def checker_bot_test(screenshot):
    # will likely make this a bot class and have unique actions but for now still testing stuff out 
    global is_bot_active, is_logged_in
    # -- sleep for a few seconds to allow pages to load, and to allow for incrememntal rerun if not initially successful (due to slow loading) --
    sleep(2)
    # -- 
    # locs, find_img = get_template_matches_at_threshold("test_imgs/play_btn_test_1_img.png", screenshot, threshold=0.99)
    # rects = get_matched_rectangles(find_img, locs)
    # points = draw_points(rects, screenshot)
    # if points:
    # if rects.all():
    # if len(rects):
    # -- look for play button --
    success_play_btn, find_img = get_template_matches_at_threshold("test_imgs/play_btn_test_1_img.png", screenshot, threshold=0.99, only_confirm_mathces_at_threshold=True)
    if success_play_btn:
        print(f"Found Play Button - Login Success Confirmed")
        print(f"\nCurrent Page = Home")
        is_logged_in = True
    # -- free up resources and start a new thread by using resetting global --
    is_bot_active = False
    
@storeInQueue
def go_to_user_profile_home(screenshot):
    global is_bot_active
    print(f"Start Go To User Profile Home")
    locs, find_img = get_template_matches_at_threshold("test_imgs/play_btn_test_1_img.png", screenshot, threshold=0.99)
    rects = get_matched_rectangles(find_img, locs)
    points, ss_with_points = draw_points(rects, screenshot)
    if points:
        print("Attempting Click User Profile...")
        target = wincap.get_true_pos(points[0])
        pyautogui.moveTo(x = target[0], y = target[1])
        pyautogui.click()
        return ss_with_points
    sleep(2)







# -- main --

# -- loop until quit --
while True:

    # -- get game window screencap -- 
    screenshot = wincap.get_screencap()

    # -- print current frame rate for debugging, use floating point format string to change decimal precision - for proper version use pyqt for info and just have fps in terminal bosh --
    want_framerate = False
    if want_framerate:
        current_time = perf_counter()
        print(f"FPS : {1 / (current_time - processing_timer):.2f}")
        processing_timer = perf_counter()


    new_ss = False

    # -- test bot actions using multithreading --
    if not is_bot_active:
        # -- activate the bot first for consistency --
        is_bot_active = True

        # -- if not logged in run the log-in check in a new thread, so we dont clog up the output display blit while processing and waiting --
        if not is_logged_in:
            print(f"Starting Login Thread...\n")
            t = Thread(target=checker_bot_test, args=(screenshot,))
            t.start()
    
        # -- if not logged in run the log-in check in a new thread, so we dont clog up the output display blit while processing and waiting --
        if is_logged_in:
            print(f"Starting Click Profile Thread...\n")
            t = Thread(target=go_to_user_profile_home, args=(screenshot,))
            t.start()    
            # use queue to get back our img data from the thread
            my_data = my_queue.get()
            # 
            if len(my_data):
                cv.imshow("Results", new_ss)

    # -- blit the current screencap --
    cv.imshow("Results", screenshot)

    # -- if 1ms per loop to check for q press, if pressed close the window --
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

# -- clean up --
print('Complete')


# -- driver -- 
if __name__ == "__main__":
    ...



# in pyqt5
# to do things like current page
# buttons for interactions
# and even an option to see the current computer vision (or last computer vision or last action saved as an image or sumnt) <<= ok so all that stuff is defo for future lol


# so sectioned out enough to be happy with it for now
# plus multi-threading working nicely
# and have freed up quite a few extra resources during the refactor which is nice
# so....
# now its the below thing you want to do
# - ok ive confirmed im on the home page
# - show the user what actions they can take from the home page
# - take the action 
# - confirm the next page and show the actions that can be taken 
#   - could use deque or a stack or whatever to store an order of the actions (probably a decent idea tbf but is also long and not at all required lol) 

# so start by adding the home options
# starting from top left


# THEN NO CAP
# A PYQT5 OR TERMINAL
# BUT A WAY TO TOGGLE BETWEEN GOING TO BATTLELOG, HOME, OR MY USER PROFILE PAGE, USING TERMINAL OR QT
# - with the thought being to some kind of basic flow 
# - where the bot confirms where it is
# - and then gives relevant options on what to do
# - bosh love it


# THEN GET ON TO THIS...
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


