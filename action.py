import win32con
import win32api
import pyautogui

class classAction(object):
    
    
    def volumeUp(self): # 電腦聲音+10
        n = 5
        while n:
            pyautogui.press('volumeup')
            n = n - 1  
        return

    def volumeDown(self): # 電腦聲音-10
        n = 5
        while n:
            pyautogui.press('volumedown')
            n = n - 1
        return

    def volume_mute(self): # 電腦靜音
        win32api.keybd_event(173, 0)
        win32api.keybd_event(173, 0, win32con.KEYEVENTF_KEYUP)
        return

    def mediaPause(self): # 音樂暫停
        win32api.keybd_event(179, 0)
        win32api.keybd_event(179, 0, win32con.KEYEVENTF_KEYUP)
        return

    def mediaNextTrack(self): # 音樂下一首
        win32api.keybd_event(win32con.VK_MEDIA_NEXT_TRACK, 0)
        win32api.keybd_event(win32con.VK_MEDIA_NEXT_TRACK, 0, win32con.KEYEVENTF_KEYUP)
        return

    def mediaPrevTrack(self): # 音樂上一首
        win32api.keybd_event(win32con.VK_MEDIA_PREV_TRACK, 0)
        win32api.keybd_event(win32con.VK_MEDIA_PREV_TRACK, 0, win32con.KEYEVENTF_KEYUP)
        return

    def previous_page(self): # Chrome下一頁
        pyautogui.hotkey('Alt', 'left') 
        return
    
    def next_page(self):# Chrome上一頁
        pyautogui.hotkey('Alt', 'right') 
        return
    
    def windowRollDown(self):
        pyautogui.scroll(-50)

    def windowRollUp(self):
        pyautogui.scroll(50)
    
    def screenshot():
        # 捕捉整個屏幕
        screenshot = pyautogui.screenshot()
        # 保存圖像到指定文件
        screenshot.save('螢幕截圖.png')