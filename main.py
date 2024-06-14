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
    QMessageBox, QDesktopWidget
from PyQt5.QtGui import QPixmap,   QPainter, QPen, QColor
from PyQt5.QtCore import Qt

from PIL import Image

from Root_Preprocess import Ui_MainWindow

class PainterLabel(QLabel):
    def __init__(self, parent=None):
        super(PainterLabel, self).__init__(parent)
        #self.setPixmap(QPixmap('your_image.png'))  # 替换为你的图片路径
        self.last_point = None
        self.eraser_size = 20
        self.setScaledContents(True)  # 保持纵横比

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_point = self.mapToPixmap(event.pos())

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            current_pos = self.mapToPixmap(event.pos())
            self.erase(self.last_point, current_pos)
            self.last_point = current_pos

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_point = None

    def mapToPixmap(self, pos):
        # 获取 QLabel 的尺寸和 QPixmap 的尺寸
        label_width = self.width()
        label_height = self.height()
        pixmap_width = self.pixmap().width()
        pixmap_height = self.pixmap().height()

        # 计算缩放比例
        scale = min(label_width / pixmap_width, label_height / pixmap_height)

        # 计算 QPixmap 在 QLabel 中的实际显示区域
        display_width = pixmap_width * scale
        display_height = pixmap_height * scale
        offset_x = (label_width - display_width) / 2
        offset_y = (label_height - display_height) / 2

        # 将窗口坐标转换为图像坐标
        x = (pos.x() - offset_x) / scale
        y = (pos.y() - offset_y) / scale
        return QPoint(int(x), int( y) )

    def erase(self, start_point, end_point):
        pixmap = self.pixmap()
        if pixmap is None:
            return

        painter = QPainter(pixmap)
        pen = QPen(QColor(255, 255, 255), self.eraser_size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        painter.setPen(pen)
        painter.drawLine(start_point, end_point)
        painter.end()
        self.update()

class UiMain(QMainWindow, Ui_MainWindow):

    def setWindow(self):
        screen = QDesktopWidget().screenGeometry()
        window_width = screen.width() 
        window_height = screen.height() 
        self.setGeometry(screen.center().x() - window_width // 2, screen.center().y() - window_height // 2, window_width, window_height)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_point = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            painter = QPainter(self.image_label_1.pixmap())
            pen = QPen(QColor(255, 0, 0), self.eraser_size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            painter.setPen(pen)
            painter.drawLine(self.last_point, event.pos())
            painter.end()
            self.last_point = event.pos()
            self.image_label_1.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_point = None


    def __init__(self, parent=None):
        #如果没用特殊情况，中间图像全是opencv的图像

        super(UiMain, self).__init__(parent)
        self.info = 'info.json'
        self.setupUi(self)
        self.eraser_size=30
        self.current_index=None

        self.middle_filter_par=self.spinBox.value()

        self.bing_signal()
        self.init_style()
        self.threshold=0
        self.pixmap = QPixmap()
        self.gray_pixmap = QPixmap()
        self.q_image=None
        self.export_pixmap=None

        self.filtered_cv_image=None
        self.confirmed_cv_image=None

    def resize_event(self, event):
        print('resize event, main window size:', self.size())
        print('resize event:', self.image_label_1.size())
        print('image label size:', self.image_label_1.size())
        print('widget size:', self.widget.size())
        print('widget2 size:', self.widget_2.size())
        
        if self.q_image:
            #self.update_image(self.image_label_2, self.pixmap)
            self.update_image(self.image_label_1, self.pixmap)

    def save_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                                                   "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.tif)", options=options)
        if file_path:
            self.pixmap.save(file_path)

    def bing_signal(self):
        self.open_img_btn.clicked.connect(self.open_image)
        self.horizontalSlider.valueChanged.connect(self.horizontalSlider_valueChanged)
        self.plus_btn.clicked.connect(self.plus_button_clicked)
        self.minus_btn.clicked.connect(self.minus_button_clicked)
        self.threshold_apply_btn.clicked.connect(self.apply_threshold)  
        self.export_img_btn.clicked.connect(self.export_img)
        self.next_img_btn.clicked.connect(self.next_image)
        self.previous_img_btn.clicked.connect(self.previous_image)
        self.filter_img_btn.clicked.connect(self.middle_filter_image)
        self.confirm_btn.clicked.connect(self.confirm)



        self.resizeEvent=self.resize_event
        
    def confirm(self):
        self.confirmed_cv_image=self.filtered_cv_image

    def middle_filter_image(self):
        self.middle_filter_par=self.spinBox.value()
        cv_image=self.qimage2cv(self.q_image)        
        denoised_image = cv2.medianBlur(cv_image,  self.middle_filter_par)
        q_image=self.cv2qimage(denoised_image)

        self.filtered_cv_image=denoised_image

        self.update_image(self.image_label_1, QPixmap.fromImage(q_image) )

    def export_img(self):
        options = QFileDialog.Options()

        file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                                                   "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.tif)", options=options)
        if file_path:
            self.pixmap.save(file_path)

    def previous_image(self):
        if not self.current_index:
            return

        if self.current_index > 0:
            self.current_index -= 1
        else:
            QMessageBox.information(self, 'Info', 'This is the first image')
            return

        self.read_image(self.image_files[self.current_index])

    def next_image(self):
        if not self.current_index:
            return
        if self.current_index < len(self.image_files)-1:
            self.current_index += 1
        else:
            QMessageBox.information(self, 'Info', 'This is the last image')
            return 

        self.read_image(self.image_files[self.current_index])

    def init_style(self):
        pass

    def apply_threshold(self):
        gray_image=self.filter_image()

        self.update_image(self.image_label_1, QPixmap.fromImage(gray_image) )

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


    def update_image(self, image_label, pixmap):
        
        scaledPixmap = pixmap.scaled(self.image_label_1.size(), Qt.KeepAspectRatio)
        print(self.size(), 'label size:')
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setPixmap(scaledPixmap)
        

    def get_image_file_list(self, path):
        dir1, fname=os.path.split(path)
        self.path=dir1
        image_files=[]
        for f in os.listdir(dir1): 
            if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tif', '.tiff')):
                full_path=os.path.join(dir1, f)
                full_path = full_path.replace("\\", "/")
                image_files.append(full_path)

        return image_files
    
    def read_image(self, file_path):
        self.q_image=QImage(file_path)
        #gray_image = self.q_image.convertToFormat(QImage.Format_Grayscale8)
        self.pixmap = QPixmap.fromImage(self.q_image)            
        #self.gray_pixmap=QPixmap.fromImage(gray_image)
        self.image_label_1.setPixmap( QPixmap.fromImage(self.q_image)  )
        self.update_image(self.image_label_1, self.pixmap)


    def open_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "",
                                                   "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.tif *.tiff)", options=options)

        if file_path:
            #self.pil_image=Image.open(file_path)
            self.image_files=self.get_image_file_list(file_path)
            self.current_index=self.image_files.index(file_path)

            self.read_image(file_path)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = UiMain()
    win.show()
    sys.exit(app.exec_())
