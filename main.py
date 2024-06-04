import sys
import os
import json
import datetime
from decimal import Decimal, getcontext

getcontext().prec = 10
getcontext().rounding = 'ROUND_HALF_UP'

from tkinter import Tk

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QAction, QToolBar, QMainWindow, QFileDialog, \
    QMessageBox
from PyQt5.QtGui import QPixmap

from Root_Preprocess import Ui_MainWindow


class UiMain(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(UiMain, self).__init__(parent)
        self.info = 'info.json'
        self.setupUi(self)
        self.bing_signal()
        self.init_style()

    def bing_signal(self):
        self.open_img_btn.clicked.connect(self.openImage)
        pass

    def init_style(self):
        pass


    def openImage(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "",
                                                   "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)
        if file_path:
            pixmap = QPixmap(file_path)
            self.image_label_1.setPixmap(pixmap)
            self.image_label_1.setScaledContents(True)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = UiMain()
    win.show()
    sys.exit(app.exec_())
