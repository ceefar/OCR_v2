# -- imports --
import win32ui
import win32gui
import win32con
import numpy as np


class WindowCap:
 
    # -- class constructor --
    def __init__(self, window_name):
        # in the case no Window Name is provided we'll instead just capture the entire screen (no additional functionality on top yet tho tbf)
        if window_name is None:
            self.hwnd = win32gui.GetDesktopWindow()
        else:
            # -- get only the image data from the window we're interested in to significantly improve the performance --
            self.hwnd = win32gui.FindWindow(None, window_name)
            # -- throws an exception if it cant find the window --
            if not self.hwnd:
                raise Exception(f"Window Not Found: {window_name}")

        # -- dynamically crop the size of our windowCap window to the size of the window_name window we are working with using the window rect to get the width and height --
        window_rect = win32gui.GetWindowRect(self.hwnd) # [0] and [1] = x upper left corner of window, y upper left - then - [2] and [3] =  bottom right, bottom right
        self.w = window_rect[2] - window_rect[0] # previously 1520
        self.h = window_rect[3] - window_rect[1] # previously 750

        # -- make small adjustments to the width, height, and the windows offset position so we only crop out the game window and not the bluestacks ui around the perimeter --
        x_offset = 32
        self.y_offset = 30
        self.w = self.w - x_offset
        self.h = self.h - self.y_offset

        # -- get the true coordinates, adjusted due to the bluestacks ui edge offset above so have more logical positions for window interactions --  
        self.true_x = window_rect[0] + x_offset
        self.true_y = window_rect[1] + self.y_offset


    def get_screencap(self):
        """ uses win32 api for fastest possible window capture so the returned screencap can also be used for live botting commands """

        # -- get the screenshot img data --
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0,0), (self.w, self.h), dcObj, (0, self.y_offset), win32con.SRCCOPY) # bit blit, aka bit block transfer, basically just like pygame lol thats so kewl

        # -- disabled : save screenshot, think this errors if you try to open the bitmap while the script is updating it btw, not using anyway so should just remove --
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


    def get_true_pos(self, pos): # legit this is exactly the same as it is in pygame winner winner as per the camera position which is SO awesome
        """ translate the position on the screenshot img to the true img based on any offset to the window 
        - note : this is not calculated dynamically only on initialising the window, so moving the client window after launch will return incorrect positions """
        return (pos[0] + self.true_x, pos[1] + self.true_y)


# -- driver --
if __name__ == "__main__":
    pass
