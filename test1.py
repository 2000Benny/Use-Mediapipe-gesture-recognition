from PyQt6.QtWidgets import QApplication, QWidget, QComboBox, QPushButton, QVBoxLayout
import os

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_text()
        
    def initUI(self):
        # 创建4个combobox，并设置其选项
        self.options = ['No', 'volumeUp', 'volumeDown', 'mediaPause', 'mediaNextTrack', 
                        'previous_page', 'next_page', 'windowRollDown', 'windowRollUp', 
                        '自定義1', '自定義2', '自定義3', '自定義4', 
                        '自定義路徑1', '自定義路徑2', '自定義網址1', '自定義網址2']
        self.box_v1 = QtWidgets.QComboBox(self)
        self.box_v1.addItems(self.options)
        self.box_v2 = QtWidgets.QComboBox(self)
        self.box_v2.addItems(self.options)
        self.box_v3 = QtWidgets.QComboBox(self)
        self.box_v3.addItems(self.options)
        self.box_v4 = QtWidgets.QComboBox(self)
        self.box_v4.addItems(self.options)

        # 创建保存按钮，用于保存combobox的选项
        self.save_button = QtWidgets.QPushButton('Save', self)
        self.save_button.clicked.connect(self.save_text)

    def load_text(self):
        # 从 QSettings 中读取 combobox 的选项，并设置到对应的combobox中
        settings = QSettings("MyCompany", "MyApp")
        self.box_v1.setCurrentIndex(settings.value("box_v1", 0, type=int))
        self.box_v2.setCurrentIndex(settings.value("box_v2", 0, type=int))
        self.box_v3.setCurrentIndex(settings.value("box_v3", 0, type=int))
        self.box_v4.setCurrentIndex(settings.value("box_v4", 0, type=int))

    def save_text(self):
        # 将 combobox 的选项保存到 QSettings 中
        settings = QSettings("MyCompany", "MyApp")
        settings.setValue("box_v1", self.box_v1.currentIndex())
        settings.setValue("box_v2", self.box_v2.currentIndex())
        settings.setValue("box_v3", self.box_v3.currentIndex())
        settings.setValue("box_v4", self.box_v4.currentIndex())
        
        # 手动同步 QSettings
        settings.sync()

    def closeEvent(self, event):
        # 在窗口关闭前保存选项
        self.save_text()
        super().closeEvent(event)


if __name__ == '__main__':
    app = QApplication([])
    w = MyWidget()
    w.show()
    app.exec()
