from PyQt6 import QtWidgets
from PyQt6.QtGui import QImage, QPixmap
import sys, cv2, threading, random

def closeEvent(self, event):
        self.ocv = False                # 關閉視窗時設定為 False

def op():
    print("123")
    
    
def opencv(self):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while self.ocv:
        ret, frame = cap.read()
        if not ret:
            print("Cannot receive frame")
            break
        frame = cv2.resize(frame, (300, 200))  # 使用變數
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channel = frame.shape
        bytesPerline = channel * width
        img = QImage(frame, width, height, bytesPerline, QImage.Format.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(img))
        
