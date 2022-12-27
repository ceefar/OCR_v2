# -- external imports --
import cv2 as cv # for img manipulation, etc
import numpy as np # for array conversion 
import pyautogui # for interface automation
import os # for file handling
from pytesseract import pytesseract
from time import perf_counter, sleep # for performance timing, sleeping
from PIL import Image, ImageGrab, ImageDraw, ImageFont, ImageFilter # likely guna be some unused that can be removed tbf
from threading import Thread
from pytesseract import Output
from datetime import datetime
import queue

# -- internal imports --
from cls_windowCap import WindowCap
from comp_vision import *

# -- initialise pytesseract for ocr --
pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe" # < required 

# -- ensure pyautogui failsafe is active --
pyautogui.FAILSAFE = True

# -- create a new instance of our screen capture class using the Max Performance window (which is the name of the Bluestacks game)
wincap = WindowCap('Max Performance')


# -- variables --
is_bot_active = False
is_bot_home = False # being at homepage essentially is our blank slate to start running bot actions, our bot will return here when its actions have been completed
user_action_select = 0

# -- functions -- 
def get_template_matches_at_threshold(find_img_path, base_img, threshold=0.95):
    # -- debug vars --
    want_confidence = True # True False
    want_results_count = True # True False
    # -- load image to match, get matches --
    find_img = cv.imread(find_img_path, cv.IMREAD_COLOR) # returns multi-dimensional array (as : y, x - dont ask me why) of each position with its confidence score # 0, -1, cv.IMREAD_UNCHANGED, cv.IMREAD_REDUCED_COLOR_2
    method = cv.TM_CCORR_NORMED
    result = cv.matchTemplate(base_img, find_img, method) 
    # -- get only locations above a given threshold --
    locations = np.where(result >= threshold)
    # -- debug log : confidence at best match --
    if want_confidence:
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        print('Best match confidence: %s' % max_val)
        # print('Best match top left position: %s' % str(max_loc))
    # -- debug log : amount of matches at given threshold --
    if want_results_count:
        print(f"Results @ threshold {threshold} = {locations[0].size}\n") 
    # -- return the resulting list of locations over the threshold --
    return locations, find_img


def confirm_at_homepage(screenshot):
    # --
    global is_bot_active, is_bot_home
    # --
    home_img_path = "test_imgs/purenub_user_icon_test_withoutLevel_img.png"
    home_img_threshold = 0.999
    # --
    locs, _ = get_template_matches_at_threshold(home_img_path, screenshot, home_img_threshold)
    if locs:
        print(f"Current Page : Home")
        is_bot_home = True
    # -- short sleep --
    sleep(0.5)
    is_bot_active = False


def confirm_at_page(screenshot, page_name="profile_home"):
    # --
    global is_bot_active
    # will use a dict for this or sumnt else idk yet actually tbf, either way rn its just testing
    if page_name == "profile_home":
        home_img_path = "test_imgs/purenub_user_icon_test_withoutLevel_img.png"
        home_img_threshold = 0.999
        # --
        locs, _ = get_template_matches_at_threshold(home_img_path, screenshot, home_img_threshold)
        if locs:
            print(f"Current Page : Profile - Home")
            return True
    # -- yeah defo will do this better just rushing it out to test stuff --
    if page_name == "battlelog_all":
        battlelog_img_path = "test_imgs/profile_all_matches_dropdown.png" # profile_all_matches_dropdown profile_battle_log_my_videos_btn 0.99
        battlelog_img_threshold = 0.999
        # --
        locs, find_img = get_template_matches_at_threshold(battlelog_img_path, screenshot, battlelog_img_threshold)
        if locs[0].size:
            rects = get_matched_rectangles(find_img, locs)
            points, ss_with_points = draw_points(rects, screenshot)
            return ss_with_points    
    # -- short sleep --
    sleep(0.5)
    return False
    

def get_bot_actions():
    # --
    global is_bot_active, user_action_select
    # --
    print(f"\n- - - - Actions - - - -")
    print(f"- 1. Save All Games")
    print(f"- 2. A Bot Action")
    print(f"- 9. Quit")
    faux_input = int(input("Enter Your Selection? : "))
    user_action_select = faux_input
    is_bot_active = False

def run_bot_action_1(screenshot): # test af name obvs
    global is_bot_active, user_action_select
    print(f"1. {user_action_select = }")
    click_on_image(screenshot, "test_imgs/purenub_user_icon_test_withLevel_img.png", 0.99, "home")
    success = confirm_at_page(screenshot, "profile_home")
    if success:
        print(f"Location Confirmed")
        print(f"Clicking... Go To Match History")

        # -- update the screenshot --
        screenshot = wincap.get_screencap()

        click_on_image(screenshot, "test_imgs/profile_match_history_btn.png", 0.99, "profile")
        sleep(2)
        
        # -- update the screenshot --
        screenshot = wincap.get_screencap()

        success_img = confirm_at_page(screenshot, "battlelog_all")
        if success_img.any():
            success_img = cv.cvtColor(success_img, cv.COLOR_BGR2RGB)
            success_img = Image.fromarray(success_img)
            success_img.save(f"bot_test_imgs/battlelog_all.png")
            print(f"Current Page : Battlelog - All Matches") 

        # click dis
        # go to leggy
        # - change function name to save all leggy

        # ---- can skip that above bit actually rn duh since its just one change but exact same formatting for everything bosh so... ---

        # then its the whole storing things that are there and cropping etc
        # - both in saved folders ting but then obvs also want to consider dataclasses idea too
        # - start doing the champion image matching too

        # then just do them incrementally and its gravy af

    # -- reset everything now this entire bot action is completed --
    user_action_select = 0
    is_bot_active = False


def run_bot_action_2(): # test af name obvs
    global is_bot_active, user_action_select
    print(f"2. {user_action_select = }")
    user_action_select = 0 # [ IMPORTANT! ] => once actions are completed this must be reset too 
    is_bot_active = False


def click_on_image(screenshot, path_to_img, threshold=0.99, file_name="test"):
    global is_bot_active, current_state
    print(f"Attempting Click")
    # --
    locs, find_img = get_template_matches_at_threshold(path_to_img, screenshot, threshold)
    rects = get_matched_rectangles(find_img, locs)
    points, ss_with_points = draw_points(rects, screenshot)
    sleep(2)
    if points:
        ss_with_points = cv.cvtColor(ss_with_points, cv.COLOR_BGR2RGB)
        ss_with_points = Image.fromarray(ss_with_points)
        ss_with_points.save(f"bot_test_imgs/{file_name}.png")
        # --
        print("Found Image. Clicking...")
        target = wincap.get_true_pos(points[0])
        pyautogui.moveTo(x = target[0], y = target[1])
        pyautogui.click()
        sleep(2) # sleep at the end to give time for the screen to update from the interaction 
    else:
        # if we dont find points, sleep for 5 seconds before rerunning this code to try again
        print(f"Couldnt Find Given Image - Waiting 2 seconds")
        sleep(2)




# -- main - loop until quit --
while True:
    # -- get game window screencap -- 
    screenshot = wincap.get_screencap()
    # -- blit the current screencap --
    cv.imshow("Game Window", screenshot)
    # -- confirm we are on the homepage --
    if not is_bot_home:
        # -- start a new thread to check we are at the home page, and so want to start running a new bot action -- 
        if not is_bot_active:
            is_bot_active = True
            t = Thread(target=confirm_at_homepage, args=(screenshot,))
            t.start()
    # -- if we are on the home page, display the actions to the user --
    if is_bot_home:
        # -- only run one bot thread at a time, using threading so we dont clog up the windowcapture while awaiting action --
        if not is_bot_active:
            # -- if user has selected an action, run it --
            if user_action_select: 
                if user_action_select == 1:
                    # -- start a new thread to run this action --
                    is_bot_active = True
                    t = Thread(target=run_bot_action_1, args=(screenshot,))
                    t.start()
                elif user_action_select == 2:
                    # -- start a new thread to run this action --
                    is_bot_active = True
                    t = Thread(target=run_bot_action_2, args=())
                    t.start()
                elif user_action_select == 9:
                    cv.destroyAllWindows()
                    break
                else:
                    user_action_select = 0
            else:
                # -- else we are home and we havent got a user action yet, so prompt the user for an action --
                is_bot_active = True
                # -- start the thread --
                t = Thread(target=get_bot_actions, args=())
                t.start()
    # --
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break


# get to match history
# store the current 4 games times in memory
# make their folders
# incrementally process them
# return to home
# ensure we get prompted again

# then from here just continue with more saving and processing 
# - ig initial idea to do kdas and saving rank and stats page will be perf for now
