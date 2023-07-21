from PyQt6 import QtWidgets
from PyQt6.QtGui import  QPixmap,QMovie
from PyQt6.QtCore import Qt, QPoint
import sys
import threading

import pyautogui
from camera import classCamera
from action import classAction
from PyQt6.QtCore import QTimer

import subprocess
import os

class MyWidget(QtWidgets.QWidget):    
    
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100,750, 500)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        
        self.title_bar = QtWidgets.QFrame(self)
        self.title_bar.setObjectName("title_bar")
        self.title_bar.setGeometry(0, 0, self.width(), 30)
        # 在標題欄部件中添加文本
        self.title_label = QtWidgets.QLabel("手 勢 控 制 電 腦", self.title_bar)
        self.title_label.setObjectName("title_label")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)#對齊
        self.title_label.setGeometry(0, 0, self.width(), 30)
        self.title_label.setStyleSheet("font-family: DFKai-sb;font-size: 16px")
        # 在右上方新增一个關閉按钮
        self.close_button = QtWidgets.QPushButton("關閉", self.title_bar)
        self.close_button.setGeometry(self.width() - 50, 0, 50, 30)
        self.close_button.clicked.connect(self.close)
        self.close_button.setStyleSheet("QPushButton {"
                                        "   font-family: DFKai-sb;"
                                        "   font-size: 16px;"
                                        "}"
                                        "QPushButton:hover {"
                                        "   background-color: #cf4848;"
                                        "}")
        # 創建最小化按鈕
        self.minimize_button = QtWidgets.QPushButton("最小化", self.title_bar)
        self.minimize_button.setGeometry(self.width() - 130, 0, 80, 30)
        self.minimize_button.clicked.connect(self.minimizeWindow)
        self.minimize_button.setStyleSheet("QPushButton {"
                                        "   font-family: DFKai-sb;"
                                        "   font-size: 16px;"
                                        "}"
                                        "QPushButton:hover {"
                                        "   background-color: #cf4848;"
                                        "}")
        
        self.setUpdatesEnabled(True)#即時更新
        self.video = None ; self.judge = None
        self.control = classCamera() ; self.control_Action = classAction()
        self.aa= None
        
        self.load_user()
        self.ui()
        self.control.signal.connect(self.signal)    # 建立插槽監聽信號
      
        self.load_text()
        self.boxes = [self.box_v1, self.box_v2, self.box_v3, self.box_v4, self.box_v5, 
                      self.box_v6, self.box_v7, self.box_v8, self.box_v9, self.box_v10, 
                      self.box_v11, self.box_v12, self.box_v13, self.box_v14, self.box_v15, 
                      self.box_v16, self.box_v17, self.box_v18, self.box_v19, self.box_v20]
        self.load_comboboxes()
        self.custom()
        
    
        
        self.second_page = None
        
    def ui(self):
        # 建立 QTabWidget 物件
        self.tabs = QtWidgets.QTabWidget(self)
        self.tabs.setGeometry(0, 30, self.width(), self.height() - 30)
        
        # 建立第一個頁面
        page1 = QtWidgets.QWidget()
        page1.setObjectName("page")
        label_1 = QtWidgets.QLabel(page1)          # 在 Form 裡加入 label
        label_1.move(30,30)                       # 移動到 (50, 50) 的位置
        label_1.setText('為了防止誤判<br>請將手移動至紅色的方框內才會開始辨識')            # 寫入文字
        label_1.setStyleSheet('font-size:20px; color:#00c')  # 設定樣式
        label = QtWidgets.QLabel(page1)
        label.move(150,100)
        pixmap = QPixmap("help.png")
        label.setPixmap(pixmap)
                   
        page2 = QtWidgets.QWidget()
        page2.setObjectName("page")
        self.label3 = QtWidgets.QLabel(page2); self.label3.setGeometry(360,10,500,500)  
        self.label_GIF =QtWidgets.QLabel(page2)  # 創建用於顯示GIF的 QLabel
        self.label_GIF.setGeometry(50, 50, 540, 310)
        self.label_GIF.setStyleSheet("border-radius: 23px")                     
        self.options = ['No','volumeUp','volumeDown','volume_mute','mediaPause','mediaNextTrack','previous_page','next_page','windowRollDown','windowRollUp','screenshot','自定義1','自定義2','自定義3','自定義4','自定義5','自定義6','自定義7','自定義8','自定義路徑1','自定義路徑2','自定義路徑3','自定義路徑4','自定義網址1','自定義網址2','自定義網址3','自定義網址4']                       
        self.box_v1 = QtWidgets.QComboBox(page2) ; self.box_v1.addItems(self.options) ; self.box_v1.setGeometry(10,10,150,30);self.box_v1.currentIndexChanged.connect(self.save_comboboxes)
        self.button_v1 = QtWidgets.QPushButton('動作1',page2) ; self.button_v1.setGeometry(190,10,100,30);self.button_v1.clicked.connect(lambda:self.gif_choose(1))
        self.box_v2 = QtWidgets.QComboBox(page2) ; self.box_v2.addItems(self.options) ; self.box_v2.setGeometry(10,50,150,30);self.box_v2.currentIndexChanged.connect(self.save_comboboxes)
        self.button_v2 = QtWidgets.QPushButton('動作2',page2) ; self.button_v2.setGeometry(190,50,100,30);self.button_v2.clicked.connect(lambda:self.gif_choose(2))
        self.box_v3 = QtWidgets.QComboBox(page2) ; self.box_v3.addItems(self.options) ; self.box_v3.setGeometry(10,90,150,30);self.box_v3.currentIndexChanged.connect(self.save_comboboxes)
        self.button_v3 = QtWidgets.QPushButton('動作3',page2) ; self.button_v3.setGeometry(190,90,100,30);self.button_v3.clicked.connect(lambda:self.gif_choose(3))
        self.box_v4 = QtWidgets.QComboBox(page2) ; self.box_v4.addItems(self.options) ; self.box_v4.setGeometry(10,130,150,30);self.box_v4.currentIndexChanged.connect(self.save_comboboxes)
        self.button_v4 = QtWidgets.QPushButton('動作4',page2) ; self.button_v4.setGeometry(190,130,100,30);self.button_v4.clicked.connect(lambda:self.gif_choose(4))
        self.box_v5 = QtWidgets.QComboBox(page2) ; self.box_v5.addItems(self.options) ; self.box_v5.setGeometry(10,170,150,30);self.box_v5.currentIndexChanged.connect(self.save_comboboxes)
        self.button_v5 = QtWidgets.QPushButton('動作5',page2) ; self.button_v5.setGeometry(190,170,100,30);self.button_v5.clicked.connect(lambda:self.gif_choose(5))
        self.box_v6 = QtWidgets.QComboBox(page2) ; self.box_v6.addItems(self.options) ; self.box_v6.setGeometry(10,210,150,30);self.box_v6.currentIndexChanged.connect(self.save_comboboxes)
        self.button_v6 = QtWidgets.QPushButton('動作6',page2) ; self.button_v6.setGeometry(190,210,100,30);self.button_v6.clicked.connect(lambda:self.gif_choose(6))
        self.box_v7 = QtWidgets.QComboBox(page2) ; self.box_v7.addItems(self.options) ; self.box_v7.setGeometry(10,250,150,30);self.box_v7.currentIndexChanged.connect(self.save_comboboxes)
        self.button_v7 = QtWidgets.QPushButton('動作7',page2) ; self.button_v7.setGeometry(190,250,100,30);self.button_v7.clicked.connect(lambda:self.gif_choose(7))
        self.box_v8 = QtWidgets.QComboBox(page2) ; self.box_v8.addItems(self.options) ; self.box_v8.setGeometry(10,290,150,30);self.box_v8.currentIndexChanged.connect(self.save_comboboxes)
        self.button_v8 = QtWidgets.QPushButton('動作8',page2) ; self.button_v8.setGeometry(190,290,100,30);self.button_v8.clicked.connect(lambda:self.gif_choose(8))
        self.box_v9 = QtWidgets.QComboBox(page2) ; self.box_v9.addItems(self.options) ; self.box_v9.setGeometry(10,330,150,30);self.box_v9.currentIndexChanged.connect(self.save_comboboxes)
        self.button_v9 = QtWidgets.QPushButton('動作9',page2) ; self.button_v9.setGeometry(190,330,100,30);self.button_v9.clicked.connect(lambda:self.gif_choose(9))
        self.box_v10 = QtWidgets.QComboBox(page2) ; self.box_v10.addItems(self.options) ; self.box_v10.setGeometry(10,370,150,30);self.box_v10.currentIndexChanged.connect(self.save_comboboxes)
        self.button_v10 = QtWidgets.QPushButton('動作10',page2) ; self.button_v10.setGeometry(190,370,100,30);self.button_v10.clicked.connect(lambda:self.gif_choose(10))
        self.box_v11 = QtWidgets.QComboBox(page2) ; self.box_v11.addItems(self.options) ; self.box_v11.setGeometry(330,10,150,30);self.box_v11.currentIndexChanged.connect(self.save_comboboxes)
        self.button_v11 = QtWidgets.QPushButton('動作11',page2) ; self.button_v11.setGeometry(510,10,100,30);self.button_v11.clicked.connect(lambda:self.gif_choose(11))
        self.box_v12 = QtWidgets.QComboBox(page2) ; self.box_v12.addItems(self.options) ; self.box_v12.setGeometry(330,50,150,30);self.box_v12.currentIndexChanged.connect(self.save_comboboxes)
        self.button_v12 = QtWidgets.QPushButton('動作12',page2) ; self.button_v12.setGeometry(510,50,100,30);self.button_v12.clicked.connect(lambda:self.gif_choose(12))
        self.box_v13 = QtWidgets.QComboBox(page2) ; self.box_v13.addItems(self.options) ; self.box_v13.setGeometry(330,90,150,30);self.box_v13.currentIndexChanged.connect(self.save_comboboxes)
        self.button_v13 = QtWidgets.QPushButton('動作13',page2) ; self.button_v13.setGeometry(510,90,100,30);self.button_v13.clicked.connect(lambda:self.gif_choose(13))
        self.box_v14 = QtWidgets.QComboBox(page2) ; self.box_v14.addItems(self.options) ; self.box_v14.setGeometry(330,130,150,30);self.box_v14.currentIndexChanged.connect(self.save_comboboxes)
        self.button_v14 = QtWidgets.QPushButton('動作14',page2) ; self.button_v14.setGeometry(510,130,100,30);self.button_v14.clicked.connect(lambda:self.gif_choose(14))
        self.box_v15 = QtWidgets.QComboBox(page2) ; self.box_v15.addItems(self.options) ; self.box_v15.setGeometry(330,170,150,30);self.box_v15.currentIndexChanged.connect(self.save_comboboxes)
        self.button_v15 = QtWidgets.QPushButton('動作15',page2) ; self.button_v15.setGeometry(510,170,100,30);self.button_v15.clicked.connect(lambda:self.gif_choose(15))
        self.box_v16 = QtWidgets.QComboBox(page2) ; self.box_v16.addItems(self.options) ; self.box_v16.setGeometry(330,210,150,30);self.box_v16.currentIndexChanged.connect(self.save_comboboxes)
        self.button_v16 = QtWidgets.QPushButton('動作16',page2) ; self.button_v16.setGeometry(510,210,100,30);self.button_v16.clicked.connect(lambda:self.gif_choose(16))
        self.box_v17 = QtWidgets.QComboBox(page2) ; self.box_v17.addItems(self.options) ; self.box_v17.setGeometry(330,250,150,30);self.box_v17.currentIndexChanged.connect(self.save_comboboxes)
        self.button_v17 = QtWidgets.QPushButton('動作17',page2) ; self.button_v17.setGeometry(510,250,100,30);self.button_v17.clicked.connect(lambda:self.gif_choose(17))
        self.box_v18 = QtWidgets.QComboBox(page2) ; self.box_v18.addItems(self.options) ; self.box_v18.setGeometry(330,290,150,30);self.box_v18.currentIndexChanged.connect(self.save_comboboxes)
        self.button_v18 = QtWidgets.QPushButton('動作18',page2) ; self.button_v18.setGeometry(510,290,100,30);self.button_v18.clicked.connect(lambda:self.gif_choose(18))
        self.box_v19 = QtWidgets.QComboBox(page2) ; self.box_v19.addItems(self.options) ; self.box_v19.setGeometry(330,330,150,30);self.box_v19.currentIndexChanged.connect(self.save_comboboxes)
        self.button_v19 = QtWidgets.QPushButton('動作19',page2) ; self.button_v19.setGeometry(510,330,100,30);self.button_v19.clicked.connect(lambda:self.gif_choose(19))
        self.box_v20 = QtWidgets.QComboBox(page2) ; self.box_v20.addItems(self.options) ; self.box_v20.setGeometry(330,370,150,30);self.box_v20.currentIndexChanged.connect(self.save_comboboxes)
        self.button_v20 = QtWidgets.QPushButton('動作20',page2) ; self.button_v20.setGeometry(510,370,100,30);self.button_v20.clicked.connect(lambda:self.gif_choose(20))
        
        
        # 建立第二個頁面
        page3 = QtWidgets.QWidget()
        page3.setObjectName("page")
        label_3 = QtWidgets.QLabel(page3)
        label_3.setGeometry(70,50,540,310)
        self.control.label=label_3
        #self.label_3 = QtWidgets.QLabel('',page3);self.label_3.setGeometry(10,10,100,30)
        button = QtWidgets.QPushButton('開始',page3);button.move(550,370)
        button.setStyleSheet(" font-family: Microsoft JhengHei; font-size: 18px")
        button.clicked.connect(self.on_button_clicked);button.clicked.connect(self.on_button_clicked1)
        
        page4 = QtWidgets.QWidget()
        page4.setObjectName("page")
        label_4_data = [('自定義1', 20, 50), ('自定義2', 20, 90), ('自定義3', 20, 130), ('自定義4', 20, 170), ('自定義5', 20, 210), ('自定義6', 20, 250), ('自定義7', 20, 290), ('自定義8', 20, 330)]
        for text, x, y in label_4_data:
            label = QtWidgets.QLabel(text, page4)
            label.setGeometry(x, y, 100, 30)
            label.setStyleSheet('font-size: 12pt')
        self.input1_1 = QtWidgets.QLineEdit(page4) ; self.input1_1.setGeometry(80,50,100,30)
        self.input1_2 = QtWidgets.QLineEdit(page4) ; self.input1_2.setGeometry(190,50,100,30)
        self.input2_1 = QtWidgets.QLineEdit(page4) ; self.input2_1.setGeometry(80,90,100,30)
        self.input2_2 = QtWidgets.QLineEdit(page4) ; self.input2_2.setGeometry(190,90,100,30)
        self.input3_1 = QtWidgets.QLineEdit(page4) ; self.input3_1.setGeometry(80,130,100,30)
        self.input3_2 = QtWidgets.QLineEdit(page4) ; self.input3_2.setGeometry(190,130,100,30)
        self.input4_1 = QtWidgets.QLineEdit(page4) ; self.input4_1.setGeometry(80,170,100,30)
        self.input4_2 = QtWidgets.QLineEdit(page4) ; self.input4_2.setGeometry(190,170,100,30)
        self.input5_1 = QtWidgets.QLineEdit(page4) ; self.input5_1.setGeometry(80,210,100,30)
        self.input5_2 = QtWidgets.QLineEdit(page4) ; self.input5_2.setGeometry(190,210,100,30)
        self.input6_1 = QtWidgets.QLineEdit(page4) ; self.input6_1.setGeometry(80,250,100,30)
        self.input6_2 = QtWidgets.QLineEdit(page4) ; self.input6_2.setGeometry(190,250,100,30)
        self.input6_3 = QtWidgets.QLineEdit(page4) ; self.input6_3.setGeometry(300,250,100,30)
        self.input7_1 = QtWidgets.QLineEdit(page4) ; self.input7_1.setGeometry(80,290,100,30)
        self.input7_2 = QtWidgets.QLineEdit(page4) ; self.input7_2.setGeometry(190,290,100,30)
        self.input7_3 = QtWidgets.QLineEdit(page4) ; self.input7_3.setGeometry(300,290,100,30)
        self.input8_1 = QtWidgets.QLineEdit(page4) ; self.input8_1.setGeometry(80,330,100,30)
        self.input8_2 = QtWidgets.QLineEdit(page4) ; self.input8_2.setGeometry(190,330,100,30)
        self.input8_3 = QtWidgets.QLineEdit(page4) ; self.input8_3.setGeometry(300,330,100,30)
        
        button_save = QtWidgets.QPushButton('存入',page4);button_save.move(450,290)
        button_help = QtWidgets.QPushButton('快捷鍵查詢',page4);button_help.move(450,330)
        button_save.clicked.connect(self.custom)
        button_save.clicked.connect(self.save_text)
        button_help.clicked.connect(self.open_help_page)

        page5 = QtWidgets.QWidget()
        page5.setObjectName("page")
        label_5_data = [('自定義路徑1', 20, 50), ('自定義路徑2', 20, 90),('自定義路徑3', 20, 130),('自定義路徑4', 20, 170), ('自定義網址1', 20, 210), ('自定義網址2', 20, 250),('自定義網址3', 20, 290),('自定義網址4', 20, 330)]
        for text, x, y in label_5_data:
            label = QtWidgets.QLabel(text, page5)
            label.setGeometry(x, y, 100, 30)
            label.setStyleSheet('font-size: 12pt')
        self.input_path1 = QtWidgets.QLineEdit(page5) ; self.input_path1.setGeometry(140,50,370,30)
        self.input_path2 = QtWidgets.QLineEdit(page5) ; self.input_path2.setGeometry(140,90,370,30)
        self.input_path3 = QtWidgets.QLineEdit(page5) ; self.input_path3.setGeometry(140,130,370,30)
        self.input_path4 = QtWidgets.QLineEdit(page5) ; self.input_path4.setGeometry(140,170,370,30)
        self.input_web1 = QtWidgets.QLineEdit(page5) ; self.input_web1.setGeometry(140,210,370,30)
        self.input_web2 = QtWidgets.QLineEdit(page5) ; self.input_web2.setGeometry(140,250,370,30)
        self.input_web3 = QtWidgets.QLineEdit(page5) ; self.input_web3.setGeometry(140,290,370,30)
        self.input_web4 = QtWidgets.QLineEdit(page5) ; self.input_web4.setGeometry(140,330,370,30)
        
        button_S = QtWidgets.QPushButton('存 入',page5);button_S.setGeometry(500,380,100,40)
        button_S.setStyleSheet(" font-family: Microsoft JhengHei; font-size: 18px")
        button_S.clicked.connect(self.custom)
        button_S.clicked.connect(self.save_text)
        
        
        
        page0 = QtWidgets.QWidget()
        page0.setObjectName("page")
        label_0 = QtWidgets.QLabel(page0)          # 在 Form 裡加入 label
        label_0.move(30,30)                       # 移動到 (50, 50) 的位置
        label_0.setText('選擇使用者')            # 寫入文字
        label_0.setStyleSheet('font-size:20px; color:#00c')  # 設定樣式  
        self.box = QtWidgets.QComboBox(page0) ; self.box.addItems(self.user) ; self.box.setGeometry(30,70,100,30)
        self.box.currentIndexChanged.connect(self.load_text)
        self.box.currentIndexChanged.connect(self.load_comboboxes)
        label_01 = QtWidgets.QLabel(page0)          # 在 Form 裡加入 label
        label_01.move(30,170)                       # 移動到 (50, 50) 的位置
        label_01.setText('新增使用者')
        label_01.setStyleSheet('font-size:20px; color:#00c')  # 設定樣式
        self.label_02 = QtWidgets.QLabel(page0)          
        self.label_02.setGeometry(30,290,200,30)                       
        self.label_02.setText('')
        self.label_02.setStyleSheet('font-size:20px; color:#00c')  
        self.user_input = QtWidgets.QLineEdit(page0)
        self.user_input.setGeometry(30, 210, 100, 30)
        self.button = QtWidgets.QPushButton(page0)
        self.button.setGeometry(30, 250, 100, 30)
        self.button.setText("創建")
        self.button.clicked.connect(self.create)
        self.button_delete = QtWidgets.QPushButton(page0)
        self.button_delete.setGeometry(180, 70, 100, 30)
        self.button_delete.setText("刪除使用者")
        self.button_delete.clicked.connect(self.delete)
        #self.box.setStyleSheet('border: 1px solid #ccc;border-radius: 5px;padding: 5px;background-color: white;color: black')
        #標籤
        self.tabs.addTab(page0, '使用者')
        self.tabs.addTab(page1, '使用方法')
        self.tabs.addTab(page2, '選單')
        self.tabs.addTab(page3, '鏡頭')
        self.tabs.addTab(page4, '自定義pyautogui')
        self.tabs.addTab(page5, '自定義路徑開啟')
        
        # 设置样式表
        self.setStyleSheet(
            """
            QWidget#page {
                background-color: #c1e3e8; 
                
            }

            """
            "QFrame#title_bar {"
            "   background-color: rgb(43, 181, 189);"
            "   color: rgb(43, 181, 189);"
            "}"
            "QPushButton {"
            "   background-color: #3498db;"
            "   color: #ffffff;"
            "   border-style: none;"
            "   padding: 5px 10px;"
            "   font-size: 12px;"
            "   border-radius: 3px;"
            "}"
            "QPushButton:hover {"
            "   background-color: #2980b9;"
            "}"
            
            """
            QTabWidget::tab-bar {
                alignment: left;
            }

            QTabBar::tab:last {
                border-top-right-radius: 3px;
            }

            QTabBar::tab {
                color: #333333;
                background-color: #dddddd;
                border: none;
                padding: 5px 10px;
                border-top-left-radius: 3px;
                font-family: Microsoft JhengHei;
                font-size: 15px;
            }

            QTabBar::tab:selected {
                background-color: #ffffff;
            }

            QTabBar::tab:!selected:hover {
                background-color: #f2f2f2;
            }

            QTabBar::tab:!selected:!hover {
                background-color: #dddddd;
            }

            QTabBar::tab:disabled {
                color: #999999;
            }

            """
            """
            QLineEdit {
                background-color: #f2f2f2; /* 修改为所需的背景色 */
                border: 1px solid #c0c0c0; /* 修改为所需的边框样式和颜色 */
                border-radius: 3px; /* 可选，添加圆角效果 */
            }
            QLineEdit:focus {
                border: 1px solid #0078d7; /* 修改为所需的聚焦边框样式和颜色 */
                outline: none; /* 可选，去掉聚焦时的外发光效果 */
            }

            """
            """
            QComboBox {
                background-color: rgb(27, 29, 35);
                border: 1px solid gray;
                border-radius: 3px;
                padding: 1px 18px 1px 3px;
                min-width: 6em;
                padding-left: 10px;
                color: #063469;
            }

            QComboBox:editable {
                background: #a0effa;
            }

            QComboBox:!editable, QComboBox::drop-down:editable {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #EAF2F8, stop: 0.4 #D6EAFB,
                                stop: 0.5 #B3DBF2, stop: 1.0 #82CFFD);
            }
            """
        )
    def delete(self): 
        user_name = self.box.currentText()
        with open("user.txt", "r") as file:
            lines = file.readline()
            user_list = lines.split(",")
        # 检查要删除的名字是否存在于列表中
            if user_name =='user1':
                self.label_02.setText(f"{user_name} 不能被删除。")
            else:
                user_list.remove(user_name)
                self.label_02.setText(f"{user_name} 已從列表中删除。")
                filename1 = user_name + ".txt"
                filename2 = user_name + "_ComboBox.txt"
                os.remove(filename1)
                os.remove(filename2)
                # 将修改后的内容写回文件
                with open("user.txt", "w") as file:
                    aaa=",".join(user_list)
                    file.writelines(aaa)
                self.box.clear()
                self.load_user()
                self.box.addItems(self.user)
    def create(self):
        name = self.user_input.text()
        with open("user.txt", "r") as file:
            content = file.read()
            users = content.split(",")  # 將content分割成使用者列表
            if name in users:
                self.label_02.setText("使用者已存在")
            else:
                filename1 = name + ".txt"
                with open(filename1, "w") as file:
                    file.write(",,,,,,,,,,,,,,,,,,,,,,,,,,")
                filename2 = name + "_ComboBox.txt"
                with open(filename2, "w") as file:
                    file.write("0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
                with open("user.txt", "a") as file:
                    file.write(","+ name)
                self.load_user()
                self.box.addItems([str(name)])
                self.label_02.setText("創建成功")    
    def load_user(self):
        with open('user.txt', 'r') as file:
            content = file.read().split(',')
            self.user = []
        for item in content:
            # 去除首尾空格并添加到user列表中
            self.user.append(item.strip())
        
    def gif_choose(self,num):
        index = num
        movie = None
        if index==1:
            movie = QMovie('v1.gif')
        elif index==2:
            movie = QMovie('v2.gif')
        elif index==3:
            movie = QMovie('v3.gif')
        elif index==4:
            movie = QMovie('v4.gif')
        elif index==5:
            movie = QMovie('v5.gif')
        elif index==6:
            movie = QMovie('v6.gif')
        elif index==7:
            movie = QMovie('v7.gif')
        elif index==8:
            movie = QMovie('v8.gif')
        elif index==9:
            movie = QMovie('v9.gif')
        elif index==10:
            movie = QMovie('v10.gif')
        elif index==11:
            movie = QMovie('v11.gif')
        elif index==12:
            movie = QMovie('v12.gif')
        elif index==13:
            movie = QMovie('v13.gif')
        elif index==14:
            movie = QMovie('v14.gif')
        elif index==15:
            movie = QMovie('v15.gif')
        elif index==16:
            movie = QMovie('v16.gif')
        elif index==17:
            movie = QMovie('v17.gif')
        elif index==18:
            movie = QMovie('v18.gif')
        elif index==19:
            movie = QMovie('v19.gif')
        elif index==20:
            movie = QMovie('v20.gif')
        else:
            pass
        if movie:
            self.label_GIF.setMovie(movie);self.label_GIF.raise_();movie.start() 
            # 使用 QTimer 設置2.5秒後結束照片顯示
            timer = QTimer(self)
            timer.singleShot(2500, self.end_GIF_display)        
    def end_GIF_display(self):
        self.label_GIF.clear()  # 清除照片
        self.label_GIF.lower()  # 將照片 QLabel 降低到最下層
        
    def on_button_clicked(self):
        self.video = threading.Thread(target=self.control.camera)
        self.video.start()
    def on_button_clicked1(self):
        self.judge = threading.Thread(target=self.control.judge)
        self.judge.start()
        
        
    def signal(self, message):
        for index, box in enumerate(self.boxes, start=1):
            if message == 'v{}'.format(index):
                self.choose = box.currentText()
                self.action()
                break             
    def action (self): 
        if self.choose=='volumeUp':
            self.control_Action.volumeUp()
        elif self.choose=='volumeDown':
            self.control_Action.volumeDown()
        elif self.choose=='volume_mute':
            self.control_Action.volume_mute()
        elif self.choose=='mediaPause':
            self.control_Action.mediaPause()
        elif self.choose=='mediaNextTrack':
            self.control_Action.mediaNextTrack()
        elif self.choose=='mediaPrevTrack':
            self.control_Action.mediaNextTrack()
        elif self.choose=='previous_page':
            self.control_Action.previous_page()
        elif self.choose=='next_page':
            self.control_Action.next_page()
        elif self.choose=='windowRollUp':
            self.control_Action.windowRollUp()
        elif self.choose=='windowRollDown':
            self.control_Action.windowRollDown()
        elif self.choose=='screenshot':
            self.control_Action.screenshot()
        elif self.choose=='自定義1':
            pyautogui.hotkey(self.custom1_1,self.custom1_2)
        elif self.choose=='自定義2':
            pyautogui.hotkey(self.custom2_1,self.custom2_2)
        elif self.choose=='自定義3':
            pyautogui.hotkey(self.custom3_1,self.custom3_2)
        elif self.choose=='自定義4':
            pyautogui.hotkey(self.custom4_1,self.custom4_1)
        elif self.choose=='自定義5':
            pyautogui.hotkey(self.custom5_1,self.custom5_2)
        elif self.choose=='自定義6':
            pyautogui.hotkey(self.custom6_1,self.custom6_2,self.custom6_3)
        elif self.choose=='自定義7':
            pyautogui.hotkey(self.custom7_1,self.custom7_2,self.custom7_3)
        elif self.choose=='自定義8':
            pyautogui.hotkey(self.custom8_1,self.custom8_1,self.custom8_3)
        elif self.choose=='自定義路徑1':
            subprocess.Popen(['start', self.custom_path1,'r'], shell=True)
        elif self.choose=='自定義路徑2':
            subprocess.Popen(['start', self.custom_path2,'r'], shell=True)
        elif self.choose=='自定義路徑3':
            subprocess.Popen(['start', self.custom_path3,'r'], shell=True)
        elif self.choose=='自定義路徑4':
            subprocess.Popen(['start', self.custom_path4,'r'], shell=True)
        elif self.choose=='自定義網址1':
            subprocess.Popen(['start', 'chrome', self.custom_web1], shell=True)
        elif self.choose=='自定義網址2':
            subprocess.Popen(['start', 'chrome', self.custom_web2], shell=True)
        elif self.choose=='自定義網址3':
            subprocess.Popen(['start', 'chrome', self.custom_web3], shell=True)
        elif self.choose=='自定義網址4':
            subprocess.Popen(['start', 'chrome', self.custom_web4], shell=True)
        else:
            pass

    def custom(self):
        self.custom1_1=self.input1_1.text() ; self.custom1_2=self.input1_2.text()
        self.custom2_1=self.input2_1.text() ; self.custom2_2=self.input2_2.text()
        self.custom3_1=self.input3_1.text() ; self.custom3_2=self.input3_2.text()
        self.custom4_1=self.input4_1.text() ; self.custom4_2=self.input4_2.text()
        self.custom5_1=self.input5_1.text() ; self.custom5_2=self.input5_2.text()
        self.custom6_1=self.input6_1.text() ; self.custom6_2=self.input6_2.text(); self.custom6_3=self.input6_3.text()
        self.custom7_1=self.input7_1.text() ; self.custom7_2=self.input7_2.text(); self.custom7_3=self.input7_3.text()
        self.custom8_1=self.input8_1.text() ; self.custom8_2=self.input8_2.text(); self.custom8_3=self.input8_3.text()
        self.custom_path1=self.input_path1.text() ; self.custom_path2=self.input_path2.text()
        self.custom_path3=self.input_path3.text() ; self.custom_path4=self.input_path2.text()
        self.custom_web1=self.input_web1.text() ; self.custom_web2=self.input_web2.text()
        self.custom_web3=self.input_web3.text() ; self.custom_web4=self.input_web4.text()

    def save_text(self):
        self.chooseUser=self.box.currentText()
        # 創建存儲文件的路徑
        filename = os.path.join(os.getcwd(), self.chooseUser+'.txt')

        # 將內容存儲到文件中
        with open(filename, 'w') as f:
            f.write(f"{self.input1_1.text()},{self.input1_2.text()},{self.input2_1.text()},{self.input2_2.text()},"
                    f"{self.input3_1.text()},{self.input3_2.text()},{self.input4_1.text()},{self.input4_2.text()},"
                    f"{self.input5_1.text()},{self.input5_2.text()},{self.input6_1.text()},{self.input6_2.text()},{self.input6_3.text()},"
                    f"{self.input7_1.text()},{self.input7_2.text()},{self.input7_3.text()},{self.input8_1.text()},{self.input8_2.text()},{self.input8_3.text()},"
                    f"{self.input_path1.text()},{self.input_path2.text()},{self.input_path3.text()},{self.input_path4.text()},"
                    f"{self.input_web1.text()},{self.input_web2.text()},{self.input_web3.text()},{self.input_web4.text()}")
    def load_text(self):
    # 從文件中加載之前存儲的內容input_path
        self.chooseUser=self.box.currentText()
        filename = os.path.join(os.getcwd(), self.chooseUser+'.txt')
        try:
            with open(filename, 'r') as f:
                text = f.read()
                values = text.split(',', maxsplit=26)
                if len(values) == 27:
                    self.input1_1.setText(values[0]);self.input1_2.setText(values[1])
                    self.input2_1.setText(values[2]);self.input2_2.setText(values[3])
                    self.input3_1.setText(values[4]);self.input3_2.setText(values[5])
                    self.input4_1.setText(values[6]);self.input4_2.setText(values[7])
                    self.input5_1.setText(values[8]);self.input5_2.setText(values[9])
                    self.input6_1.setText(values[10]);self.input6_2.setText(values[11]);self.input6_3.setText(values[12])
                    self.input7_1.setText(values[13]);self.input7_2.setText(values[14]);self.input7_3.setText(values[15])
                    self.input8_1.setText(values[16]);self.input8_2.setText(values[17]);self.input8_3.setText(values[18])
                    self.input_path1.setText(values[19])
                    self.input_path2.setText(values[20])
                    self.input_path3.setText(values[21])
                    self.input_path4.setText(values[22])
                    self.input_web1.setText(values[23])
                    self.input_web2.setText(values[24])
                    self.input_web3.setText(values[25])
                    self.input_web4.setText(values[26])
        except FileNotFoundError:
            pass

    def save_comboboxes(self):
        self.chooseUser=self.box.currentText()
        indexes = []
        for i in range(20):
            box = getattr(self, f'box_v{i+1}')
            indexes.append(str(box.currentIndex()))
        with open(self.chooseUser+'_ComboBox.txt', 'w') as f:
            f.write(','.join(indexes))
    def load_comboboxes(self):
        self.chooseUser=self.box.currentText()
        try:
            with open(self.chooseUser+'_ComboBox.txt', 'r') as f:
                indexes = f.read().split(',')
                for i in range(20):
                    getattr(self, f"box_v{i+1}").setCurrentIndex(int(indexes[i]))
        except (FileNotFoundError, ValueError, IndexError):
            # 如果檔案不存在，或者轉換整數失敗，或者列表索引失敗，就將所有的 QComboBox 都設置為空值
            for box in self.boxes:
                box.setCurrentIndex(0)

    def open_help_page(self):
        self.second_page = SecondPage()
        self.second_page.show()

    def closeEvent(self, event):
        self.control.model='end'
        if self.second_page:
            self.second_page.close()
        event.accept()
    
    def minimizeWindow(self):
        self.showMinimized()
    
    #拖動視窗    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if event.pos().y() <= 30:  # 只有鼠標在(0, 0, self.width(), 30)內才能拖動畫面
                self.drag_start_position = event.globalPosition()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and hasattr(self, 'drag_start_position'):
            if event.pos().y() <= 30:  # 只有鼠標在(0, 0, self.width(), 30)內才能拖動畫面
                delta = event.globalPosition() - self.drag_start_position
                new_pos = self.pos() + QPoint(delta.x(), delta.y())
                self.move(new_pos)
                self.drag_start_position = event.globalPosition()
            event.accept()





   

class SecondPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('快捷鍵')      # 設定視窗標題
        self.resize(680, 450)
        
        # 建立 QTabWidget 物件
        self.tabs = QtWidgets.QTabWidget(self)
        self.tabs.setGeometry(self.rect())  # 設定 QTabWidget 的尺寸
        
        # 建立第一個頁面
        page1 = QtWidgets.QWidget()
        label1 = QtWidgets.QLabel("開啟新分頁：Ctrl + T<br>關閉目前分頁：Ctrl + W<br>切換到下一個分頁：Ctrl + Tab 或者 Ctrl + Page Down<br>切換到上一個分頁：Ctrl + Shift + Tab 或者 Ctrl + Page Up<br>"
                                  "跳到特定分頁：Ctrl + [數字鍵 1-8]，例如 Ctrl + 1 跳到第一個分頁<br>切換到最後一個分頁：Ctrl + 9<br>重新載入目前分頁：Ctrl + R 或者 F5<br>停止載入目前分頁：Esc<br>"
                                  "開啟新的視窗：Ctrl + N<br>開啟新的無痕視窗：Ctrl + Shift + N<br>開啟下載管理器：Ctrl + J<br>開啟歷史記錄頁面：Ctrl + H<br>開啟書籤管理器：Ctrl + Shift + O<br>開啟開發人員工具：Ctrl + Shift + I", page1)
        self.setStyleSheet('background:rgb(161, 178, 179);')  # 使用網頁 CSS 樣式設定背景
        label1.setStyleSheet('font-size:20px; color:#00c')  # 設定樣式
        
        page2 = QtWidgets.QWidget()
        label2 = QtWidgets.QLabel("暫停/播放：空白鍵<br>"
                                   " 靜音/取消靜音：M 鍵<br>"
                                   " 調整音量：上/下箭頭鍵<br>"
                                   " 快進/倒退：左/右箭頭鍵（小步長）或者 J/K 鍵（大步長）<br>"
                                   "聚焦聊天輸入框：Enter 或者 T 鍵<br>"
                                   "聚焦聊天輸入框：Enter 或者 T 鍵<br>"
                                   "切換全螢幕模式：F11 鍵<br>"
                                   "切換到下一個頻道：Ctrl + Tab<br>切換到上一個頻道：Ctrl + Shift + Tab", page2)
        self.setStyleSheet('background:rgb(161, 178, 179);')  # 使用網頁 CSS 樣式設定背景
        label2.setStyleSheet('font-size:20px; color:#00c')  # 設定樣式
        
        page3 = QtWidgets.QWidget()
        label3 = QtWidgets.QLabel("暫停/播放：空白鍵<br>"
                                   " 靜音/取消靜音：M 鍵<br>"
                                   " 調整音量：上/下箭頭鍵<br>"
                                   " 快進/倒退：左/右箭頭鍵（小步長）或者 J/K 鍵（大步長）<br>"
                                   "回到影片開頭：0（數字鍵盤）<br>"
                                   "快進到影片的特定時間：數字鍵盤的數字 + Enter<br>"
                                   "開啟全螢幕模式：F 鍵<br>"
                                   "關閉全螢幕模式：Esc 鍵<br>在搜尋欄位中進行搜尋：/ 鍵", page3)
        self.setStyleSheet('background:rgb(161, 178, 179);')  # 使用網頁 CSS 樣式設定背景
        label3.setStyleSheet('font-size:20px; color:#00c')  # 設定樣式
        #標籤
        self.tabs.addTab(page1, 'chrome快捷鍵')
        self.tabs.addTab(page2, 'twitch快捷鍵')
        self.tabs.addTab(page3, 'youtube快捷鍵')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Form = MyWidget()
    Form.show()
    sys.exit(app.exec())
    