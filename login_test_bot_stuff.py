
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
    points = get_click_positions("test_imgs/login_existing_login_btn_img.png", screenshot, 0.99, "rectangles")
    # -- if we match the login template, move the mouse to the target and click it --
    if points:
        target = wincap.get_true_pos(points[0])
        # -- if we hit 100 on our counter, click the login button, and reset the counter --
        print(f"\nInitialising Login")
        print(f"Rito Login Target Pos = {target}\n")
        pyautogui.moveTo(x = target[0], y = target[1]) # pyautogui.click(x = target[0], y = target[1])
        sleep(2)
        pyautogui.click()

