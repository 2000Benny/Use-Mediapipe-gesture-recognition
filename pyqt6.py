from PyQt6 import QtWidgets
from PyQt6.QtGui import QImage, QPixmap,QMovie
from PyQt6.QtCore import Qt
import sys
import threading

import pyautogui
from camera6 import classCamera
from action import classAction
from PyQt6.QtCore import QTimer

import subprocess

class MyWidget(QtWidgets.QWidget):    # 建立 pyqtSignal 物件，傳遞字串格式內容
    def __init__(self):
        super().__init__()
        self.setWindowTitle('手勢控制')      # 設定視窗標題
        #self.resize(1080, 720)               # 設定視窗尺寸
        self.resize(680, 450) 
        self.setStyleSheet('background:rgb(126, 154, 230);')  # 使用網頁 CSS 樣式設定背景
        self.setUpdatesEnabled(True)#即時更新
        self.video = None ; self.judge = None
        self.control = classCamera() ; self.control2 = classAction()
        self.aa= None
        self.ui()
        self.control.signal.connect(self.signal)    # 建立插槽監聽信號
      
    
    def ui(self):
        # 建立 QTabWidget 物件
        self.tabs = QtWidgets.QTabWidget(self)
        self.tabs.setGeometry(self.rect())  # 設定 QTabWidget 的尺寸
        
        # 建立第一個頁面
        page1 = QtWidgets.QWidget()
        label = QtWidgets.QLabel(page1)          # 在 Form 裡加入 label
        label.move(50,50)                       # 移動到 (50, 50) 的位置
        label.setText('使用方法')            # 寫入文字
        label.setStyleSheet('font-size:30px; color:#00c')  # 設定樣式
                   
        page3 = QtWidgets.QWidget()
        self.label3 = QtWidgets.QLabel(page3); self.label3.setGeometry(360,10,500,500)  
        self.label_GIF =QtWidgets.QLabel(page3)  # 創建用於顯示GIF的 QLabel
        self.label_GIF.setGeometry(50, 50, 400, 400)                     
        options = ['No','volumeUp','volumeDown','mediaPause','mediaNextTrack','previous_page','next_page','windowRollDown','windowRollUp','自定義1','自定義2','自定義3']                       
        self.box_v1 = QtWidgets.QComboBox(page3) ; self.box_v1.addItems(options) ; self.box_v1.setGeometry(10,10,150,30);self.box_v1.setCurrentIndex(1);self.box_v1.currentIndexChanged.connect(self.display)
        self.button_v1 = QtWidgets.QPushButton('動作1',page3) ; self.button_v1.setGeometry(170,10,100,30);self.button_v1.clicked.connect(lambda:self.gif_choose(1))
        self.box_v2 = QtWidgets.QComboBox(page3) ; self.box_v2.addItems(options) ; self.box_v2.setGeometry(10,50,150,30);self.box_v2.setCurrentIndex(2);self.box_v2.currentIndexChanged.connect(self.display)
        self.button_v2 = QtWidgets.QPushButton('動作2',page3) ; self.button_v2.setGeometry(170,50,100,30);self.button_v2.clicked.connect(lambda:self.gif_choose(1))
        self.box_v3 = QtWidgets.QComboBox(page3) ; self.box_v3.addItems(options) ; self.box_v3.setGeometry(10,90,150,30);self.box_v3.setCurrentIndex(3);self.box_v3.currentIndexChanged.connect(self.display)
        self.button_v3 = QtWidgets.QPushButton('動作3',page3) ; self.button_v3.setGeometry(170,90,100,30);self.button_v3.clicked.connect(lambda:self.gif_choose(1))
        self.box_v4 = QtWidgets.QComboBox(page3) ; self.box_v4.addItems(options) ; self.box_v4.setGeometry(10,130,150,30);self.box_v4.setCurrentIndex(4);self.box_v4.currentIndexChanged.connect(self.display)
        self.button_v4 = QtWidgets.QPushButton('動作4',page3) ; self.button_v4.setGeometry(170,130,100,30);self.button_v4.clicked.connect(lambda:self.gif_choose(1))
        self.box_v5 = QtWidgets.QComboBox(page3) ; self.box_v5.addItems(options) ; self.box_v5.setGeometry(10,170,150,30);self.box_v5.setCurrentIndex(5);self.box_v5.currentIndexChanged.connect(self.display)
        self.button_v5 = QtWidgets.QPushButton('動作5',page3) ; self.button_v5.setGeometry(170,170,100,30);self.button_v5.clicked.connect(lambda:self.gif_choose(1))
        self.box_v6 = QtWidgets.QComboBox(page3) ; self.box_v6.addItems(options) ; self.box_v6.setGeometry(10,210,150,30);self.box_v6.setCurrentIndex(6);self.box_v6.currentIndexChanged.connect(self.display)
        self.button_v6 = QtWidgets.QPushButton('動作6',page3) ; self.button_v6.setGeometry(170,210,100,30);self.button_v6.clicked.connect(lambda:self.gif_choose(1))
        self.box_v7 = QtWidgets.QComboBox(page3) ; self.box_v7.addItems(options) ; self.box_v7.setGeometry(10,250,150,30);self.box_v7.setCurrentIndex(1);self.box_v7.currentIndexChanged.connect(self.display)
        self.button_v7 = QtWidgets.QPushButton('動作7',page3) ; self.button_v7.setGeometry(170,250,100,30);self.button_v7.clicked.connect(lambda:self.gif_choose(1))
        self.box_v8 = QtWidgets.QComboBox(page3) ; self.box_v8.addItems(options) ; self.box_v8.setGeometry(10,290,150,30);self.box_v8.setCurrentIndex(0);self.box_v8.currentIndexChanged.connect(self.display)
        self.button_v8 = QtWidgets.QPushButton('動作8',page3) ; self.button_v8.setGeometry(170,290,100,30);self.button_v8.clicked.connect(lambda:self.gif_choose(1))
        self.box_v9 = QtWidgets.QComboBox(page3) ; self.box_v9.addItems(options) ; self.box_v9.setGeometry(10,330,150,30);self.box_v9.setCurrentIndex(0);self.box_v9.currentIndexChanged.connect(self.display)
        self.button_v9 = QtWidgets.QPushButton('動作9',page3) ; self.button_v9.setGeometry(170,330,100,30);self.button_v9.clicked.connect(lambda:self.gif_choose(1))
        self.box_v10 = QtWidgets.QComboBox(page3) ; self.box_v10.addItems(options) ; self.box_v10.setGeometry(10,370,150,30);self.box_v10.setCurrentIndex(0);self.box_v10.currentIndexChanged.connect(self.display)
        self.button_v10 = QtWidgets.QPushButton('動作10',page3) ; self.button_v10.setGeometry(170,370,100,30);self.button_v10.clicked.connect(lambda:self.gif_choose(1))
        self.box_v11 = QtWidgets.QComboBox(page3) ; self.box_v11.addItems(options) ; self.box_v11.setGeometry(290,10,150,30);self.box_v11.setCurrentIndex(0);self.box_v11.currentIndexChanged.connect(self.display)
        self.button_v11 = QtWidgets.QPushButton('動作11',page3) ; self.button_v11.setGeometry(490,10,100,30);self.button_v11.clicked.connect(lambda:self.gif_choose(1))
        self.box_v12 = QtWidgets.QComboBox(page3) ; self.box_v12.addItems(options) ; self.box_v12.setGeometry(290,50,150,30);self.box_v12.setCurrentIndex(0);self.box_v12.currentIndexChanged.connect(self.display)
        self.button_v12 = QtWidgets.QPushButton('動作12',page3) ; self.button_v12.setGeometry(490,50,100,30);self.button_v12.clicked.connect(lambda:self.gif_choose(1))
        self.box_v13 = QtWidgets.QComboBox(page3) ; self.box_v13.addItems(options) ; self.box_v13.setGeometry(290,90,150,30);self.box_v13.setCurrentIndex(0);self.box_v13.currentIndexChanged.connect(self.display)
        self.button_v13 = QtWidgets.QPushButton('動作13',page3) ; self.button_v13.setGeometry(490,90,100,30);self.button_v13.clicked.connect(lambda:self.gif_choose(1))
        self.box_v14 = QtWidgets.QComboBox(page3) ; self.box_v14.addItems(options) ; self.box_v14.setGeometry(290,130,150,30);self.box_v14.setCurrentIndex(0);self.box_v14.currentIndexChanged.connect(self.display)
        self.button_v14 = QtWidgets.QPushButton('動作14',page3) ; self.button_v14.setGeometry(490,130,100,30);self.button_v14.clicked.connect(lambda:self.gif_choose(1))
        self.box_v15 = QtWidgets.QComboBox(page3) ; self.box_v15.addItems(options) ; self.box_v15.setGeometry(290,170,150,30);self.box_v15.setCurrentIndex(0);self.box_v15.currentIndexChanged.connect(self.display)
        self.button_v15 = QtWidgets.QPushButton('動作15',page3) ; self.button_v15.setGeometry(490,170,100,30);self.button_v15.clicked.connect(lambda:self.gif_choose(1))
        self.box_v16 = QtWidgets.QComboBox(page3) ; self.box_v16.addItems(options) ; self.box_v16.setGeometry(290,210,150,30);self.box_v16.setCurrentIndex(0);self.box_v16.currentIndexChanged.connect(self.display)
        self.button_v16 = QtWidgets.QPushButton('動作16',page3) ; self.button_v16.setGeometry(490,210,100,30);self.button_v16.clicked.connect(lambda:self.gif_choose(1))
        self.box_v17 = QtWidgets.QComboBox(page3) ; self.box_v17.addItems(options) ; self.box_v17.setGeometry(290,250,150,30);self.box_v17.setCurrentIndex(0);self.box_v17.currentIndexChanged.connect(self.display)
        self.button_v17 = QtWidgets.QPushButton('動作17',page3) ; self.button_v17.setGeometry(490,250,100,30);self.button_v17.clicked.connect(lambda:self.gif_choose(1))
        self.box_v18 = QtWidgets.QComboBox(page3) ; self.box_v18.addItems(options) ; self.box_v18.setGeometry(290,290,150,30);self.box_v18.setCurrentIndex(0);self.box_v18.currentIndexChanged.connect(self.display)
        self.button_v18 = QtWidgets.QPushButton('動作18',page3) ; self.button_v18.setGeometry(490,290,100,30);self.button_v18.clicked.connect(lambda:self.gif_choose(1))
        self.box_v19 = QtWidgets.QComboBox(page3) ; self.box_v19.addItems(options) ; self.box_v19.setGeometry(290,330,150,30);self.box_v19.setCurrentIndex(0);self.box_v19.currentIndexChanged.connect(self.display)
        self.button_v19 = QtWidgets.QPushButton('動作19',page3) ; self.button_v19.setGeometry(490,330,100,30);self.button_v19.clicked.connect(lambda:self.gif_choose(1))
        self.box_v20 = QtWidgets.QComboBox(page3) ; self.box_v20.addItems(options) ; self.box_v20.setGeometry(290,370,150,30);self.box_v20.setCurrentIndex(0);self.box_v20.currentIndexChanged.connect(self.display)
        self.button_v20 = QtWidgets.QPushButton('動作20',page3) ; self.button_v20.setGeometry(490,370,100,30);self.button_v20.clicked.connect(lambda:self.gif_choose(1))
        
        self.box_style=('''
            QComboBox {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                background-color: white;
                color: black;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #ccc;
                border-left-style: solid;
                border-top-right-radius: 5px;
                border-bottom-right-radius: 5px;
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #f6f6f6, stop:1 #e0e0e0);
            }
            QComboBox::down-arrow {
                image: url(arrow_down.png);
            }
            QListView {
                background-color: white;
                border: 1px solid #ccc;
                selection-background-color: #e0e0e0;
            }
            ''')
        box_inputs = [self.box_v1,self.box_v2,self.box_v3,self.box_v4,self.box_v5,self.box_v6,self.box_v7,self.box_v8,self.box_v9,self.box_v10,self.box_v11,self.box_v12,self.box_v13,self.box_v14,self.box_v15,self.box_v16,self.box_v17,self.box_v18,self.box_v19,self.box_v20]
        for input in box_inputs:
            input.setStyleSheet(self.box_style)
        # 建立第二個頁面
        page2 = QtWidgets.QWidget()
        label2 = QtWidgets.QLabel(page2)
        label2.setGeometry(10,30,550,340)
        self.control.label=label2
        self.label2 = QtWidgets.QLabel('模式',page2);self.label2.setGeometry(10,10,100,30)
        button = QtWidgets.QPushButton('開始',page2);button.move(550,370)
        button.clicked.connect(self.on_button_clicked);button.clicked.connect(self.on_button_clicked1)
        
        page4 = QtWidgets.QWidget()
        label4 = QtWidgets.QLabel(page4)
        self.label4_1 = QtWidgets.QLabel('自定義1',page4) ; self.label4_1.setGeometry(20,50,100,20)
        self.label4_2 = QtWidgets.QLabel('自定義2',page4) ; self.label4_2.setGeometry(20,80,100,20)
        self.label4_3 = QtWidgets.QLabel('自定義3',page4) ; self.label4_3.setGeometry(20,110,100,20)
        self.label4_4 = QtWidgets.QLabel('自定義4',page4) ; self.label4_4.setGeometry(20,140,100,20)
        self.input1_1 = QtWidgets.QLineEdit(page4) ; self.input1_1.setGeometry(80,50,100,20)
        self.input1_2 = QtWidgets.QLineEdit(page4) ; self.input1_2.setGeometry(190,50,100,20)
        self.input2_1 = QtWidgets.QLineEdit(page4) ; self.input2_1.setGeometry(80,80,100,20)
        self.input2_2 = QtWidgets.QLineEdit(page4) ; self.input2_2.setGeometry(190,80,100,20)
        self.input3_1 = QtWidgets.QLineEdit(page4) ; self.input3_1.setGeometry(80,110,100,20)
        self.input3_2 = QtWidgets.QLineEdit(page4) ; self.input3_2.setGeometry(190,110,100,20)
        self.input4_1 = QtWidgets.QLineEdit(page4) ; self.input4_1.setGeometry(80,140,210,20)
        button111 = QtWidgets.QPushButton('存入',page4);button111.move(250,170)
        button111.clicked.connect(self.custom)
        
        common_style=('''
            QLineEdit {
                background-color: #f2f2f2;
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 4px;
                font-size: 14px;
                color: #333333;
            }
            QLineEdit:hover {
                border: 1px solid #999999;
            }
            QLineEdit:focus {
                border: 1px solid #0078d7;
                outline: none;
            }
            ''')
        text_inputs = [self.input1_1, self.input1_2, self.input2_1, self.input2_2, self.input3_1, self.input3_2 , self.input4_1]
        for input in text_inputs:
            input.setStyleSheet(common_style)

        button_style=('''
            QPushButton {
                background:#fff;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #367c3b;
            }
            ''')
        button_inputs = [self.button_v1, self.button_v2, self.button_v3, self.button_v4, self.button_v5, self.button_v6, self.button_v7, self.button_v8, self.button_v9, self.button_v10, self.button_v11, self.button_v12, self.button_v13, self.button_v14, self.button_v15, self.button_v16, self.button_v17, self.button_v18, self.button_v19, self.button_v20,button111 ]
        for input in button_inputs:
            input.setStyleSheet(button_style)

        self.tabs.addTab(page1, '使用方法')
        self.tabs.addTab(page3, '選單')
        self.tabs.addTab(page2, '鏡頭')
        self.tabs.addTab(page4, '自定義')
    def gif_choose(self,num):
        index = num
        movie = None
        if index==1:
            movie = QMovie('umamusumeprettyderby.gif')
        elif index==2:
            movie = QMovie('umamusumeprettyderby (1).gif')
        else:
            pass
        if movie:
            self.label_GIF.setMovie(movie);self.label_GIF.raise_();movie.start() 
            # 使用 QTimer 設置兩秒後結束照片顯示
            timer = QTimer(self)
            timer.singleShot(2000, self.end_GIF_display)
    def custom(self):
        self.A=self.input1_1.text()
        self.B=self.input1_2.text()
        pyautogui.hotkey(self.A,self.B)
        self.C=self.input4_1.text()
        subprocess.Popen(['start', self.C], shell=True)
    def end_GIF_display(self):
        self.label_GIF.clear()  # 清除照片
        self.label_GIF.lower()  # 將照片 QLabel 降低到最下層
    def on_button_clicked(self):
        self.video = threading.Thread(target=self.control.camera)
        self.video.start()
    def on_button_clicked1(self):
        self.judge = threading.Thread(target=self.control.judge)
        self.judge.start()
    def closeEvent(self, event):
        self.control.model='end'
        event.accept()
    def display(self):
        pass
        #self.label3_1.setText(self.box1.currentText())
        #self.label3_2.setText(self.box2.currentText())
        #self.label3_3.setText(self.box3.currentText())
        #self.label3_4.setText(self.box4.currentText())
        #self.label3_5.setText(self.box5.currentText())
        #self.label3_6.setText(self.box6.currentText())
    def signal(self, message):
        if message=='11':
            self.choose=self.box1.currentText();self.label2.setText(self.choose);self.action()
        elif message=='12':
            self.choose=self.box2.currentText();self.label2.setText(self.choose);self.action()
        elif message=='v5':
            self.choose=self.box3.currentText();self.label2.setText(self.choose);self.action()
        elif message=='v6':
            self.choose=self.box4.currentText();self.label2.setText(self.choose);self.action()
        elif message=='51':
            self.choose=self.box5.currentText();self.label2.setText(self.choose);self.action()
        elif message=='52':
            self.choose=self.box6.currentText();self.label2.setText(self.choose);self.action()
        elif message=='v1':
            self.choose=self.box7.currentText();self.label2.setText(self.choose);self.action()
        elif message=='v2':
            self.choose=self.box8.currentText();self.label2.setText(self.choose);self.action()         
    def action (self): 
        if self.choose=='volumeUp':
            self.control2.mediaNextTrack()
        elif self.choose=='volumeDown':
            self.control2.mediaPrevTrack()
        elif self.choose=='mediaPause':
            self.control2.mediaPause()
            print("123")
        elif self.choose=='mediaNextTrack':
            self.control2.mediaNextTrack()
            print("123")
        elif self.choose=='previous_page':
            self.control2.previous_page()
        elif self.choose=='next_page':
            self.control2.next_page()
        elif self.choose=='windowRollUp':
            self.control2.windowRollUp()
        elif self.choose=='windowRollDown':
            self.control2.windowRollDown()
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Form = MyWidget()
    Form.show()
    sys.exit(app.exec())