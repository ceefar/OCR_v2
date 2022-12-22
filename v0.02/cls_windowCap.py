# -- imports --
import win32ui
import win32gui
import win32con
import numpy as np

# -- notes -- 
# - as per this version screencap at around 30-35 fps on average, peaks at around 42, lowest around 25 (tho tbf one outliner 19)

class WindowCap:
    # -- class constructor --
    def __init__(self, window_name):

        # -- get only the image data from the window we're interested in to significantly improve the performance --
        self.hwnd = win32gui.FindWindow(None, window_name) 
        # -- throws an exception if it cant find the window --
        if not self.hwnd:
            raise Exception(f"Window Not Found: {window_name}")

        # -- define vars for window, screensize is for 1280 x 720 in bluestacks v10 --
        self.w = 1520 
        self.h = 750

    def get_screencap(self):
        """ uses win32 api for fastest possible window capture so the returned screencap can also be used for live botting commands """

        # -- get the screenshot img data --
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0,0), (self.w, self.h), dcObj, (0,0), win32con.SRCCOPY)

        # -- disabled : save screenshot --
        want_save = False
        if want_save:
            dataBitMap.SaveBitmapFile(cDC, 'debug.bmp')

        # -- process the bitmap img to a useable image for opencv processing --
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (self.h, self.w, 4)

        # -- release resources --
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        # -- drop the alpha channel for opencv matchTemplate --
        # -- note : theres a performance increase if matchTemplate is removed, to be fair matchTemplate not *entirely* needed so could remove this but leaving it in for now --
        img = img[..., :3] # use numpy slicing to get rid of the alpha channel data 
        img = np.ascontiguousarray(img) # slicing the alpha data from the bmp file data will cause errors when processing the file as an image, we can instead pass the image using numpy ascontgiousarray so we send a full image array instead of just a slice of the image data (with the alpha channel data missing)

        # -- return the screencap img --
        return img