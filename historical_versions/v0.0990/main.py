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

# -- initialise pytesseract for ocr --
pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe" # < required 

# -- ensure pyautogui failsafe is active --
pyautogui.FAILSAFE = True

# -- create a new instance of our screen capture class using the Max Performance window (which is the name of the Bluestacks game)
wincap = WindowCap('Max Performance')


# -- variables --
want_framerate = False

# -- functions -- 
def print_framerate():
    """ uses floating point format string to change decimal precision """
    current_time = perf_counter()
    print(f"FPS : {1 / (current_time - processing_timer):.2f}")
    processing_timer = perf_counter()


# -- main - loop until quit --
while True:

    # -- get game window screencap -- 
    screenshot = wincap.get_screencap()

    # -- print current frame rate for debugging --
    if want_framerate:
        print_framerate()







    # -- blit the current screencap --
    cv.imshow("Game Window", screenshot)
        
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break