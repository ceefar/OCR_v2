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

# -- initialise pytesseract for ocr --
pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe" # < required 

# -- ensure pyautogui failsafe is active --
pyautogui.FAILSAFE = True

# -- create a new instance of our screen capture class using the Max Performance window (which is the name of the Bluestacks game)
wincap = WindowCap('Max Performance')


# -- variables --
is_bot_active = False

# -- functions -- 
def get_template_matches_at_threshold(find_img_path, base_img, threshold=0.95):
    # -- debug vars --
    want_confidence = False # True False
    want_results_count = False # True False
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
    return locations

def confirm_at_homepage(screenshot):
    # --
    global is_bot_active
    # --
    home_img_path = "test_imgs/purenub_user_icon_test_withoutLevel_img.png"
    home_img_threshold = 0.999
    # --
    locs = get_template_matches_at_threshold(home_img_path, screenshot, home_img_threshold)
    if locs:
        print(f"Current Page : Home")
        print(f"\nActions")
    faux_input = input("Sup?")
    is_bot_active = False


# -- main - loop until quit --
while True:

    # -- get game window screencap -- 
    screenshot = wincap.get_screencap()

    # -- blit the current screencap --
    cv.imshow("Game Window", screenshot)
        
    # -- confirm we are on the homepage --
    if not is_bot_active:
        is_bot_active = True
        t = Thread(target=confirm_at_homepage, args=(screenshot,))
        t.start()
    
    # confirm_at_homepage(screenshot)

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break