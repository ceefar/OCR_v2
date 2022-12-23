# -- external imports --
import cv2 as cv # for img manipulation, etc
import numpy as np # for array conversion 
import pyautogui # for interface automation
import os # for file handling
from PIL import ImageGrab # for grabbing images only at present
from time import perf_counter, sleep # for performance timing, sleeping

# -- internal imports --
from cls_windowCap import WindowCap


# -- temp ongoing notes --
# so really what i want first is it to detect this login page and then prompt us, so to start do sumnt like this
# - wait for login page
# - use the google riot and facebook symbols since they are also login buttons bosh
# - consider a pyqt5 menu when you CAN login, to prompt for which account etc
# - remember this is just guna be the data extraction and analytics part

# optional but mays well...
# so initially it may be worth only checking the area the we expect those log in buttons to be
# then add in a check everywhere if it doesnt find a match after a set amount of time




def get_click_positions(find_img_path="test_imgs/login_rito.png", base_img_path="test_imgs/login_page2.png", threshold=0.95, debug_mode=None):

    # note
    # confidence at which this is the only match : login_rito (0.96), login_fb (0.95), login_google (0.96 - preferably 0.962 but tbf the best match is correct so its fine)
    
    # load images 
    find_img = cv.imread(find_img_path, cv.IMREAD_UNCHANGED) # 0, -1, cv.IMREAD_UNCHANGED, cv.IMREAD_REDUCED_COLOR_2
    base_img = cv.imread(base_img_path, cv.IMREAD_UNCHANGED)

    # get search/find image dimensions 
    search_w = find_img.shape[1]
    search_h = find_img.shape[0]
    
    # returns multi-dimensional array (as : y, x - dont ask me why) of each position with its confidence score
    method = cv.TM_CCORR_NORMED # TM_CCOEFF_NORMED, TM_CCOEFF, TM_CCORR, TM_CCORR_NORMED, TM_SQDIFF, TM_SQDIFF_NORMED - BEST SO FAR : TM_CCORR_NORMED
    result = cv.matchTemplate(base_img, find_img, method) 
    print(f"{result = }")

    # get only locations above a given threshold
    locations = np.where(result >= threshold)

    # if locations...
    print(f"Results @ threshold {threshold} = {locations[0].size}") # print(locations)

    # convert tuple of np arrays to standard tuple of ints, while maintaining the order of the positions x y positions
    locations = list(zip(*locations[::-1])) # reverse the first dimension of the list, then * unpack the list to remove the outer dimension of the array (i.e. 2 1d arrays not 1 2d array), then zip it together to get xy tuples, then convert our zip object back to a list 

    # create the list of rects [x, y, w, h]
    rectangles = []
    for loc in locations:
        rect = [int(loc[0]), int(loc[1]), search_w, search_h]
        rectangles.append(rect)
        rectangles.append(rect) # add a copy of the rect so that group rect doesnt skip over the edge case of finding only 1 rect (again, more for a live botting situation but leaving the code in since it may be useful in future)

    rectangles, weights = cv.groupRectangles(rectangles, 1, 0.5) # 2nd param = grouping threshold : 1 group when just one overlap (basically), 0 too low, 2+ means needing lots of overlapping rects to group, 3rd param = eps : how close the rects need to be to group them, 0.5 is good start, 1 & 1.5 also good starting points, increasing will group rects that are further away, smaller means they will need to be practically on top of each other to group 
    print(rectangles)
    
    points = []
    if len(rectangles):
        print(f"Match Template Search Successful")

        line_colour = (255, 200, 0)
        line_type = cv.LINE_4

        marker_colour = (255, 0, 0) # pink : 255, 0, 255
        marker_type = cv.MARKER_CROSS

        # loop over all the matched rectangles, then unpack and draw them
        for x, y, w, h in rectangles:

            # calculate center pos
            center_x = x + int(w/2) # again add to portfolio write-ups regarding similarities to pygame
            center_y = y + int(h/2)
            # store the points
            points.append((center_x, center_y))
            
            if debug_mode == "rectangles":
                # calculate rect pos
                top_left = (x, y)
                bottom_right = (x + w, y + h)
                # draw rect
                cv.rectangle(base_img, top_left, bottom_right, line_colour, line_type)

            if debug_mode == "points":
                cv.drawMarker(base_img, (center_x, center_y), marker_colour, marker_type)

        if debug_mode:
            cv.imshow("Results", base_img)
            cv.waitKey(0)
    
    return points


def test(find_img_path="test_imgs/login_rito.png", base_img_path="test_imgs/login_page2.png", threshold=0.95):

    # load images 
    find_img = cv.imread(find_img_path, cv.IMREAD_UNCHANGED) # 0, -1, cv.IMREAD_UNCHANGED, cv.IMREAD_REDUCED_COLOR_2
    base_img = cv.imread(base_img_path, cv.IMREAD_UNCHANGED)

    # returns multi-dimensional array (as : y, x - dont ask me why) of each position with its confidence score
    method = cv.TM_CCORR_NORMED # TM_CCOEFF_NORMED, TM_CCOEFF, TM_CCORR, TM_CCORR_NORMED, TM_SQDIFF, TM_SQDIFF_NORMED - BEST SO FAR : TM_CCORR_NORMED
    result = cv.matchTemplate(base_img, find_img, method) 

    # get best match
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

    print('Best match top left position: %s' % str(max_loc))
    print('Best match confidence: %s' % max_val)

    # threshold = 0.6
    if max_val >= threshold:
        print('Found img')

        # get size of found img
        find_w = find_img.shape[1]
        find_h = find_img.shape[0]

        # Calculate the bottom right corner of the rectangle to draw
        top_left = max_loc # use min_loc for sqdiffs
        bottom_right = (top_left[0] + find_w, top_left[1] + find_h)

        # draw a rect at the found position
        cv.rectangle(base_img, top_left, bottom_right, 
                        color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)

        # save result
        want_save = False
        if want_save:
            cv.imwrite('result.png', base_img)

    else:
        print('Img not found.')

    cv.imshow('Result', base_img)
    cv.waitKey(0)



get_click_positions(debug_mode="points")
get_click_positions(debug_mode="rectangles")
test()
quit()


# -- test main --
def main():

    # -- create a new instance of our screen capture class using the Max Performance window (which is the name of the Bluestacks game)
    wincap = WindowCap('Max Performance')

    # -- update working directory to the folder this file is in --
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # -- initialise performance timer --
    processing_timer = perf_counter()

    # -- loop until quit --
    while True:

        # -- get a full-screen screenshot -- 
        screenshot = wincap.get_screencap()

        # -- print current frame rate for debugging, use floating point format string to change decimal precision --
        current_time = perf_counter()
        print(f"FPS : {1 / (current_time - processing_timer):.2f}")
        processing_timer = perf_counter()

        # -- show screenshot in same window --
        cv.imshow('Comp Vision', screenshot)

        # -- if 1ms per loop to check for q press, if pressed close the window --
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break

    # -- clean up --
    print('Complete')


# -- driver -- 
main()





# -- add this in write up --
# - despite not knowing it at the time, the last 2 pygame projects have been insanely useful as insanely similar and functionalities 
# - in libraries like opencv, win32ui/gui, and even helps being brushed up with arrays in relation to images (as per pygame projects) 
# - since its basically the same interaction with numpy
# - and 
# - funnily enough, about contiguous arrays in google foobar
