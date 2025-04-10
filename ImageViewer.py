import sys
from PyQt5.QtWidgets import  QGraphicsScene, QGraphicsView, QGraphicsPolygonItem, QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsPixmapItem, QGraphicsLineItem
from PyQt5.QtGui import  QPainter, QPen, QBrush, QColor, QPolygonF, QPixmap, QPainter, QCursor
from PyQt5.QtCore import Qt, QPointF, QRectF, QRect, QLineF

class ImageGraphicsView(QGraphicsView):
    def __init__(self, widget):
        super().__init__(widget) 
        #self.setRenderHint(self.renderHints() | Qt.Antialiasing)
        self.setMouseTracking(True)
        #self.drawing = False
        self.erasing = False
        #self.dragging = False
        self.start_point = QPointF()
        self.end_point = QPointF()
        self.current_line = None
        self.scale_factor = 1.15  # 缩放因子
        
        self.base_cv_image = None

        self.eraser_size=4
        
        self.mask_eraser_size=20
        self.mask_pencil_size=10

        self.curr_tool=None
        self.pre_tool=None

        self.rect_items = []
        self.rect_item = None

        self.dragging = False

        self.points = []
        self.polygon_items = []
        self.current_polygon = None

        self.center_position = QPointF(0, 0)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)

        self.eraser_cursor_item = QGraphicsEllipseItem(0, 0, self.eraser_size, self.eraser_size)
        self.cursor_item=QGraphicsEllipseItem(0, 0, 1, 1)
        self.cursor_item.setZValue(10)

        self.mask_pixmap_item = QGraphicsPixmapItem()  #mask

        self.base_pixmap_item = QGraphicsPixmapItem()  #背景 
        self._sync_view=None

        self.line_start_point=None

        scene=   QGraphicsScene()
        scene.setBackgroundBrush(QColor(255, 255, 255,128))
        self.setScene(scene)
        

        self.setTool('hand') 


    def set_sync_view(self, view):
        self._sync_view = view


    def sync_view(self):
        # self.scale_factor = self.transform().m11()
        # self.center_position = self.mapToScene(self.viewport().rect().center())
        self._sync_view.resetTransform()
        self._sync_view.scale(self.scale_factor, self.scale_factor)
        self._sync_view.centerOn(self.center_position )
        return
    

    def keyPressEvent(self, event):
        # 捕捉按键按下事件
        self.pre_tool = self.curr_tool
        if event.key() == Qt.Key_Control:
            self.setTool('hand')
            
    def keyReleaseEvent(self, event):
        # 捕捉按键释放事件
        if event.key() == Qt.Key_Control:
            self.setTool(self.pre_tool)

    def set_eraser_size(self, size):
        self.eraser_size = size
        self.update_eraser_cursor(self.mapToScene(self.mapFromGlobal(QCursor.pos())))

    def set_mask_eraser_size(self, size):
        self.mask_eraser_size = size
        #self.update_eraser_cursor(self.mapToScene(self.mapFromGlobal(QCursor.pos())))
        rect=QRectF(-size/2, -size/2, size , size)
        
        self.cursor_item.setRect(rect)
        self.cursor_item.setPen(QPen(QColor(0,0,0), 1, Qt.SolidLine))
        self.cursor_item.setBrush(QBrush(QColor(255, 255, 255)))

    def set_mask_pencil_size(self, size):
        self.mask_pencil_size = size
        self.cursor_item.setRect(QRectF(-size/2, -size/2, size , size ))
        #self.cursor_item.setPen(QPen(QColor(0,0,0), 1, Qt.SolidLine))
        self.cursor_item.setBrush(QBrush(QColor(255, 0, 0,128)))

    def setTool(self, tool):
        self.curr_tool = tool
        self.updateCursor()

    def mouseMoveEvent(self, event):
        point=self.mapToScene(event.pos())
        
        if self.cursor_item.scene(): ##move cursor to the current position
            self.cursor_item.setPos(point)

        if self.curr_tool=='eraser' :  
            if not event.buttons() & Qt.LeftButton:
                return  
            pixmap=self.base_pixmap_item.pixmap()     
            pixmap=self.eraseAt(pixmap,point)
            self.base_pixmap_item.setPixmap(pixmap)
        elif self.curr_tool=='mask_eraser' :
            offset=self.mask_eraser_size
            if not event.buttons() & Qt.LeftButton:
                return            
            pixmap=self.mask_pixmap_item.pixmap()
            self.eraseAt(pixmap, point, self.mask_eraser_size)
            self.mask_pixmap_item.setPixmap(pixmap)

        elif self.curr_tool=='mask_pencil' :
            if not event.buttons() & Qt.LeftButton:
                return  
                 
            pixmap=self.mask_pixmap_item.pixmap()
            painter = QPainter(pixmap)
            #painter.setRenderHint(QPainter.Antialiasing)
            pen=QPen(QColor(255, 0, 0, 128), self.mask_pencil_size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            painter.setPen(pen)
            
            painter.setCompositionMode(QPainter.CompositionMode_Source)

            painter.drawLine(self.line_start_point, point)
            painter.end()      
            self.mask_pixmap_item.setPixmap(pixmap)

            self.line_start_point=point

        elif self.curr_tool=='hand' and self.dragging:
            super().mouseMoveEvent(event)

        elif self.curr_tool=='rectangle' :
            if not event.buttons() & Qt.LeftButton:
                return
            if not self.rect_item:
                return
            if point.x()>self.rect_item.rect().topLeft().x():
                rect = QRectF(self.rect_item.rect().topLeft(), point).normalized()
            else:
                rect = QRectF(point, self.rect_item.rect().bottomRight()).normalized()
            self.rect_item.setRect(rect)               

        elif self.curr_tool=='lasso' :
            if not event.buttons() & Qt.LeftButton:
                return
            end_point = point
            polygon = self.current_polygon.polygon()
            polygon.append(end_point)
            self.current_polygon.setPolygon(polygon)
        

    def mouseReleaseEvent(self, event):
        if not (event.button() == Qt.LeftButton):
            return

        if self.erasing:
            self.erasing = False
        elif self.curr_tool=='rectangle':
            self.rect_items.append(self.rect_item)
            self.rect_item = None
        elif self.curr_tool=='hand':
            super().mouseReleaseEvent(event)
            self.dragging = False
            self.save_view_state()

        elif self.curr_tool=='lasso' :
            polygon = self.current_polygon.polygon()
            polygon.append(self.start_point)
            self.current_polygon.setPolygon(polygon)
            self.polygon_items.append(self.current_polygon)
            self.current_polygon = None
        elif self.curr_tool=='mask_pencil':
            self.line_start_point=None
            

    def mousePressEvent(self, event):
        if not event.button() == Qt.LeftButton:
            return
        point=self.mapToScene(event.pos())

        if self.curr_tool=='hand':
            super().mousePressEvent(event)
            self.dragging = True

        elif self.curr_tool=='eraser':  # 橡皮擦状态
            self.erasing = True
            pixmap=self.eraseAt(self.base_pixmap_item.pixmap(), point)
            self.base_pixmap_item.setPixmap(pixmap)

        elif self.curr_tool=='mask_eraser':
            self.erasing = True
            brush = QBrush(QColor(0, 0, 0, 0))  # Transparent black
            pixmap=self.eraseAt(self.mask_pixmap_item.pixmap(), point, self.mask_eraser_size)
            #pixmap=self.drawAt(pixmap, point)
            self.mask_pixmap_item.setPixmap(pixmap)

        elif self.curr_tool=='mask_pencil':            
            self.line_start_point=point

        elif self.curr_tool=='rectangle':     
            
            self.rect_item = QGraphicsRectItem(QRectF(point, point))
            self.rect_item.setPen(QPen(Qt.red, 2, Qt.DashLine))
            self.rect_item.setZValue(10)
            self.scene().addItem(self.rect_item)


        elif self.curr_tool=='lasso':
            self.start_point = point
            self.current_polygon = QGraphicsPolygonItem(QPolygonF([self.start_point]))
            self.current_polygon.setPen(QPen(Qt.red, 2))
            self.current_polygon.setZValue(10)
            self.scene().addItem(self.current_polygon)

        super().mousePressEvent(event)

    def update_polygon(self):
        if self.current_polygon:
            self.scene().removeItem(self.current_polygon)
        
        if self.points:
            polygon = QPolygonF(self.points)
            self.current_polygon = QGraphicsPolygonItem(polygon)
            pen = QPen(Qt.black, 2)
            brush = QBrush(QColor(255, 0, 0, 100))  # Semi-transparent red
            self.current_polygon.setPen(pen)
            self.current_polygon.setBrush(brush)
            self.scene().addItem(self.current_polygon)

    # def create_eraser_cursor(self, size):
    #     pixmap = QPixmap(size, size)
    #     pixmap.fill(Qt.transparent)
    #     painter = QPainter(pixmap)
    #     painter.setRenderHint(QPainter.Antialiasing)
    #     painter.setBrush(Qt.black)
    #     painter.drawEllipse(0, 0, size, size)
    #     painter.end()
    #     return QCursor(pixmap)
    
    def updateCursor(self):
        tool=self.curr_tool
        if tool == 'eraser':
            self.setCursor(Qt.BlankCursor)
            
        if tool == 'hand':
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            if self.cursor_item.scene(): # Remove the eraser cursor
                self.scene().removeItem(self.cursor_item)
                #self.setCursor(Qt.ArrowCursor)
            
        elif tool == 'rectangle' or tool == 'lasso':
            self.setDragMode(QGraphicsView.NoDrag)
            if self.cursor_item.scene(): # Remove the eraser cursor
                self.scene().removeItem(self.cursor_item)
            self.setCursor(Qt.CrossCursor)

        elif tool == 'eraser':
            self.setDragMode(QGraphicsView.NoDrag)
            #self.setCursor(Qt.CrossCursor)

        elif tool == 'mask_eraser':
            pen_size=self.mask_eraser_size
            self.setDragMode(QGraphicsView.NoDrag)
            self.setCursor(Qt.BlankCursor)

            rect = QRectF(-pen_size/2, -pen_size/2, pen_size , pen_size )
            self.cursor_item.setRect(rect)
            self.cursor_item.setPen(QPen(QColor(0,0,0), 1, Qt.SolidLine))
            #brush = QBrush(QColor(255, 0, 0, 128))  # 半透明的红色
            self.cursor_item.setBrush(QBrush(QColor(255, 255, 255)))

            if not self.cursor_item.scene():
                self.scene().addItem(self.cursor_item)

        elif tool == 'mask_pencil':
            pen_size=self.mask_pencil_size
            self.setDragMode(QGraphicsView.NoDrag)
            self.setCursor(Qt.BlankCursor)

            rect = QRectF(-pen_size/2, -pen_size/2, pen_size , pen_size)
            self.cursor_item.setRect(rect)
            #self.cursor_item.setPen(QPen(QColor(255,0,0,128), 1, Qt.SolidLine))
            self.cursor_item.setBrush(QBrush(QColor(255, 0, 0,128)))

            if not self.cursor_item.scene():
                self.scene().addItem(self.cursor_item)

        else:
            self.setDragMode(QGraphicsView.NoDrag)
            if  self.cursor_item.scene():
                self.scene().removeItem(self.cursor_item)



    def eraseAt(self, pixmap, pos, eraser_size):
        painter = QPainter(pixmap)
        #painter.setRenderHint(QPainter.Antialiasing)
        painter.setCompositionMode(QPainter.CompositionMode_Clear)
        painter.setBrush(Qt.transparent)
        painter.drawEllipse(pos, eraser_size / 2, eraser_size / 2)
        painter.end()
        return pixmap
    
    def drawAt(self,pixmap, pos,  brush):

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(brush)
        painter.drawEllipse(pos, self.eraser_size / 2, self.eraser_size / 2)
        painter.end()

        # if self.curr_tool=='mask_eraser':
        #     painter.setCompositionMode(QPainter.CompositionMode_Clear)  # Set composition mode to clear
        #     painter.setBrush(Qt.transparent)             
        #     painter.drawEllipse(pos, self.eraser_size / 2, self.eraser_size / 2)
        #     painter.end()

        # elif self.curr_tool=='eraser':
        #     pen=QPen(Qt.white , 0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        #     brush = QBrush(QColor(Qt.white))
        #     painter.setBrush(brush)

        #     #painter.setCompositionMode(QPainter.CompositionMode_Clear)
        #     painter.setPen(pen)
        #     painter.drawEllipse(pos, self.eraser_size / 2, self.eraser_size / 2)
        #     painter.end()
        #     #self.base_pixmap_item.setPixmap(pixmap)
        return pixmap

    def wheelEvent(self, event):
        self.factor = 1.15 if event.angleDelta().y() > 0 else 1 / 1.15

        self.scale( self.factor, self.factor)
        if self.curr_tool=='eraser':
            #self.eraser_size *= factor
            point=self.mapToScene(event.pos())
            self.update_eraser_cursor(point)    
        
        self.save_view_state()
        super().wheelEvent(event)

    def save_view_state(self):
        self.scale_factor = self.transform().m11()
        self.center_position = self.mapToScene(self.viewport().rect().center())
        if self._sync_view:
            self.sync_view()

    def restore_view_state(self):
        self.resetTransform()
        self.scale(self.scale_factor, self.scale_factor)
        self.centerOn(self.center_position)
        if self._sync_view:
            self.sync_view()