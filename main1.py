import sys
import os
import json
import datetime
from decimal import Decimal, getcontext

getcontext().prec = 10
getcontext().rounding = 'ROUND_HALF_UP'

#from tkinter import Tk
import numpy as np

import cv2
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import  QMainWindow, QFileDialog,  QMessageBox,  QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap,   QPainter,  QColor, QCursor, QImage
from PyQt5.QtCore import Qt,QSize

from PIL import Image

from Root_Preprocess import Ui_MainWindow

from ImageViewer import ImageGraphicsView

import utils
import  RootSelect

class UiMain(QMainWindow, Ui_MainWindow):

    # def setWindow(self):
    #     screen = QDesktopWidget().screenGeometry()
    #     window_width = screen.width() 
    #     window_height = screen.height() 
    #     self.setGeometry(screen.center().x() - window_width // 2, screen.center().y() - window_height // 2, window_width, window_height)

    def customizeUI(self):
        self.graphicsView.deleteLater()
        self.graphicsView = ImageGraphicsView(self.widget)

        self.graphicsView.resize(QSize(800,800))

        self.graphicsView_2.deleteLater()
        self.graphicsView_2 = ImageGraphicsView(self.widget_2)

        self.graphicsView_2.resize(QSize(800,800))

        self.mask_pixmap=None

        self.graphicsView.set_sync_view(self.graphicsView_2)
        self.graphicsView_2.set_sync_view(self.graphicsView)
        

    def render_scene_to_pixmap(self, scene):
        # Determine the size of the scene
        scene_rect = scene.sceneRect()
        width = int(scene_rect.width())
        height = int(scene_rect.height())

        # Create a QPixmap to render the scene into
        pixmap = QPixmap(width, height)
        pixmap.fill(Qt.white)  # Fill the pixmap with white background

        # Create a QPainter to render the scene into the QPixmap
        painter = QPainter(pixmap)
        scene.render(painter)
        painter.end()
        return pixmap

    def __init__(self, parent=None):
        #如果没用特殊情况，中间图像全是opencv的图像
        super(UiMain, self).__init__(parent)
        self.info = 'info.json'
        self.setupUi(self)
        self.customizeUI()

        self.bing_signal()

        self.eraser_size=30
        self.current_index=None

        #self.middle_filter_par=self.spinBox.value()

        self.threshold=200
        self.thresholdSpinBox.setValue(self.threshold)
        
        self.pixmap = QPixmap()
        self.original_pixmap = None

        self.brightness = 0
        self.contrast = 0

        self.selectedRootPixmap=None
        self.selectedRootItem=QGraphicsPixmapItem()

    def setOriginalPixmap(self, pixmap):
        self.original_pixmap = pixmap

    def bing_signal(self):
        self.open_img_btn.clicked.connect(self.open_image)
        self.horizontalSlider.valueChanged.connect(self.horizontalSlider_valueChanged)
        #self.plus_btn.clicked.connect(self.plus_button_clicked)
        #self.minus_btn.clicked.connect(self.minus_button_clicked)
        self.threshold_apply_btn.clicked.connect(self.apply_threshold)  
        self.export_img_btn.clicked.connect(self.export_img)
        self.next_img_btn.clicked.connect(self.next_image)
        self.previous_img_btn.clicked.connect(self.previous_image)
        self.thresholdSpinBox.valueChanged.connect(self.horizontalSlider.setValue)
 
        self.root_select_button.clicked.connect(self.root_select)
        self.brightnessSlider.valueChanged.connect(self.brightness_change)
        self.contrastSlider.valueChanged.connect(self.contrast_change)

        self.handToolButton.clicked.connect(self.hand)
        self.handToolButton_2.clicked.connect(self.hand2)

        self.pencilToolButton.clicked.connect(self.mask_pencil)
        self.eraserToolButton.clicked.connect(self.mask_eraser)

        self.pencilSizeSpinBox.valueChanged.connect(self.graphicsView_2.set_mask_pencil_size)
        self.eraserSizeSpinBox.valueChanged.connect(self.graphicsView_2.set_mask_eraser_size)
        
        self.resizeEvent=self.resize_event

    def mask_pencil(self):
        self.graphicsView_2.setTool('mask_pencil')
        self.graphicsView_2.setCursor(QCursor(Qt.CrossCursor))

    

    def brightness_change(self, value):
        self.brightness = value
        self.adjust_brightness_contrast()
    def contrast_change(self, value):
        self.contrast = value
        self.adjust_brightness_contrast()

    def adjust_brightness_contrast(self):
        #参考了gimp，效果更好
        pixmap=self.original_pixmap
        image = utils.qpixmap_to_cv2(pixmap)
        
        contrast = np.clip(self.contrast, -127, 127)
        brightness = np.clip(self.brightness, -127, 127)
        
        # 调整亮度：直接加到像素值上
        if brightness != 0:
            if brightness > 0:
                shadow = brightness
                highlight = 255
            else:
                shadow = 0
                highlight = 255 + brightness
            alpha_b = (highlight - shadow) / 255.0
            gamma_b = shadow
            image = cv2.addWeighted(image, alpha_b, image, 0, gamma_b)

        # 调整对比度：缩放像素值围绕中心点
        if contrast != 0:
            f = 131 * (contrast + 127) / (127 * (131 - contrast))
            alpha_c = f
            gamma_c = 127 * (1 - f)
            image = cv2.addWeighted(image, alpha_c, image, 0, gamma_c)
   
        pixmap = utils.cv2_to_qpixmap(image)
        self.graphicsView.base_pixmap_item.setPixmap(pixmap)

        return     
    def root_select(self):
        if self.original_pixmap is  None:
             QMessageBox.information(self, 'Info', 'Image not loaded ')
             return
        
        self.rootSelectWindow=RootSelect.UiMain()
        self.rootSelectWindow.set_mainwindow(self)

        self.rootSelectWindow.set_scene_pixmap(self.graphicsView.base_pixmap_item.pixmap())
        self.rootSelectWindow.show()


    def resize_event(self, event):
        #print('resize event, main window size:', self.size())

        if self.current_index is not None:
            self.graphicsView.resize(self.frame_3.size())
            self.graphicsView_2.resize(self.frame_5.size())
            self.graphicsView.base_pixmap_item.update()


    def save_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                                                   "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.tif)", options=options)
        if file_path:
            self.pixmap.save(file_path)



    def confirm(self):
        self.confirmed_pixmap=self.render_scene_to_pixmap(self.graphicsView.scene)

        self.update_image_viewer(self.graphicsView_2, self.confirmed_pixmap, False )


    def mask_eraser(self):
        self.graphicsView_2.eraser_size=self.eraserSizeSpinBox.value()
        self.graphicsView_2.setTool('mask_eraser')
        

    def hand(self):
        self.graphicsView.setTool('hand')
        self.graphicsView.setCursor(QCursor(Qt.OpenHandCursor))

    def hand2(self):
        self.graphicsView_2.setTool('hand')
        self.graphicsView_2.setCursor(QCursor(Qt.OpenHandCursor))

    def middle_filter(self):
        self.middle_filter_par=self.spinBox.value()
        
        cv_image=utils.qpixmap_to_cv2(self.graphicsView.base_pixmap_item.pixmap())        
        self.filtered_cv_image = cv2.medianBlur(cv_image,  self.middle_filter_par)

        pixmap=utils.cv2_to_qpixmap(self.filtered_cv_image)

        self.update_image_viewer(self.graphicsView, pixmap, True )
   
    def qpixmap2cv(self, qpixmap):      
        qimage=qpixmap.toImage()
        return self.qimage2cv(qimage)

    def export_img(self):
        path=self.image_files[self.current_index]
        dir1, fname=os.path.split(path)
        name, ext=os.path.splitext(fname)
        new_path=os.path.join(dir1, "export_"+name+'.png')
        self.graphicsView_2.base_pixmap_item.pixmap().save(new_path)

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
        if  self.current_index is None:
            return
        if self.current_index < len(self.image_files)-1:
            self.current_index += 1
        else:
            QMessageBox.information(self, 'Info', 'This is the last image')
            return 
        self.read_image(self.image_files[self.current_index])


    def apply_threshold(self): 

        self.update_image_viewer(self.graphicsView_2, self.graphicsView.base_pixmap_item.pixmap(), True )

        mask_pixmap=self.draw_mask()

        if  self.graphicsView_2.mask_pixmap_item.scene() is None:
            self.graphicsView_2.scene().addItem(self.graphicsView_2.mask_pixmap_item)
            self.graphicsView_2.mask_pixmap_item.setZValue(10)
        #self.selectedRootItem.setZValue(10)
        
        self.graphicsView_2.mask_pixmap_item.setPixmap(self.mask_pixmap)
        self.graphicsView_2.scene().update()

    def draw_mask(self):
    # 1. first 二值化
        pixmap=self.graphicsView.base_pixmap_item.pixmap()
        cv2_image=utils.qpixmap_to_cv2( pixmap )
        gray_image=cv2.cvtColor(cv2_image, cv2.COLOR_BGR2GRAY)
        _, binary_image = cv2.threshold(gray_image, self.threshold, 255, cv2.THRESH_BINARY)

    # 2. then create mask
        color = (255, 0, 0)  # 红色
        alpha = 0.5  # 70% 透明度
        # 读取二值化后的图片
        
        # 创建一个RGBA图像，初始化为全透明
        h, w = binary_image.shape
        mask = np.zeros((h, w, 4), dtype=np.uint8)
        
        # 设置黑色区域的颜色和透明度
        mask[binary_image == 0] = [color[0], color[1], color[2], 100]  ###透明度直接用128
        
        # 设置白色区域为完全透明
        mask[binary_image != 0, 3] = 0
    # 3. then draw mask
        self.mask_pixmap=self.convert_to_qpixmap(mask)

        
        return self.mask_pixmap

    def convert_to_qpixmap(self, rgba):
        # 将RGBA图像转换为QImage
        height, width, channel = rgba.shape
        bytes_per_line = 4 * width
        q_image = QImage(rgba.data, width, height, bytes_per_line, QImage.Format_RGBA8888)
        
        return QPixmap.fromImage(q_image)

    def plus_button_clicked(self):
        self.threshold += 1
        self.lineEdit.setText(str(self.threshold))
        self.horizontalSlider.setValue(self.threshold)

    def horizontalSlider_valueChanged(self):
        self.threshold = self.horizontalSlider.value()
        self.thresholdSpinBox.setValue(self.threshold)

    # def minus_button_clicked(self):
    #     self.threshold -= 1
    #     self.lineEdit.setText(str(self.threshold))
    #     self.horizontalSlider.setValue(self.threshold)

    def update_image_viewer(self, graphicsView, pixmap, keep_view_state):
        scene=graphicsView.scene()
        #scene.clear()
        scene.setSceneRect(0, 0, self.pixmap.width(), self.pixmap.height())
        graphicsView.base_pixmap_item = QGraphicsPixmapItem(pixmap)
        scene.addItem(graphicsView.base_pixmap_item)
        
        if keep_view_state:
            graphicsView.restore_view_state()
        else:
            graphicsView.fitInView(scene.sceneRect(), Qt.KeepAspectRatio)  # 自动调整视图以适应图像
            graphicsView.save_view_state()

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

        self.original_pixmap = QPixmap(file_path)

        self.graphicsView.scene().clear()
        self.update_image_viewer(self.graphicsView, self.original_pixmap, False)


    def open_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "",
                                                   "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.tif *.tiff)", options=options)

        if file_path:
            #self.pil_image=Image.open(file_path)
            self.image_files=self.get_image_file_list(file_path)
            self.current_index=self.image_files.index(file_path)

            self.read_image(file_path)




    def dilate_image(self):
        pixmap=self.graphicsView.base_pixmap_item.pixmap()
        cv_image=utils.qpixmap_to_cv2(pixmap)
        kernel = np.ones((5, 5), np.uint8)
        dilated_image = cv2.dilate(cv_image, kernel, iterations=1)
        pixmap=utils.cv2_to_qpixmap(dilated_image)
        self.update_image_viewer(self.graphicsView, pixmap, True )

    def erode_image(self):
        pixmap=self.graphicsView.base_pixmap_item.pixmap()
        cv_image=utils.qpixmap_to_cv2(pixmap)
        kernel = np.ones((5, 5), np.uint8)
        eroded_image = cv2.erode(cv_image, kernel, iterations=1)
        pixmap=utils.cv2_to_qpixmap(eroded_image)
        self.update_image_viewer(self.graphicsView, pixmap, True )

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = UiMain()
    win.show()
    sys.exit(app.exec_())
