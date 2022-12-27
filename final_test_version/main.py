# -- external imports --
import cv2 as cv # for img manipulation, etc
import numpy as np # for array conversion 
import pyautogui # for interface automation
import os # for file handling
from PIL import Image, ImageGrab, ImageDraw, ImageFont, ImageFilter # likely guna be some unused that can be removed tbf
from time import perf_counter, sleep # for performance timing, sleeping
from threading import Thread
from pytesseract import pytesseract
from pytesseract import Output
from datetime import datetime
import queue

# -- internal imports --
from cls_windowCap import WindowCap
from comp_vision import *

# -- initialise pytesseract for ocr --
pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe" # < required 

# new test - using queue for getting return vals from threads
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
matches_dict = {}

# -- ensure pyautogui failsafe is active --
pyautogui.FAILSAFE = True

# -- create a new instance of our screen capture class using the Max Performance window (which is the name of the Bluestacks game)
wincap = WindowCap('Max Performance')

# -- initialise performance timer --
processing_timer = perf_counter()


# -- to move to module artist.py, maybe even as class but doesnt really matter tbf --
def create_bounding_img(img, padding):
    """ add padding to an image """
    img_w = img.shape[1]
    img_h = img.shape[0]
    new_w, new_h = img_w + padding, img_h + padding
    new_x, new_y = padding/2, padding/2
    # creating new image object
    imgnew = Image.new("RGB", (new_w, new_h), color='#8ecae6')
    # save
    imgnew.save('test_imgs/match_padder.png')


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
def find_page(screenshot):
    """ incrementally go through the pages (starting from top level - tho in future a stack/queue could be good too) checking to see which of the main pages / page types we are on currently """ # profile_text_img
    global is_bot_active, current_state, confirmed_page
    # note probably a much better idea to convert this to a deque
    # - actually best thing to do is to run performance timing on this stuff first tbf
    location_img_paths = {"home":{"img":"test_imgs/purenub_user_icon_test_withoutLevel_img.png", "threshold":0.999},
                    "login":{"img":"test_imgs/login_existing_login_btn_img.png", "threshold":0.99}, 
                    "profile_home":{"img":"test_imgs/profile_home_purenub_img.png","threshold":0.99}, 
                    "profile_battlelog":{"img":"test_imgs/profile_battle_log_my_videos_btn.png","threshold":0.97},
                    "game_info_ranked":{"img":"test_imgs/game_info_ranked_img.png","threshold":0.999}}
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


def clean_time(time:str):
    time = time.replace("/","_").replace(":","_").replace(" ","_")
    return time


def find_matches_test(screenshot):
    # note think will be best to actually crop out say the top the and process them this way or sumnt
    global is_bot_active
    location_img_path = "test_imgs/profile_battlelog_game_info_btn.png"
    locs, find_img = get_template_matches_at_threshold(location_img_path, screenshot, 0.95) # 95 for 4, 96 for 3, 98 for 2
    rects = get_matched_rectangles(find_img, locs)
    points, returned_img = draw_points(rects, screenshot, "points")
    # new test
    match_times_list = []
    # if we matched the match info button img
    if points:
        print(f"Found Selectable Matches")
        for found_match_btn_point in points:
            cropped_match_img = crop_img(returned_img, found_match_btn_point[0] - 1075, found_match_btn_point[1] - 53, 1203, 115)
            window_uuid = datetime.now() # generate a unique name for the window each time

            # cv.imshow(f"vision_{window_uuid}", returned_img)
            # cv.imshow(f"crop_{window_uuid}", cropped_match_img)

            # words = get_words_in_image(cropped_match_img)

            # new_test_img, words_list = draw_word_boxes(cropped_match_img)
            # processed_imgs = run_image_pre_processing(cropped_match_img)

            # cv.imshow(f"ocr_{window_uuid}", final_match_img) # new_test_img

            # -- run light processing and ocr to get time of match as string --
            cropped_match_time_img = crop_img(cropped_match_img, 800, 5, 200, 40)
            match_time = get_words_in_image(cropped_match_time_img)
            match_time_slicer = match_time.rfind("\n")
            match_time = match_time[:match_time_slicer]
            match_times_list.append(match_time)
            matches_dict[match_time] = {}
            matches_dict[match_time]["processed"] = False # for storing all matches, not just the page we are currently processing, false for not processed
            matches_dict[match_time]["btn_pos"] = found_match_btn_point 
            match_time = clean_time(match_time)
            print(f"{match_time = }")   

            # -- convert colour to rgb, and then convert numpy array to img --
            cropped_colour_convert = cv.cvtColor(cropped_match_img, cv.COLOR_BGR2RGB)
            paste_crop = Image.fromarray(cropped_colour_convert)
            
            # -- new - create folders of matches for proper organising of extracted data -- 
            current_match_folder = f"match_{match_time}"
            try:
                os.mkdir(f"botted_test_imgs/{current_match_folder}") 
            except FileExistsError:
                pass
                        
            paste_crop.save(f"botted_test_imgs/{current_match_folder}/battlelog_match.png")
            fore_img = cv.imread(f"botted_test_imgs/{current_match_folder}/battlelog_match.png", -1)
            final_match_img = cv.imread("test_imgs/match_padder.png", -1)

            # padding = 100
            # create_bounding_img(cropped_match_img, padding)
            x_offset=y_offset=50
            final_match_img[y_offset:y_offset+fore_img.shape[0], x_offset:x_offset+fore_img.shape[1]] = fore_img

            new_test_img, words_list = draw_word_boxes(final_match_img)
            with open(f'botted_test_imgs/{current_match_folder}/battlelog_match_ocr.txt', 'w') as f:
                for word in words_list:
                    f.write(f"{word}\n") 
            
            ocr_test_img = cv.cvtColor(new_test_img, cv.COLOR_BGR2RGB)
            ocr_test_img = Image.fromarray(ocr_test_img)

            # saving
            ocr_test_img.save(f"botted_test_imgs/{current_match_folder}/battlelog_match_ocr.png")

            # show window
            want_show_window = False
            if want_show_window:
                cv.imshow(f"ocr_{window_uuid}", cropped_match_time_img)
                cv.waitKey()

    # --
    print(f"{match_times_list = }")
    is_bot_active = False


def click_at_pos(position):
    print(f"Clicking @ {position}...")
    target = wincap.get_true_pos(position)
    pyautogui.moveTo(x = target[0], y = target[1])
    pyautogui.click()
    sleep(2) # sleep at the end to give time for the screen to update from the interaction 



def process_match_test(screenshot, btn_pos, match_id):
    print(f"\nProcess Match")
    click_at_pos(btn_pos)
    sleep(5)
    success, find_img = get_template_matches_at_threshold("test_imgs/game_info_ranked_img.png", screenshot, 0.999, only_confirm_mathces_at_threshold=True)
    if success:
        screenshot_img = Image.fromarray(screenshot)
        match_time = clean_time(match_id)
        current_match_folder = f"match_{match_time}"
        screenshot_img.save(f"botted_test_imgs/{current_match_folder}/match_result_full.png")
        locs, find_img = get_template_matches_at_threshold("test_imgs/back_btn.png", screenshot, 0.97)
        rects = get_matched_rectangles(find_img, locs)
        points, returned_img = draw_points(rects, screenshot, "points")
        if points:
            print("Found Back Btn")
            print(f"{points[0] = }")
            # click_at_pos(points[0])
            # sleep(5)
    


    is_bot_active = False






# so this is working but a its a complete mess now which is fine as was really just trying to test as much as possible
# also partly due to being farily new to multithreading

# anyways legit just guna rewrite this now as i know much better what I want to implement and how to implement it
# :D  



# save the page image in the folder properly with some light croppping maybe
# - start by just cropping the main things i wanna save, which are the result, and then the kdas (tho will do this by player ig)
# then its processing the players in the same way as the match list button press thing
# again just get their rank ocr only for now but still save their main page (and fuck it maybe their stats page too)



def run_image_pre_processing(img):
    """ performs simple preprocessing (blur, binary, gaussian blur), on an image and returns the resulting images in a list """
    # img = cv.medianBlur(img, 5)
    ret, th1 = cv.threshold(img, 127, 255, cv.THRESH_BINARY) # ret = return (i believe for success or failure), should just use _ but seems to be convention to leave it?
    # th2 = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 11, 2)
    # th3 = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)
    images = [img, th1] # th2, th3
    return images 


def get_words_in_image(img):
    words_in_image = pytesseract.image_to_string(img)
    return words_in_image


def img_to_greyscale(img):
    grey_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    return grey_img


def draw_word_boxes(img):
    image_data = pytesseract.image_to_data(img, output_type=Output.DICT)
    words_list = []
    for i, word in enumerate(image_data['text']):
        if word != '':
            x,y,w,h = image_data['left'][i],image_data['top'][i],image_data['width'][i],image_data['height'][i]
            cv.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
            cv.putText(img,word,(x,y-16),cv.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
            words_list.append(word)
    # --
    return img, words_list


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

        
            if matches_dict:
                print(f"{matches_dict = }")
                for match_id, match_info_dict in matches_dict.items():
                    is_processed = match_info_dict["processed"]
                    btn_pos = match_info_dict["btn_pos"]
                    if not is_processed:
                        print(f"Processing {match_id = }") # need to pass this as well obvs btw
                        is_bot_active = True
                        t = Thread(target=process_match_test, args=(screenshot, btn_pos, match_id))
                        t.start()

            # -- regularly reset the page checker while debugging --              
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




# THEN CLICK THRU AND DO STUFF ON THE PAGE
# - FOR NOW JUST TAKE ALL SCREENSHOTS AND SAVE PROPERLY THEN BOUNCE
# REPEAT FOR ALL 4 ON PAGE

# THEN BOSH

# THEN ITS JUST...
# DO SCROLL
# DO DATA EXTRACTION, PRE-PROCESSING, OCR, AND DATA ANALYSIS

# THEN BOSH AGAIN

# ALSO N0TE 
# - COULD START ADDING IN PYQT5 STUFF
# - COULD ALSO JUST REFACTOR THE WHOLE THING FROM SCRATCH NOW MAYBEH?

# ALSO N0TE
# - KEEP A HIDDEN FOLDER TO STORE VARIOUS CLIPS DURING THE PROGRESS FOR THE THAT I CAN USE FOR THE WRITE UP
# - ALSO VIDS WOULD BE HELLA USEFUL HUH

