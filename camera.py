import cv2
import mediapipe as mp
import math
import time
import threading
from PyQt6.QtGui import QImage,QPixmap      
from PyQt6 import QtWidgets
from PyQt6.QtCore import pyqtSignal

class classCamera(QtWidgets.QWidget):
    
    signal = pyqtSignal(str)      # 建立 pyqtSignal 物件，傳遞字串格式內容
    
    def __init__(self):
        super().__init__()
        self.img=None; self.imgRGB=None;self.label = None
        self.pTime = 0 ; self.cTime = 0 #抓取fps時要用
        self.model=None ;self.new_x=self.new_y=None ;self.t= 0
        self.x8 =self.x5 =self.x17= self.y8 =self.y5 =self.y17 = None
        self.f1 =self.f2 = self.f3 = self.f4 = self.f5 = None
        self.cap = cv2.VideoCapture(0)            # 讀取攝影機
        self.fontFace = cv2.FONT_HERSHEY_SIMPLEX  # 印出文字的字型
        self.lineType = cv2.LINE_AA               # 印出文字的邊框
        self.mp_hands = mp.solutions.hands   # mediapipe 偵測手掌方法
        self.mp_drawing = mp.solutions.drawing_utils    # mediapipe 抓21節點
        
    def angle(self,v1, v2):  # 根據兩點的座標，計算角度
        v1_x = v1[0] ; v1_y = v1[1]
        v2_x = v2[0] ; v2_y = v2[1]
        try:
            angle_= math.degrees(math.acos((v1_x*v2_x+v1_y*v2_y)/(((v1_x**2+v1_y**2)**0.5)*((v2_x**2+v2_y**2)**0.5))))
        except:
            angle_ = 180
        return angle_

    def hand_angle(self,hand_):# 根據傳入的 21 個節點座標，得到該手指的角度
        """### 靜態手勢"""
        angle_list = []
        # thumb 大拇指角度
        angle_ = self.angle(((int(hand_[0][0])- int(hand_[2][0])),(int(hand_[0][1])-int(hand_[2][1]))),((int(hand_[3][0])- int(hand_[4][0])),(int(hand_[3][1])- int(hand_[4][1]))) )
        angle_list.append(angle_)
        # index 食指角度
        angle_ = self.angle(((int(hand_[0][0])-int(hand_[6][0])),(int(hand_[0][1])- int(hand_[6][1]))),((int(hand_[7][0])- int(hand_[8][0])),(int(hand_[7][1])- int(hand_[8][1]))) )
        angle_list.append(angle_)
        # middle 中指角度
        angle_ = self.angle(((int(hand_[0][0])- int(hand_[10][0])),(int(hand_[0][1])- int(hand_[10][1]))),((int(hand_[11][0])- int(hand_[12][0])),(int(hand_[11][1])- int(hand_[12][1]))))
        angle_list.append(angle_)
        # ring 無名指角度
        angle_ = self.angle(((int(hand_[0][0])- int(hand_[14][0])),(int(hand_[0][1])- int(hand_[14][1]))),((int(hand_[15][0])- int(hand_[16][0])),(int(hand_[15][1])- int(hand_[16][1]))))
        angle_list.append(angle_)
        # pink 小拇指角度
        angle_ = self.angle(((int(hand_[0][0])- int(hand_[18][0])),(int(hand_[0][1])- int(hand_[18][1]))),((int(hand_[19][0])- int(hand_[20][0])),(int(hand_[19][1])- int(hand_[20][1])))  )
        angle_list.append(angle_)
        return angle_list

    def hand_pos(self,finger_angle):
        """### 手指的角度"""
        self.f1 = finger_angle[0]   # 大拇指角度
        self.f2 = finger_angle[1]   # 食指角度
        self.f3 = finger_angle[2]   # 中指角度
        self.f4 = finger_angle[3]   # 無名指角度
        self.f5 = finger_angle[4]   # 小拇指角度

        # 小於 50 表示手指伸直，大於等於 50 表示手指捲縮
        if   self.f2>=50 and self.f3>=50 and self.f4>=50 and self.f5>=50:
            return '0'
        elif self.f2<50 and self.f3>=50 and self.f4>=50 and self.f5>=50:
            return '1'
        elif self.f2<50 and self.f3<50 and self.f4<50 and self.f5<50:
            return '5'
        else:
            return ''

    def camera(self):# mediapipe 啟用偵測手掌
        """### 開啟相機"""
        hands=self.mp_hands.Hands(
        static_image_mode=False,
        model_complexity=0,
        max_num_hands=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5)
                                        
        while self.model != 'end':
            ret, self.img = self.cap.read()
            w, h = 540, 310 
            centerX=270 ; centerY=155
            if ret:
                self.img = cv2.resize(self.img, (w,h))  # 影像尺寸
                self.imgRGB = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)  # 轉換成 RGB
                results = hands.process(self.imgRGB)
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        self.mp_drawing.draw_landmarks(self.img,hand_landmarks,self.mp_hands.HAND_CONNECTIONS) # 將節點和骨架繪製到影像中
                        finger_coordinate = []                   # 記錄手指節點座標的串列
                        for i in hand_landmarks.landmark:
                            # 將 21 個節點換算成座標，記錄到 finger_coordinate
                            x = i.x*w    ;   y = i.y*h      ; finger_coordinate.append((x,y))
                            
                            self.x8 = hand_landmarks.landmark[8].x * w   ; self.y8 = hand_landmarks.landmark[8].y * h
                            self.x5 = hand_landmarks.landmark[5].x * w   ; self.y5 = hand_landmarks.landmark[5].y * h
                            self.x17 = hand_landmarks.landmark[17].x * w ; self.y17 = hand_landmarks.landmark[17].y * h
                            
                        if finger_coordinate:
                            finger_angle = self.hand_angle(finger_coordinate) # 計算手指角度，回傳長度為 5 的串列
                            #print(finger_angle)                     # 印出角度 ( 有需要就開啟註解 )
                            text = self.hand_pos(finger_angle)            # 取得手勢所回傳的內容
                            
                            if centerX-100<self.x5<centerX+100 and centerX-100<self.x17<centerX+100 and centerY-100<self.y5<centerY+100 and centerY-100<self.y17<centerY+100 and self.model==None:
                                self.model= text
                                if self.new_x == self.new_y== None:
                                    self.new_x = self.x8
                                    self.new_y = self.y8
                                    print(self.model)
                                # cv2.putText(self.img, text, (30,120), fontFace, 3, (255,255,255), 10, lineType) # 印出文字    
                        # print (finger_coordinate)
            
            self.cTime = time.time()
            fps = 1/(self.cTime-self.pTime)
            self.pTime = self.cTime
            cv2.putText(self.img, f"FPS : {int(fps)}", (130, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
            centerX , centerY = w//2 , h//2
            cv2.rectangle(self.img,(centerX-100,centerY-100),(centerX+100,centerY+100),(0,0,255),2)   # 畫出中間
            #cv2.imshow('camera', self.img)
            self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
            height, width, channel = self.img.shape
            bytesPerline = channel * width
            self.img = QImage(self.img, width, height, bytesPerline, QImage.Format.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(self.img))
            
            cv2.waitKey(1) 
        self.cap.release()
        cv2.destroyAllWindows()
    
    def judge(self):
        """### 手勢判別"""
        while self.model != 'end':
            time.sleep(0.1)
            while self.model == '1' and self.t!=10:
                time.sleep(0.1)
                if self.x5 >= self.x17:#右
                    if self.x8 < self.new_x - 100:#右
                        self.signal.emit('v1')
                        time.sleep(0.5);print("請選擇模式");self.model = self.new_x = self.new_y= None;self.t=0;break
                    elif self.x8 > self.new_x + 100:
                        self.signal.emit('v2')
                        time.sleep(0.5);print("請選擇模式");self.model = self.new_x = self.new_y= None;self.t=0;break
                    elif self.y8 < self.new_y - 100:#上
                        self.signal.emit('v3')
                        time.sleep(0.5);print("請選擇模式");self.model = self.new_x = self.new_y= None;self.t=0;break
                    elif self.y8 > self.new_y + 100:
                        self.signal.emit('v4')
                        time.sleep(0.5);print("請選擇模式");self.model = self.new_x = self.new_y= None;self.t=0;break
                    else:
                        self.t=self.t+1
                        time.sleep(0.5)
                else:#左
                    if self.x8 < self.new_x - 100:
                        self.signal.emit('v11')
                        print("左手")
                        time.sleep(0.5);print("請選擇模式");self.model = self.new_x = self.new_y= None;self.t=0;break
                    elif self.x8 > self.new_x + 100:
                        self.signal.emit('v12')
                        time.sleep(0.5);print("請選擇模式");self.model = self.new_x = self.new_y= None;self.t=0;break
                    elif self.y8 < self.new_y - 100:
                        self.signal.emit('v13')
                        time.sleep(0.5);print("請選擇模式");self.model = self.new_x = self.new_y= None;self.t=0;break
                    elif self.y8 > self.new_y + 100:
                        self.signal.emit('v14')
                        time.sleep(0.5);print("請選擇模式");self.model = self.new_x = self.new_y= None;self.t=0;break
                    else:
                        self.t=self.t+1
                        time.sleep(0.5)            
            while self.model == '5' and self.t!=10:
                time.sleep(0.1)
                if self.x5 >= self.x17:
                    if self.x8 < self.new_x - 100:
                        self.signal.emit('v5')
                        time.sleep(0.5);print("請選擇模式");self.model = self.new_x = self.new_y= None;self.t=0;break
                    elif self.x8 > self.new_x + 100:
                        self.signal.emit('v6')
                        time.sleep(0.5);print("請選擇模式");self.model = self.new_x = self.new_y= None;self.t=0;break
                    elif self.y8 < self.new_y - 100:
                        self.signal.emit('v7')
                        time.sleep(0.5);print("請選擇模式");self.model = self.new_x = self.new_y= None;self.t=0;break
                    elif self.y8 > self.new_y + 100:
                        self.signal.emit('v8')
                        time.sleep(0.5);print("請選擇模式");self.model = self.new_x = self.new_y= None;self.t=0;break
                    elif self.f2>=50 and self.f3>=50 and self.f4>=50 and self.f5>=50:
                        self.signal.emit('v9')
                        time.sleep(0.5);print("請選擇模式");self.model = self.new_x = self.new_y= None;self.t=0;break
                    else:
                        self.t=self.t+1
                        time.sleep(0.5)
                else:
                    if self.x8 < self.new_x - 100:
                        self.signal.emit('v15')
                        time.sleep(0.5);print("請選擇模式");self.model = self.new_x = self.new_y= None;self.t=0;break
                    elif self.x8 > self.new_x + 100:
                        self.signal.emit('v16')
                        time.sleep(0.5);print("請選擇模式");self.model = self.new_x = self.new_y= None;self.t=0;break
                    elif self.y8 < self.new_y - 100:
                        self.signal.emit('v17')
                        time.sleep(0.5);print("請選擇模式");self.model = self.new_x = self.new_y= None;self.t=0;break
                    elif self.y8 > self.new_y + 100:
                        self.signal.emit('v18')
                        time.sleep(0.5);print("請選擇模式");self.model = self.new_x = self.new_y= None;self.t=0;break
                    elif self.f2>=50 and self.f3>=50 and self.f4>=50 and self.f5>=50:
                        self.signal.emit('v19')
                        time.sleep(0.5);print("請選擇模式");self.model = self.new_x = self.new_y= None;self.t=0;break
                    else:
                        self.t=self.t+1
                        time.sleep(0.5)            
            while self.model == '0' and self.t!=10 :
                time.sleep(0.1)
                if self.x5 >= self.x17:
                    if self.f2<50 and self.f3<50 and self.f4<50 and self.f5<50:
                        self.signal.emit('v10')
                        time.sleep(0.5);print("請選擇模式");self.model = self.new_x = self.new_y= None;self.t=0;break
                    else:
                        self.t=self.t+1
                        time.sleep(0.5)
                else:
                    if self.f2<50 and self.f3<50 and self.f4<50 and self.f5<50:
                        self.signal.emit('v20')
                        time.sleep(0.5);print("請選擇模式");self.model = self.new_x = self.new_y= None;self.t=0;break
                    else:
                        self.t=self.t+1
                        time.sleep(0.5)
            if self.model != 'end':
                self.model = self.new_x = self.new_y= None;self.t=0    
if __name__ == '__main__':

   start=classCamera() 
   video = threading.Thread(target=start.judge)
   video.start()
   start.camera()
   
   