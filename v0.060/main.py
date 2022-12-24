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


# so now we can click the login we want something to
# first confirm we are on the home page (simple af for now is fine, even if its just text or whatever)
# then confirm we are on the login page
# do the login

# consider pyqt5

# will do this properly shortly, but i think the best thing to do will be states, and have obvs the login state be 0 or 1, 
# and then once we move out of that state its more free (to do a multitude of tasks, instead of just this one (login))




# -- test main --
def main():

    # -- initialise test vars --
    test_state = 0
    temp_inc = 0

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

        # -- print current frame rate for debugging, use floating point format string to change decimal precision --
        # for proper version use pyqt for info and just have fps in terminal bosh
        want_framerate = False
        if want_framerate:
            current_time = perf_counter()
            print(f"FPS : {1 / (current_time - processing_timer):.2f}")
            processing_timer = perf_counter()

        # -- if 1ms per loop to check for q press, if pressed close the window --
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break
        
        # so ig what i actually want is to have something confirm the page first
        # then set some kinda PageState or sumnt like that
        # and obvs then the below state stuff will be broken up into more relevant functions and then actions for each state
        # which can be trigger (by pyqt5, which ill add once everything else is more finalised)
        # - for sure 100% do this but again since im still figuring stuff out
        # - im guna do this after getting a super basic alpha laid down
        # - so i have a better understanding of the general flow i want for the program 


        # -- initial state --
        if test_state == 0:
            temp_inc += 1
            if temp_inc >= 30:
                temp_inc = 0
                test_state = 1
                print(f"\nStarting Login Process")


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

            # also obvs just testing here but a function for stuff like this would be best huh
            # - legit just give it the image and let it make the click for example or sumnt similar
            # - hmmm maybe not actually but for sure something more specialised for login (since is only time for text entry)

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
                pyautogui.write("hiitzsenna4") 
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
                pyautogui.write("e150upm4n") 
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

            # then here just sumnt super simple to confirm we are actually logged in




        # so just continue
        # note it wasnt printing the result count here as the login_password_img needs to be the selected one
        # so anyways to do
        # - the above next section with the above note ting
        # - move password and username to secrets or sumnt so can upload
        #   - if that is long then just dont upload the un and password obvs
        # - then obvs clicking login and waiting bosh
        # - also change the window name from results please, maybe to a global yanno
        #   - its *actually* a legitimate use for global too lol
        # - and then upload it and make a new version!

        # then its the fun stuff for going to pages n processing things
        # - remember do still want a db but imo could just save as xsl or json or whatever for now
        # - should check riots own json file yanno!
        #   - 100% compatability with any kinda image creator to work with both their data and my data would be insanely awesome
        # - start by just doing the average rank of each player and the score?


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


