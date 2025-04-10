from RootSelectUI import Ui_RootSelection
import numpy as np
import cv2

from PyQt5.QtWidgets import  QMainWindow,  QGraphicsScene,  QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap,   QPainter, QPen, QColor, QRegion
from PyQt5.QtCore import Qt
import utils

from ImageViewer import ImageGraphicsView
class UiMain(QMainWindow, Ui_RootSelection):

    def customizeUI(self):
        self.scene=   QGraphicsScene()
        self.scene.setBackgroundBrush(QColor(255, 255, 255,128))
        self.graphicsView.deleteLater()
        self.graphicsView = ImageGraphicsView(self.frame_2)
        self.graphicsView.setScene(self.scene)

        
    def set_scene_pixmap(self, pixmap):
        self.origin_pixmap = pixmap

        self.scene.clear()
        self.scene.setSceneRect(0, 0, pixmap.width(), pixmap.height())
        self.graphicsView.base_pixmap_item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(self.graphicsView.base_pixmap_item)
        self.graphicsView.resize(self.centralwidget.size())
        self.graphicsView.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio) 


    def set_mainwindow(self, mainWindow):
        self.mainWindow = mainWindow

    def __init__(self):
        super(UiMain, self).__init__()
        self.setupUi(self)
        self.customizeUI()
        self.bing_signal()
        self.mainWindow =None
        self.origin_pixmap = None
        self.contrast=0
        self.brightness=0

    def bing_signal(self):

        self.actionconfirm.triggered.connect(self.confirm_selection)
        self.actionreset.triggered.connect(self.reload)

        self.handToolButton.clicked.connect(self.hand_tool)
        self.rectangleToolButton.clicked.connect(self.rectangle_tool)
        self.lassoToolButton.clicked.connect(self.lasso_tool)
        self.eraserToolButton.clicked.connect(self.eraser_tool)

        self.contrastSlider.valueChanged.connect(self.contrast_change)
        self.brightnessSlider.valueChanged.connect(self.brightness_change)

        self.showEvent=self.show_event
        self.resizeEvent=self.resize_event
        self.spinBox.valueChanged.connect(self.update_eraser_size)
        
    def update_eraser_size(self, value):
        self.graphicsView.set_erase_size(value)
        #self.graphicsView.eraser_size=value

    def eraser_tool(self):
        self.graphicsView.setTool('eraser')
        self.graphicsView.eraser_size=self.spinBox.value()


    def brightness_change(self, value):
        self.brightness = value
        self.adjust_brightness_contrast()


    def adjust_brightness_contrast(self):
        #参考了gimp，效果更好
        image = utils.qpixmap_to_cv2(self.origin_pixmap)
        
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
    
    def contrast_change(self, value):
        
        self.contrast = value
        self.adjust_brightness_contrast()
        


    def hand_tool(self):
        self.graphicsView.setTool('hand')

    def show_event(self, event):

        self.graphicsView.resize(self.centralwidget.size())
        self.graphicsView.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
        super().showEvent(event)

    def reset(self):
        self.curr_tool=None

        self.rect_items = []
        self.rect_item = None

        self.points = []
        self.polygon_items = []
        #self.polygon_item = None
        self.current_polygon = None

        #self.
    def reload(self):
        self.set_scene_pixmap(self.origin_pixmap)

    def resize_event(self, event):
        self.graphicsView.resize(self.centralwidget.size())
        self.graphicsView.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

    def rectangle_tool(self):
        
        self.graphicsView.setTool('rectangle')

    def lasso_tool(self):
        self.graphicsView.setTool('lasso')

    def confirm_selection(self):
        pixmap=self.graphicsView.base_pixmap_item.pixmap()
        new_pixmap = QPixmap(pixmap.size())
        new_pixmap.fill(QColor('white'))  # Fill with white

        # Create a painter to draw on the new pixmap
        painter = QPainter(new_pixmap)
        for rect_item in self.graphicsView.rect_items:
            rect=rect_item.rect()
            painter.drawPixmap(rect, pixmap, rect)  # Copy the rectangular area
        self.graphicsView.rect_items=[]

        for polygon_item in self.graphicsView.polygon_items:
            polygon = polygon_item.polygon()

            painter.setClipRegion(QRegion(polygon.toPolygon()) )
            painter.setPen(QPen(Qt.black, 2))
            painter.drawPixmap(0,0, self.graphicsView.base_pixmap_item.pixmap() )
        self.graphicsView.polygon_items=[]
        painter.end()

        self.set_scene_pixmap(new_pixmap)
        #self.graphicsView.restore_view_state()
        self.mainWindow.setOriginalPixmap(new_pixmap)
        self.mainWindow.update_image_viewer(self.mainWindow.graphicsView, new_pixmap, True )
        #self.close()