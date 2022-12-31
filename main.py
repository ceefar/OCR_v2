# -- author --
# ceefar

# -- note --
# now this works refactoring in a new project as i actually dont need multi-threading for my original purpose
# but will add it back in future in a refactor for a true portfolio project, 
# this is puurely a personal x learning project  

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

# -- make temp testing directory if it doesnt exist --
try:
    os.mkdir(f"botted_test_imgs") 
except FileExistsError:
    pass

# -- variables --
is_bot_active = False
is_bot_home = False # being at homepage essentially is our blank slate to start running bot actions, our bot will return here when its actions have been completed
user_action_select = 0
matches_dict = {}
all_processed_matches_list = []

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
        print('\nBest match confidence: %s' % max_val)
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


def wipe_folders():
    folders_list = ["bot_test_imgs/"]
    for folder_path in folders_list:
        for file in os.listdir(folder_path):
            print(file)
            os.remove(f"{folder_path}{file}")


def wipe_nested_folders():
    folders_list = ["botted_test_imgs/"]
    for folder_path in folders_list:
        for nested_folder in os.listdir(folder_path):
            for file in os.listdir(f"{folder_path}{nested_folder}"):
                print(f"Deleted {file}")
                # -- remove files in directories --
                os.remove(f"{folder_path}{nested_folder}/{file}")
            # -- then remove the empty directories too --
            os.rmdir(f"{folder_path}{nested_folder}")


def confirm_at_page(screenshot, page_name="profile_home"):
    # --
    global is_bot_active
    # will use a dict for this or sumnt else idk yet actually tbf, either way rn its just testing
    if page_name == "profile_home":
        home_img_path = "test_imgs/profile_home_purenub_img.png" # purenub_user_icon_test_withoutLevel_img
        home_img_threshold = 0.999
        locs, _ = get_template_matches_at_threshold(home_img_path, screenshot, home_img_threshold)
        sleep(0.5)
        if locs[0].size:
            print(f"Current Page : Profile - Home")
            sleep(0.5)
            return True
        else:
            return False
    # -- yeah defo will do this better just rushing it out to test stuff --
    if page_name == "battlelog_all":
        battlelog_img_path = "test_imgs/profile_all_matches_dropdown.png" # profile_all_matches_dropdown profile_battle_log_my_videos_btn 0.99
        battlelog_img_threshold = 0.999
        locs, find_img = get_template_matches_at_threshold(battlelog_img_path, screenshot, battlelog_img_threshold)
        sleep(0.5)
        if locs[0].size:
            rects = get_matched_rectangles(find_img, locs)
            points, ss_with_points = draw_points(rects, screenshot)
            sleep(0.5)
            return True, ss_with_points 
        else:
            return False, False   


def get_words_in_image(img):
    words_in_image = pytesseract.image_to_string(img)
    return words_in_image


def clean_time(time:str):
    time = time.replace("/","_").replace(":","_").replace(" ","_")
    return time


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
    return img_array[y:y + height, x:x+width] 


def find_games_on_page(screenshot, loop_int):
    # note : be smart and just decrement the confidence for the threshold on the back button if we cant find it?
    # note think will be best to actually crop out say the top the and process them this way or sumnt
    global is_bot_active, matches_dict
    location_img_path = "test_imgs/profile_battlelog_game_info_btn.png"
    locs, find_img = get_template_matches_at_threshold(location_img_path, screenshot, 0.95) # 95 for 4, 96 for 3, 98 for 2
    rects = get_matched_rectangles(find_img, locs)
    points, returned_img = draw_points(rects, screenshot, "rectangles")
    # new test
    match_times_list = []
    # if we matched the match info button img
    if points:
        matches_search_img = cv.cvtColor(returned_img, cv.COLOR_BGR2RGB)
        matches_search_img = Image.fromarray(matches_search_img)
        matches_search_img.save(f"bot_test_imgs/matches_search_img_{loop_int}.png")

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
    # print(f"{match_times_list = }")
    # print(f"{matches_dict = }")


def process_a_game(btn_pos, game_id):
    print(f"Processing Game : {game_id}...")
    click_at_pos(btn_pos)
    sleep(3)
    game_img = wincap.get_screencap()
    game_img = cv.cvtColor(game_img, cv.COLOR_BGR2RGB)
    game_img = Image.fromarray(game_img)
    match_time = clean_time(game_id) 
    current_match_folder = f"match_{match_time}"
    game_img.save(f"botted_test_imgs/{current_match_folder}/match_info_main.png")
    locs, find_img = get_template_matches_at_threshold("test_imgs/back_btn.png", screenshot, 0.97) # back down to 0.97 tho seems to match at 0.99999 or even occassionally 1
    rects = get_matched_rectangles(find_img, locs)
    points, _ = draw_points(rects, screenshot, "points")
    if points:
        #print(f"Found Back Btn @ {points[0]}")
        print(f"Game Processing Complete. Returning To Battlelog\n")
        click_at_pos(points[0])
        sleep(3)
        return True


def click_at_pos(position):
    # print(f"Clicking @ {position}...")
    target = wincap.get_true_pos(position)
    pyautogui.moveTo(x = target[0], y = target[1])
    pyautogui.click()
    sleep(3) # sleep at the end to give time for the screen to update from the interaction 
    

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
    print(f"")
    is_bot_active = False


def scroll_battlelog_matches():
    # -- initial scrolling test stuff --
    print("STARTING SCROLL TEST")
    sleep(3) 

    # pyautogui.displayMousePosition()
    mouse_x, mouse_y = pyautogui.position()
    print("Mouse Initial Pos")
    print(f"{mouse_x} {mouse_y}")
    sleep(1.5)

    pyautogui.moveTo(x = mouse_x, y = mouse_y + 200) # scuffed positions before, this is actually at the back button so move down 
    mouse_x, mouse_y = pyautogui.position()
    print("Mouse Moved Pos, Starting Scroll...")
    print(f"{mouse_x} {mouse_y}")
    sleep(1.5)

    pyautogui.scroll(-100) # 215?
    print("Mouse Scrolled Pos")
    mouse_x, mouse_y = pyautogui.position()
    print(f"{mouse_x} {mouse_y}")

    # -- log scroll complete, then sleep for scrolling to end --
    print(f"Scroll Completed") # have some kinda index value to add to this so we know how many loops we've done (isnt necessary but cant hurt either)
    sleep(6)


def run_bot_action_1(screenshot): 

    global is_bot_active, user_action_select, matches_dict, all_processed_matches_list
    print(f"1. {user_action_select = }")

    # temp for testing
    loop_action = 0
    completed = False
    
    go_to_profile = True
    # -- go to profile, but dont continue until confirmed --
    while go_to_profile:
        # -- log actions progression --
        print(f"Attempting Navigation : Profile - Home ")
        # -- update the screenshot --
        screenshot = wincap.get_screencap() # dont think i need this one btw duhhh
        click_on_image(screenshot, "test_imgs/purenub_user_icon_test_withLevel_img.png", 0.98, "home")
        sleep(4)
        screenshot = wincap.get_screencap()
        success = confirm_at_page(screenshot, "profile_home")
        # -- if confirmed at location, continue --
        if success:
            print(f"Confirmed Page : Profile - Home\nContinuing...") 
            go_to_profile = False # dont need this and break duhhh
            break
        # -- else try again
        else:
            print(f"Couldn't Confirm Page : Profile - Home\nTrying Again in 2 Seconds...") 
            sleep(2)

    # -- go to battlelog, but dont continue until confirmed --
    while True:

        # -------- [navigate to battlelog-all] --------

        # -- log actions progression --
        print(f"Attempting Navigation : Battlelog - All Matches")
        # -- update the screenshot, attempt clicking the image to go to battlelog, wait 4 seconds, check success  --
        # screenshot = wincap.get_screencap() # << REMOVED QUICKLY TO TEST
        click_on_image(screenshot, "test_imgs/profile_match_history_btn.png", 0.99, "profile")
        sleep(5) 
        # new - click on all (so not current season), not guna add the confirm rn but obvs will do for final version 
        print(f"New! - All Seasons Btn Testing")
        screenshot = wincap.get_screencap()
        click_on_image(screenshot, "test_imgs/all_seasons_2_btn.png", 0.99, "all_seasons")
        sleep(5) 
        screenshot = wincap.get_screencap()
        was_successful, success_img = confirm_at_page(screenshot, "battlelog_all")
        # -- if page has been confirmed, break the loop and continue to processing games --
        if was_successful:
            print(f"Confirmed Page : Battlelog - All Matches\nContinuing...") 
            # -- save the image we processed --
            success_img = cv.cvtColor(success_img, cv.COLOR_BGR2RGB)
            success_img = Image.fromarray(success_img)
            success_img.save(f"bot_test_imgs/battlelog_all.png")

            # -------- [navigate to battlelog-all] --------

            # -- update the screenshot --
            screenshot = wincap.get_screencap()
            # -- find games on page, saving globally due to multi-threading (globals is just substantially easier implementation so im fine with it) --
            loop_action += 1
            find_games_on_page(screenshot, loop_action)
            # -- process all the games on screen based on their info button and the game_id (which is just the datetime of the game) --
            while True:
                # -- process games in a loop --
                for game_id, game_info_dict in matches_dict.items():
                    was_processed = process_a_game(game_info_dict['btn_pos'], game_id)
                    if was_processed:
                        matches_dict[game_id]["processed"] = True
                        # NEW - if processed store for all
                        all_processed_matches_list.append(game_id)

                # -- scroll the page --
                scroll_battlelog_matches()
            
                # -- now we've scrolled update the screenshot, wipe the existing matches dict, and check for new games  --
                screenshot = wincap.get_screencap()
                matches_dict = {} 
                loop_action += 1
                find_games_on_page(screenshot, loop_action)
                sleep(0.5)

                # -- check for any new unprocessed games --
                any_false = False
                for game_info_dict in matches_dict.values():
                    is_processed = game_info_dict["processed"]
                    if not is_processed:
                        any_false = True
                        # break, why'd i remove this?

                # -- check if we've already processed these games --
                any_false_processed = False
                for game_id in matches_dict.keys():
                    if game_id not in all_processed_matches_list:
                        any_false_processed = True
                        # break

                # -- if any games are not processed this loop or in previous loops, we want to continue in the loop processing games --
                if any_false and any_false_processed:
                    print(f"Found Un-Processed Games. Starting Processing...")
                    continue

                # -- else if we didnt find any un-processed games, we break this while loop, and end this bot action by returning to the home page --
                else:
                    print(f"All Games Processed Successfully. Returning To Home Page...")

                    # -- important - reset everything now this entire bot action is completed --
                    matches_dict = {}
                    user_action_select = 0
                    # todo => return to home page (after the break tho so its outside the loop)
                    completed = True
                    break

                    # not guna do this but no cap you could just let it run twice everytime and check the last two images to each other, if they match at a high threshold then break

        else:
            print(f"Couldn't Confirm Page : Battlelog - All Matches\nTrying Again in 2 Seconds...") 
            sleep(2)
            # break # < temp but incase it breaks huh
    
        if completed:
            is_bot_active = False
            break # breaks from completing loop actions to here
 




# so ig obvs can just start with legit just keep looping while true or sumnt
# but ideally and may just do like this from the start
# confirming if can continue, if you can then do it
# - attempt scroll
# - recheck the btn pos / game id 
#   - maybe a new var for this btw before wiping it (like previous_ ... or sumnt)
# - if not the same btns (consideration that 3 on page might be previous but one might not)
#   - obvs dont run it on the same ones only Processed = False

# YEAH SO TRY USING THE CONDITIONAL STUFF IVE ALREADY DONE FOR processed var in dict as this basically IS the loop condition (or atleast can be, lets try it)





def run_bot_action_2(): # test af name obvs
    global is_bot_active, user_action_select
    print(f"2. {user_action_select = }")
    user_action_select = 0 
    is_bot_active = False


def click_on_image(screenshot, path_to_img, threshold=0.99, file_name="test"):
    global is_bot_active, current_state
    # --
    locs, find_img = get_template_matches_at_threshold(path_to_img, screenshot, threshold)
    rects = get_matched_rectangles(find_img, locs)
    points, ss_with_points = draw_points(rects, screenshot)
    if points:
        ss_with_points = cv.cvtColor(ss_with_points, cv.COLOR_BGR2RGB)
        ss_with_points = Image.fromarray(ss_with_points)
        ss_with_points.save(f"bot_test_imgs/{file_name}.png")
        # --
        print("Found Image. Clicking...\n")
        target = wincap.get_true_pos(points[0])
        pyautogui.moveTo(x = target[0], y = target[1])
        pyautogui.click()
    else:
        print(f"Couldnt Find Given Image. No Click Attempted.\n")
    sleep(1) # sleep at the end to give time for the screen to update from the interaction, should be handling outside tho which is why this is short



# -- wipe folders first --
wipe_folders()
wipe_nested_folders()

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
