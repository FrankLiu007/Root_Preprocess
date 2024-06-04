import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QHBoxLayout, QAction, QMenuBar, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class ImageWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        # 初始化pixmap对象为空
        self.pixmap1 = QPixmap()
        self.pixmap2 = QPixmap()

    def initUI(self):
        # 创建菜单栏和加载图片的操作
        self.menuBar = self.menuBar()
        fileMenu = self.menuBar.addMenu('文件')
        loadAction = QAction('加载图片', self)
        loadAction.triggered.connect(self.loadImages)
        fileMenu.addAction(loadAction)

        # 创建一个中央窗口部件和水平布局
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        layout = QHBoxLayout(centralWidget)

        # 创建两个QLabel用于显示图片
        self.label1 = QLabel(self)
        self.label2 = QLabel(self)

        # 设置标签的对齐方式为居中
        self.label1.setAlignment(Qt.AlignCenter)
        self.label2.setAlignment(Qt.AlignCenter)

        # 为两个标签添加到布局中
        layout.addWidget(self.label1, 1)  # 添加拉伸因子
        layout.addWidget(self.label2, 1)  # 添加拉伸因子

        # 设置窗口的标题和初始大小
        self.setWindowTitle('双图片视图')
        self.resize(800, 400)
        self.setMinimumSize(400, 200)  # 设置最小尺寸

    def loadImages(self):
        # 弹出文件对话框让用户选择图片
        imagePath1, _ = QFileDialog.getOpenFileName(self, "选择第一张图片", "", "Image files (*.jpg *.png)")
        imagePath2 = imagePath1

        if imagePath1:
            # 加载并保存原始图片
            self.pixmap1 = QPixmap(imagePath1)
            self.pixmap2 = QPixmap(imagePath2)
            self.updateImages()
        else:
            print("未选择图片或选择图片失败")

    def updateImages(self):
        if not self.pixmap1.isNull() and not self.pixmap2.isNull():
            # 根据标签的当前大小调整图片大小
            scaled_pixmap1 = self.pixmap1.scaled(self.label1.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            scaled_pixmap2 = self.pixmap2.scaled(self.label2.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label1.setPixmap(scaled_pixmap1)
            self.label2.setPixmap(scaled_pixmap2)

    def resizeEvent(self, event):
        # 窗口大小变化时更新图片大小
        self.updateImages()

app = QApplication(sys.argv)
ex = ImageWidget()
ex.show()
sys.exit(app.exec_())