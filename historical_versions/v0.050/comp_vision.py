
# -- imports --
import cv2 as cv
import numpy as np




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


# -- driver --
if __name__ == "__main__":
    # get_click_positions(debug_mode="rectangles")
    points = get_click_positions(debug_mode="points")
    print(points)