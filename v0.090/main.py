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
from datetime import datetime
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
    # note probably a much better idea to convert this to a deque
    # - actually best thing to do is to run performance timing on this stuff first tbf
    location_img_paths = {"home":{"img":"test_imgs/purenub_user_icon_test_withoutLevel_img.png", "threshold":0.999}, "login":{"img":"test_imgs/login_existing_login_btn_img.png", "threshold":0.99}, "profile_home":{"img":"test_imgs/profile_home_purenub_img.png","threshold":0.99}, "profile_battlelog":{"img":"test_imgs/profile_battle_log_my_videos_btn.png","threshold":0.97}}
    for loc, location_template_info in location_img_paths.items():
        loc_img = location_template_info["img"]
        loc_threshold = location_template_info["threshold"]
        success, find_img = get_template_matches_at_threshold(loc_img, screenshot, loc_threshold, only_confirm_mathces_at_threshold=True)
        if success:
            print(f"Current Screen : {loc}")
            confirmed_page = loc
            break
    print("Sleep : 2")
    sleep(2)
    is_bot_active = False


def find_matches_test(screenshot):
    # note think will be best to actually crop out say the top the and process them this way or sumnt
    global is_bot_active
    location_img_path = "test_imgs/profile_battlelog_game_info_btn.png"
    locs, find_img = get_template_matches_at_threshold(location_img_path, screenshot, 0.95) # 95 for 4, 96 for 3, 98 for 2
    rects = get_matched_rectangles(find_img, locs)
    points, returned_img = draw_points(rects, screenshot, "points")
    if points:
        print(f"Found Selectable Matches")
        for found_match_btn_point in points:
            cropped = crop_img(returned_img, found_match_btn_point[0] - 1075, found_match_btn_point[1] - 53, 1203, 115)
            window_uuid = datetime.now() # generate a unique name for the window each time
            cv.imshow(f"vision_{window_uuid}", returned_img)
            cv.imshow(f"crop_{window_uuid}", cropped)
            cv.waitKey()
    # --
    is_bot_active = False


    # ok so rn
    # - save each img
    # - ocr
    # - make folder/s and store imgs and text info in folder
    # - ss all and store imgs (and text info?) in folder (where? - maybe just a unique one for this)

    # - pyqt5?
    # - db stuff?
    # - both not rn tbf

    # - again tho remember to add sumnt to be able to confirm / check off (which ig will just be from the ocr) completed items
    #   - i.e. stack or queue (even deque maybe)
    # - once we have all four completed then we scroll
    # - note there is always the potential for 1 pixel to cause problems over lots of scrolls or whatever so just keep that in find 
    



def crop_img(img_array, x, y, width, height):
    """ pass top left & bottom left co-ordinates with width and height to return cropped img """
    # making this a function as will hard code dimensions so can just pass in a name to do this, but for now obvs its just one crop type so just getting it working to test stuff
    return img_array[y:y + height, x:x+width] # img_to_crop = img_array.copy()
    # cropped_img = og_img[200:400, 300:500]
    



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

            # -- current new test stuff for processing match info --
            if confirmed_page == "profile_battlelog": 
                is_bot_active = True
                print(f"Starting New Thread For : Find Page...\n")            
                t = Thread(target=find_matches_test, args=(screenshot,))
                t.start()
        

            # regularly reset the page checker while debugging              
            confirmed_page = ""

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