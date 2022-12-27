# -- imports --
import cv2 as cv
import numpy as np

# will make this a class when done tbf, just use the default constructor is fine

def get_click_points(rectangles):
    """ returns center points of a list of rects """
    points = []
    for (x, y, w, h) in rectangles:
        # get center pos
        center_x = x + int(w/2)
        center_y = y + int(h/2)
        # store points
        points.append((center_x, center_y))
    # return posts
    return points

def draw_rects(search_img, rectangles):
       # bgr not rgb
        line_color = (0, 255, 0)
        line_type = cv.LINE_4
        for (x, y, w, h) in rectangles:
            # get the rect pos
            top_left = (x, y)
            bottom_right = (x + w, y + h)
            # draw rect
            cv.rectangle(search_img, top_left, bottom_right, line_color, lineType=line_type)
        # return the result
        return search_img

def draw_crosses(base_img, points):
    # bgr
    marker_color = (255, 0, 255)
    marker_type = cv.MARKER_CROSS
    # loop list of points
    for (center_x, center_y) in points:
        # draw a cross at the center
        cv.drawMarker(base_img, (center_x, center_y), marker_color, marker_type)
    # return the result
    return points, base_img


# -- new detection testing stuff --

def get_template_matches_at_threshold(find_img_path, base_img, threshold=0.95, only_confirm_mathces_at_threshold=False):
    # load images 
    find_img = cv.imread(find_img_path, cv.IMREAD_COLOR) # 0, -1, cv.IMREAD_UNCHANGED, cv.IMREAD_REDUCED_COLOR_2
    # returns multi-dimensional array (as : y, x - dont ask me why) of each position with its confidence score
    method = cv.TM_CCORR_NORMED
    result = cv.matchTemplate(base_img, find_img, method) 
    # new - for logging the confidence while testing
    want_confidence = False
    if want_confidence:
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        # print('Best match top left position: %s' % str(max_loc))
        print('Best match confidence: %s' % max_val)
    # get only locations above a given threshold
    locations = np.where(result >= threshold)
    # log amout of results at this threshold
    want_results_count = False
    if want_results_count:
        print(f"Results @ threshold {threshold} = {locations[0].size}\n") 
    # -- new test --
    # if you only want to confirm we hit the threshold and dont care about the actual points
    if only_confirm_mathces_at_threshold:
        # if there are results over the threshold 
        if locations[0].size:
            # return true plus the preloaded img <<= just make this a function during next refactor duhhhhhh
            return True, find_img
        else:
            return False, find_img
    # return the resulting list of locations over the threshold
    return locations, find_img

def get_matched_rectangles(find_img, locations):
    """ for creating then grouping rects from a list of locations """
    # -- if the locations arg isnt empty --
    if locations:
        # get search/find image dimensions 
        search_w = find_img.shape[1]
        search_h = find_img.shape[0]
        # convert tuple of np arrays to standard tuple of ints, while maintaining the order of the positions x y positions
        locations = list(zip(*locations[::-1])) # reverse the first dimension of the list, then * unpack the list to remove the outer dimension of the array (i.e. 2 1d arrays not 1 2d array), then zip it together to get xy tuples, then convert our zip object back to a list 
        # create the list of rects [x, y, w, h]
        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), search_w, search_h]
            rectangles.append(rect)
            rectangles.append(rect) # add a copy of the rect so that group rect doesnt skip over the edge case of finding only 1 rect (again, more for a live botting situation but leaving the code in since it may be useful in future)
        rectangles, weights = cv.groupRectangles(rectangles, 1, 0.5) # 2nd param = grouping threshold : 1 group when just one overlap (basically), 0 too low, 2+ means needing lots of overlapping rects to group, 3rd param = eps : how close the rects need to be to group them, 0.5 is good start, 1 & 1.5 also good starting points, increasing will group rects that are further away, smaller means they will need to be practically on top of each other to group 
        # -- return the results --
        return rectangles

def draw_points(rectangles, base_img, debug_mode="rectangles"):
    points = []
    if len(rectangles):
        # print(f"Match Template Search Successful")\
        line_colour = (255, 255, 0) # pink : 255, 0, 255
        line_type = cv.LINE_4
        marker_colour = (255, 0, 0) 
        marker_type = cv.MARKER_CROSS
        # loop over all the matched rectangles, then unpack and draw them
        for x, y, w, h in rectangles:
            # calculate center pos
            center_x = x + int(w/2) # again add to portfolio write-ups regarding similarities to pygame
            center_y = y + int(h/2)
            # store the points
            points.append((center_x, center_y))
            # draw based on given debug_mode argument
            if debug_mode == "rectangles":
                # calculate rect pos
                top_left = (x, y)
                bottom_right = (x + w, y + h)
                # draw rect
                cv.rectangle(base_img, top_left, bottom_right, line_colour, line_type)
            if debug_mode == "points":
                cv.drawMarker(base_img, (center_x, center_y), marker_colour, marker_type)
    # -- return the resulting points --
    return points, base_img


# -- driver --
if __name__ == "__main__":
    ...