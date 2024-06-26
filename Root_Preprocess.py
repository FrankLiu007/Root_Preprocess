# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\Root_Preprocess.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1683, 1015)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_4 = QtWidgets.QFrame(self.frame_3)
        self.frame_4.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.open_img_btn = QtWidgets.QPushButton(self.frame_4)
        self.open_img_btn.setMinimumSize(QtCore.QSize(100, 40))
        self.open_img_btn.setObjectName("open_img_btn")
        self.horizontalLayout.addWidget(self.open_img_btn)
        self.previous_img_btn = QtWidgets.QPushButton(self.frame_4)
        self.previous_img_btn.setMinimumSize(QtCore.QSize(100, 40))
        self.previous_img_btn.setObjectName("previous_img_btn")
        self.horizontalLayout.addWidget(self.previous_img_btn)
        self.next_img_btn = QtWidgets.QPushButton(self.frame_4)
        self.next_img_btn.setMinimumSize(QtCore.QSize(100, 40))
        self.next_img_btn.setObjectName("next_img_btn")
        self.horizontalLayout.addWidget(self.next_img_btn)
        self.label_4 = QtWidgets.QLabel(self.frame_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setTextFormat(QtCore.Qt.PlainText)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.spinBox = QtWidgets.QSpinBox(self.frame_4)
        self.spinBox.setMinimumSize(QtCore.QSize(60, 40))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        self.spinBox.setFont(font)
        self.spinBox.setMinimum(3)
        self.spinBox.setMaximum(21)
        self.spinBox.setSingleStep(2)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout.addWidget(self.spinBox)
        self.filter_img_btn = QtWidgets.QPushButton(self.frame_4)
        self.filter_img_btn.setMinimumSize(QtCore.QSize(100, 40))
        self.filter_img_btn.setObjectName("filter_img_btn")
        self.horizontalLayout.addWidget(self.filter_img_btn)
        self.filter_img_btn_2 = QtWidgets.QPushButton(self.frame_4)
        self.filter_img_btn_2.setMinimumSize(QtCore.QSize(100, 40))
        self.filter_img_btn_2.setObjectName("filter_img_btn_2")
        self.horizontalLayout.addWidget(self.filter_img_btn_2)
        self.confirm_btn = QtWidgets.QPushButton(self.frame_4)
        self.confirm_btn.setMinimumSize(QtCore.QSize(100, 40))
        self.confirm_btn.setObjectName("confirm_btn")
        self.horizontalLayout.addWidget(self.confirm_btn)
        self.label_5 = QtWidgets.QLabel(self.frame_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        self.label_5.setFont(font)
        self.label_5.setTextFormat(QtCore.Qt.PlainText)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout.addWidget(self.label_5)
        self.label_2 = QtWidgets.QLabel(self.frame_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setTextFormat(QtCore.Qt.PlainText)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.frame_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.horizontalSlider = QtWidgets.QSlider(self.frame_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalSlider.sizePolicy().hasHeightForWidth())
        self.horizontalSlider.setSizePolicy(sizePolicy)
        self.horizontalSlider.setMinimumSize(QtCore.QSize(100, 0))
        self.horizontalSlider.setMaximum(255)
        self.horizontalSlider.setProperty("value", 200)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalLayout.addWidget(self.horizontalSlider)
        self.lineEdit = QtWidgets.QLineEdit(self.frame_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setMinimumSize(QtCore.QSize(20, 40))
        self.lineEdit.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.minus_btn = QtWidgets.QPushButton(self.frame_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.minus_btn.sizePolicy().hasHeightForWidth())
        self.minus_btn.setSizePolicy(sizePolicy)
        self.minus_btn.setMinimumSize(QtCore.QSize(62, 40))
        self.minus_btn.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\../Downloads/minus-symbol.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.minus_btn.setIcon(icon)
        self.minus_btn.setObjectName("minus_btn")
        self.horizontalLayout.addWidget(self.minus_btn)
        self.plus_btn = QtWidgets.QPushButton(self.frame_4)
        self.plus_btn.setEnabled(True)
        self.plus_btn.setMinimumSize(QtCore.QSize(60, 40))
        self.plus_btn.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(".\\../Downloads/add (2).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.plus_btn.setIcon(icon1)
        self.plus_btn.setFlat(False)
        self.plus_btn.setObjectName("plus_btn")
        self.horizontalLayout.addWidget(self.plus_btn)
        self.threshold_apply_btn = QtWidgets.QPushButton(self.frame_4)
        self.threshold_apply_btn.setMinimumSize(QtCore.QSize(60, 40))
        self.threshold_apply_btn.setObjectName("threshold_apply_btn")
        self.horizontalLayout.addWidget(self.threshold_apply_btn)
        self.export_img_btn = QtWidgets.QPushButton(self.frame_4)
        self.export_img_btn.setMinimumSize(QtCore.QSize(100, 40))
        self.export_img_btn.setObjectName("export_img_btn")
        self.horizontalLayout.addWidget(self.export_img_btn)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout.addWidget(self.frame_4)
        self.frame_2 = QtWidgets.QFrame(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setMinimumSize(QtCore.QSize(800, 800))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.widget = QtWidgets.QWidget(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName("widget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.graphicsView = QtWidgets.QGraphicsView(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy)
        self.graphicsView.setMinimumSize(QtCore.QSize(800, 800))
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout_4.addWidget(self.graphicsView)
        self.horizontalLayout_2.addWidget(self.widget)
        self.widget_2 = QtWidgets.QWidget(self.frame_2)
        self.widget_2.setBaseSize(QtCore.QSize(300, 400))
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.graphicsView_2 = QtWidgets.QGraphicsView(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView_2.sizePolicy().hasHeightForWidth())
        self.graphicsView_2.setSizePolicy(sizePolicy)
        self.graphicsView_2.setMinimumSize(QtCore.QSize(800, 800))
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.horizontalLayout_5.addWidget(self.graphicsView_2)
        self.horizontalLayout_2.addWidget(self.widget_2)
        self.verticalLayout.addWidget(self.frame_2, 0, QtCore.Qt.AlignTop)
        self.horizontalLayout_3.addWidget(self.frame_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionhand = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(".\\../Downloads/hand.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon2.addPixmap(QtGui.QPixmap(".\\../Downloads/palm-of-hand.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionhand.setIcon(icon2)
        self.actionhand.setObjectName("actionhand")
        self.actioneraser = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(".\\../Downloads/eraser.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actioneraser.setIcon(icon3)
        self.actioneraser.setObjectName("actioneraser")
        self.toolBar.addAction(self.actionhand)
        self.toolBar.addAction(self.actioneraser)
        self.toolBar.addSeparator()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.open_img_btn.setText(_translate("MainWindow", "打开图片"))
        self.previous_img_btn.setText(_translate("MainWindow", "上一张图片"))
        self.next_img_btn.setText(_translate("MainWindow", "下一张图片"))
        self.label_4.setText(_translate("MainWindow", "1. 预处理"))
        self.filter_img_btn.setText(_translate("MainWindow", "中值滤波"))
        self.filter_img_btn_2.setText(_translate("MainWindow", "高斯滤波"))
        self.confirm_btn.setText(_translate("MainWindow", "确定"))
        self.label_5.setText(_translate("MainWindow", "2. 二值化"))
        self.label_2.setText(_translate("MainWindow", "threshold"))
        self.label.setText(_translate("MainWindow", "threshold"))
        self.threshold_apply_btn.setText(_translate("MainWindow", "Apply"))
        self.export_img_btn.setText(_translate("MainWindow", "导出"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionhand.setText(_translate("MainWindow", "手型工具"))
        self.actioneraser.setText(_translate("MainWindow", "eraser"))
