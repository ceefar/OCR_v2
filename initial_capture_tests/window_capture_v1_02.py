# -- imports --
import cv2 as cv # for img manipulation, etc
import numpy as np # for array conversion 
import pyautogui # for interface automation
import os # for file handling
from PIL import ImageGrab # for grabbing images only at present
from time import perf_counter # for performance timing

# -- new v1.02 test imports --
import win32ui
import win32gui
import win32con


# -- notes -- 
# - as per this version screencap at around 30-35 fps on average, peaks at around 42, lowest around 25 (tho tbf one outliner 19)

# -- add this in write up --
# - despite not knowing it at the time, the last 2 pygame projects have been insanely useful as insanely similar and functionalities 
# - in libraries like opencv, win32ui/gui, and even helps being brushed up with arrays in relation to images (as per pygame projects) 
# - since its basically the same interaction with numpy
# - and 
# - funnily enough, about contiguous arrays in google foobar


# -- functions --
# -- window cap --
def capture_window():
    """ uses win32 api for fastest possible window capture so the returned screencap can also be used for live botting commands """
    # -- initialise vars for window, screensize is for 1280 x 720 in bluestacks v10 --
    w = 1520 
    h = 750

    # -- get only the image data from the window we're interested in to significantly improve the performance --
    hwnd = win32gui.FindWindow(None, 'Max Performance') 

    # -- get the screenshot img data --
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0,0), (w, h), dcObj, (0,0), win32con.SRCCOPY)

    # -- disabled : save screenshot --
    want_save = False
    if want_save:
        dataBitMap.SaveBitmapFile(cDC, 'debug.bmp')

    # -- process the bitmap img to a useable image for opencv processing --
    signedIntsArray = dataBitMap.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (h, w, 4)

    # -- release resources --
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

    # -- drop the alpha channel for opencv matchTemplate --
    # -- note : theres a performance increase if matchTemplate is removed, to be fair matchTemplate not *entirely* needed so could remove this but leaving it in for now --
    img = img[..., :3] # use numpy slicing to get rid of the alpha channel data 
    img = np.ascontiguousarray(img) # slicing the alpha data from the bmp file data will cause errors when processing the file as an image, we can instead pass the image using numpy ascontgiousarray so we send a full image array instead of just a slice of the image data (with the alpha channel data missing)

    # -- return the screencap img --
    return img


# -- test main --
def main():
    # -- update working directory to the folder this file is in --
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # -- initialise performance timer --
    processing_timer = perf_counter()

    # -- loop until quit --
    while True:

        # -- get a full-screen screenshot -- 
        screenshot = capture_window()

        # -- convert our screenshot img to bgr from opencv --
        screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR) 

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