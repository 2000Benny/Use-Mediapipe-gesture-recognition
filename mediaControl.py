import win32con
import win32api
import time


def volumeUp():
    n = 5
    while n:
        win32api.keybd_event(win32con.VK_VOLUME_UP, 0)
        win32api.keybd_event(win32con.VK_VOLUME_UP, 0, win32con.KEYEVENTF_KEYUP)
        n = n - 1
    return


def volumeDown():
    n = 5
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



