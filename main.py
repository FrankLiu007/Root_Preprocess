import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QAction, QToolBar, QMainWindow, QFileDialog
from PyQt5.QtGui import QPixmap

class ImageDisplay(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Image Display')
        self.setGeometry(100, 100, 400, 200)

        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        open_action = QAction('Open', self)
        open_action.triggered.connect(self.openImage)
        self.toolbar.addAction(open_action)

        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        self.toolbar.addAction(exit_action)

        layout = QVBoxLayout()

        self.label1 = QLabel("放大")
        layout.addWidget(self.label1)

        self.label2 = QLabel("缩小")
        layout.addWidget(self.label2)

        self.setLayout(layout)

    def openImage(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)
        if file_path:
            pixmap = QPixmap(file_path)
            self.label1.setPixmap(pixmap)
            self.label2.setPixmap(pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageDisplay()
    window.show()
    sys.exit(app.exec_())