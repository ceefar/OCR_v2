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
current_state = "logged_in"


# -- actually appropriate global vars --
account_username = "hiitzsenna4" # will make these secrets tho tbf
account_password = "e150upm4n"
is_logged_in = True
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


def click_on_user_profile(screenshot):
    global is_bot_active, current_state
    print(f"Attempting To Go To User Profile Page")
    locs, find_img = get_template_matches_at_threshold("test_imgs/purenub_user_icon_test_withoutLevel_img.png", screenshot, threshold=0.99)
    rects = get_matched_rectangles(find_img, locs)
    points, ss_with_points = draw_points(rects, screenshot)
    if points:
        print("Found User Profile. Navigating...")
        target = wincap.get_true_pos(points[0])
        pyautogui.moveTo(x = target[0], y = target[1])
        pyautogui.click()
        sleep(2) # sleep at the end to give time for the screen to update from the interaction 
        current_state = "user_profile_home" # < OBVS TEMP
        is_bot_active = False
    else:
        # if we dont find points, sleep for 5 seconds before rerunning this code to try again
        print(f"Couldnt Find Given Image - Trying Again in 4 seconds")
        sleep(4)  
        is_bot_active = False


def click_on_image(screenshot, path_to_img):
    global is_bot_active, current_state
    print(f"Attempting Click")
    locs, find_img = get_template_matches_at_threshold(path_to_img, screenshot, threshold=0.99)
    rects = get_matched_rectangles(find_img, locs)
    points, ss_with_points = draw_points(rects, screenshot)
    if points:
        print("Found Image. Clicking...")
        target = wincap.get_true_pos(points[0])
        pyautogui.moveTo(x = target[0], y = target[1])
        pyautogui.click()
        sleep(2) # sleep at the end to give time for the screen to update from the interaction 
        is_bot_active = False
    else:
        # if we dont find points, sleep for 5 seconds before rerunning this code to try again
        print(f"Couldnt Find Given Image - Trying Again in 4 seconds")
        sleep(4)  
        is_bot_active = False


# -- new test stuff --
confirmed_page = ""
ticker = 0
# -- new test stuff --
def find_page(screenshot):
    """ incrementally go through the pages (starting from top level - tho in future a stack/queue could be good too) checking to see which of the main pages / page types we are on currently """ # profile_text_img
    global is_bot_active, current_state, confirmed_page
    location_img_paths = {"home":{"img":"test_imgs/purenub_user_icon_test_withoutLevel_img.png", "threshold":0.999}, "login":{"img":"test_imgs/login_existing_login_btn_img.png", "threshold":0.99}, "profile_home":{"img":"test_imgs/profile_home_purenub_img.png","threshold":0.99}, "profile_battlelog":{"img":"test_imgs/profile_battle_log_my_videos_btn.png","threshold":0.97}}
    for loc, location_template_info in location_img_paths.items():
        loc_img = location_template_info["img"]
        loc_threshold = location_template_info["threshold"]
        success, find_img = get_template_matches_at_threshold(loc_img, screenshot, loc_threshold, only_confirm_mathces_at_threshold=True)
        if success:
            print(f"Current Screen : {loc}")
            confirmed_page = loc
            break
    print("Multi-threading : sleep 5 seconds")
    sleep(5)
    is_bot_active = False


def find_match_test(screenshot):
    # note think will be best to actually crop out say the top the and process them this way or sumnt
    global is_bot_active, current_state, confirmed_page
    location_img_path = "test_imgs/profile_battlelog_game_info_btn.png"
    locs, find_img = get_template_matches_at_threshold(location_img_path, screenshot, 0.98)
    rects = get_matched_rectangles(find_img, locs)
    points, returned_img = draw_points(rects, screenshot, "rectangles")
    if points:
        print(f"found points")
        cv.imshow("Computer Vision", returned_img)
        cv.waitKey()
    print("Multi-threading : sleep 2 seconds")
    sleep(2)
    is_bot_active = False

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

    # -- test bot actions using multithreading --
    if not is_bot_active:

        # -- if not logged in run the log-in check in a new thread, so we dont clog up the output display blit while processing and waiting --
        if not is_logged_in:
            print(f"Starting Login Thread...\n")
            is_bot_active = True
            t = Thread(target=checker_bot_test, args=(screenshot,))
            t.start()
    
        # -- if not logged in run the log-in check in a new thread, so we dont clog up the output display blit while processing and waiting --
        if is_logged_in:

            if not confirmed_page:
                # test - now doing new 'find what page im on' stuff
                is_bot_active = True
                print(f"Starting New Thread For : Find Page...\n")            
                t = Thread(target=find_page, args=(screenshot,))
                t.start()



            if confirmed_page == "profile_battlelog": 
                is_bot_active = True
                print(f"Starting New Thread For : Find Page...\n")            
                t = Thread(target=find_match_test, args=(screenshot,))
                t.start()
            else:
                # regularly reset the page checker while debugging              
                confirmed_page = ""

            # if current_state != "user_profile_home":
            #     is_bot_active = True
            #     print(f"Starting Click Profile Thread...\n")
            #     t = Thread(target=click_on_user_profile, args=(screenshot,))
            #     t.start()    


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


# MIGHT BE WORTH REWRITING THIS PAGE FROM SCRATCH NOW YANNO!!!!! <<<<<<<<<
# ok so was nice test know what im actually guna do now
# so do it purely with verification like ive just said before
# so from here on out do it by starting with the just base home menu
# but really the first thing that will happen is
# - confirm which page i am on
# - if it confirms the home page
# - it will then show the options
# ...
# for now just between battlelog home and profile page is fine 
# - quickly slide in some pyqt5 even if its basic af?
# ...
# basically once you've nailed that programmatically and properly...


# THEN GET ON TO THIS...
# - start by just doing the average rank of each player in a given match, saving their name and rank, and obvs the result of the match
# - then add in a kda var to this too
# - remember and then was even guna consider template matching for champions too!
# - remember saving abd organising the data properly from the start is important


# THEN IN MORE DETAIL/NOTES/THOUGHTS...
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


# in pyqt5
# to do things like current page
# buttons for interactions
# and even an option to see the current computer vision (or last computer vision or last action saved as an image or sumnt) <<= ok so all that stuff is defo for future lol


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


