import win32gui
import win32con
import win32api
import time
import configparser


# subprocess.Popen("start msedge", shell=True) ## 開啟edge

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')
volumeDefault = int(config['volumeV']['volumeV'])
windowNameDefault = config['window']['nameDefault']
rollDefault = int(config['window']['roll'])

hwnd = win32gui.FindWindow(None, windowNameDefault)


def windowMinimize():
    win32gui.ShowWindow(hwnd, win32con.SW_FORCEMINIMIZE)


def windowMaximize():
    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)


def windowBackToscreen():
    win32gui.ShowWindow(hwnd, win32con.SW_NORMAL)
    # win32gui.SetForegroundWindow(hwnd)


def windowRollDown():
    n = 5
    while n:
        win32api.keybd_event(win32con.VK_DOWN, 0)
        win32api.keybd_event(win32con.VK_DOWN, 0, win32con.KEYEVENTF_KEYUP)
        n = n - 1
    return

def windowRollUp():
    n = 5
    while n:
        win32api.keybd_event(win32con.VK_UP, 0)
        win32api.keybd_event(win32con.VK_UP, 0, win32con.KEYEVENTF_KEYUP)
        n = n - 1
    return
'''
    def window_show():
    win32api.keybd_event(13, 0, 0, 0)
    win32gui.SetForegroundWindow(hwnd)

'''
# #win32gui.SetWindowLong (hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong (hwnd, win32con.GWL_EXSTYLE ) |
# win32con.WS_EX_LAYERED ) #winxpgui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0,0,0), 255, win32con.LWA_ALPHA)
# ## 中間的30是透明度，數字越小越淺，可以自由更改


def volumeUp():
    n = volumeDefault
    while n:
        win32api.keybd_event(win32con.VK_VOLUME_UP, 0)
        win32api.keybd_event(win32con.VK_VOLUME_UP, 0, win32con.KEYEVENTF_KEYUP)
        n = n - 1
    return


def volumeDown():
    n = volumeDefault
    while n:
        win32api.keybd_event(win32con.VK_VOLUME_DOWN, 0)
        win32api.keybd_event(win32con.VK_VOLUME_DOWN, 0, win32con.KEYEVENTF_KEYUP)
        n = n - 1
    return


def mediaPause():
    win32api.keybd_event(179, 0)
    win32api.keybd_event(179, 0, win32con.KEYEVENTF_KEYUP)
    return


def mediaNextTrack():
    win32api.keybd_event(win32con.VK_MEDIA_NEXT_TRACK, 0)
    win32api.keybd_event(win32con.VK_MEDIA_NEXT_TRACK, 0, win32con.KEYEVENTF_KEYUP)
    return


def mediaPrevTrack():
    win32api.keybd_event(win32con.VK_MEDIA_PREV_TRACK, 0)
    win32api.keybd_event(win32con.VK_MEDIA_PREV_TRACK, 0, win32con.KEYEVENTF_KEYUP)
    return


def volume_mute():
    win32api.keybd_event(173, 0)
    win32api.keybd_event(173, 0, win32con.KEYEVENTF_KEYUP)
    return
