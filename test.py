import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QLabel, QHBoxLayout, QWidget, QFileDialog, QDesktopWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class ImageDisplay(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("border: 1px solid black")
        self.pixmap = None

    def setImage(self, imagePath):
        self.pixmap = QPixmap(imagePath)
        self.updatePixmap()

    def resizeEvent(self, event):
        pass
    def eventFilter(self, obj, event):
        if event.type() == event.Resize:
            # 过滤掉resizeEvent事件
            return True
        return super().eventFilter(obj, event)
    
    def updatePixmap(self):
        print(self.size(), 'label size:')
        if self.pixmap:
            scaledPixmap = self.pixmap.scaled(self.size(), Qt.KeepAspectRatio)
            self.setPixmap(scaledPixmap)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def setWindow(self):
        screen = QDesktopWidget().screenGeometry()
        window_width = screen.width() 
        window_height = screen.height() 
        self.setGeometry(screen.center().x() - window_width // 2, screen.center().y() - window_height // 2, window_width, window_height)


    def initUI(self):
        self.setWindowTitle('Image Viewer')
        #self.setWindow()

        # Create toolbar
        openAction = QAction('打开', self)
        openAction.triggered.connect(self.openFileDialog)

        thresholdAction = QAction('threshold', self)
        plusAction = QAction('+', self)
        minusAction = QAction('-', self)

        toolbar = self.addToolBar('Toolbar')
        toolbar.addAction(openAction)
        toolbar.addSeparator()
        toolbar.addAction(thresholdAction)
        toolbar.addAction(plusAction)
        toolbar.addAction(minusAction)

        # Create image display widgets
        self.imageDisplay1 = ImageDisplay()
        self.imageDisplay1.installEventFilter(self.imageDisplay1)

        self.imageDisplay2 = ImageDisplay()
        self.imageDisplay2.installEventFilter(self.imageDisplay2)

        # Create layout
        hbox = QHBoxLayout()
        hbox.addWidget(self.imageDisplay1)
        hbox.addWidget(self.imageDisplay2)

        container = QWidget()
        container.setLayout(hbox)

        self.setCentralWidget(container)
        self.showMaximized()
    def resizeEvent(self, event):
        pass
        #self.imageDisplay1.updatePixmap()


    def openFileDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.png *.jpg *.bmp)", options=options)
        if fileName:
            self.imageDisplay1.setImage(fileName)
            #self.imageDisplay2.setImage(fileName)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
