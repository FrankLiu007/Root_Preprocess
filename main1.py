import sys
import os
import json
import datetime
from decimal import Decimal, getcontext

getcontext().prec = 10
getcontext().rounding = 'ROUND_HALF_UP'

#from tkinter import Tk
import numpy as np
from PyQt5.QtGui import QImage
import cv2
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QAction, QToolBar, QMainWindow, QFileDialog, \
    QMessageBox
from PyQt5.QtGui import QPixmap, qGray

from PIL import Image

from Root_Preprocess import Ui_MainWindow


class UiMain(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(UiMain, self).__init__(parent)
        self.info = 'info.json'
        self.setupUi(self)
        self.bing_signal()
        self.init_style()
        self.threshold=0
        self.pixmap = QPixmap()
        self.gray_pixmap = QPixmap()

    def bing_signal(self):
        self.open_img_btn.clicked.connect(self.openImage)
        self.horizontalSlider.valueChanged.connect(self.horizontalSlider_valueChanged)
        self.plus_btn.clicked.connect(self.plus_button_clicked)
        self.minus_btn.clicked.connect(self.minus_button_clicked)
        self.threshold_apply_btn.clicked.connect(self.apply_threshold)  
        pass

    def init_style(self):
        pass

    def apply_threshold(self):
        gray_image=self.filter_image()
        self.update_image(gray_image)

    def plus_button_clicked(self):
        self.threshold += 1
        self.lineEdit.setText(str(self.threshold))
        self.horizontalSlider.setValue(self.threshold)


    def horizontalSlider_valueChanged(self):
        self.threshold = self.horizontalSlider.value()
        self.lineEdit.setText(str(self.threshold))

    def minus_button_clicked(self):
        self.threshold -= 1
        self.lineEdit.setText(str(self.threshold))
        self.horizontalSlider.setValue(self.threshold)


    def filter_image(self):        
        # 2. 进行二值化处理
        tt=self.q_image.convertToFormat(QImage.Format_Grayscale8)
        cv2_image=self.qimage2cv(tt)
        _, binary_image = cv2.threshold(cv2_image, self.threshold, 255, cv2.THRESH_BINARY)
        q_image=self.cv2qimage(binary_image)
        return q_image
    
    def cv2qimage(self, cv_image):
        """Convert OpenCV image to QImage."""
        height, width, channel = cv_image.shape
        bytes_per_line = 3 * width
        qimage = QImage(cv_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        return qimage.rgbSwapped()

    def qimage2cv(self, q_image):
        """Convert QImage to OpenCV image."""
        
        width = q_image.width()
        height = q_image.height()
        ptr = q_image.bits()
        ptr.setsize(q_image.byteCount())
        arr = np.array(ptr).reshape(height, width, 1)  # Copies the data
        return cv2.cvtColor(arr, cv2.COLOR_RGBA2BGR)


    def update_image(self, gray_image):
        #scaledPixmap = self.pixmap.scaled(self.size(), Qt.KeepAspectRatio)
        self.gray_pixmap = QPixmap.fromImage(gray_image)
        self.image_label_1.setPixmap(self.gray_pixmap)
        self.image_label_1.setScaledContents(True)

    def openImage(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "",
                                                   "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)

        if file_path:
            self.pil_image=Image.open(file_path)
            self.pixmap = QPixmap(file_path)
            self.image_label_2.setPixmap(self.pixmap)
            self.image_label_2.setScaledContents(True)

            self.q_image = self.pixmap.toImage()
            gray_image = self.q_image.convertToFormat(QImage.Format_Grayscale8)
      
            self.update_image(gray_image)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = UiMain()
    win.show()
    sys.exit(app.exec_())
