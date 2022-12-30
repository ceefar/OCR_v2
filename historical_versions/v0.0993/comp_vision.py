import cv2 as cv

# -- functions ---
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