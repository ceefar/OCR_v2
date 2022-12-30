from time import sleep
import pyautogui


def scroll_battlelog_matches(i):

    print(f"STARTING SCROLL TEST {i}")
    mouse_x, mouse_y = pyautogui.position()
    print("Mouse Initial Pos")
    print(f"{mouse_x} {mouse_y}")
    sleep(1)

    pyautogui.scroll(-200) # 215?
    print("Mouse Scrolled Pos")
    mouse_x, mouse_y = pyautogui.position()
    print(f"{mouse_x} {mouse_y}")


    print(f"Scroll Completed") 
    sleep(6)


sleep(3)
scroll_battlelog_matches(1)
scroll_battlelog_matches(2)
scroll_battlelog_matches(3)
scroll_battlelog_matches(4)
scroll_battlelog_matches(5)
scroll_battlelog_matches(6)
