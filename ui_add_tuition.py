# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_add_tuition.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(700, 622)
        Dialog.setMinimumSize(QtCore.QSize(700, 620))
        Dialog.setMaximumSize(QtCore.QSize(720, 640))
        font = QtGui.QFont()
        font.setPointSize(12)
        Dialog.setFont(font)
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 681, 600))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_23 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_23.setFont(font)
        self.label_23.setObjectName("label_23")
        self.gridLayout.addWidget(self.label_23, 0, 0, 1, 1)
        self.comboBox_2 = QtWidgets.QComboBox(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comboBox_2.setFont(font)
        self.comboBox_2.setObjectName("comboBox_2")
        self.gridLayout.addWidget(self.comboBox_2, 1, 2, 1, 1)
        self.comboBox_1 = QtWidgets.QComboBox(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comboBox_1.setFont(font)
        self.comboBox_1.setObjectName("comboBox_1")
        self.gridLayout.addWidget(self.comboBox_1, 1, 1, 1, 1)
        self.label_25 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setKerning(True)
        self.label_25.setFont(font)
        self.label_25.setObjectName("label_25")
        self.gridLayout.addWidget(self.label_25, 0, 2, 1, 1)
        self.label_24 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_24.setFont(font)
        self.label_24.setObjectName("label_24")
        self.gridLayout.addWidget(self.label_24, 0, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.line_2 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_2.addWidget(self.line_2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.lcdNumber = QtWidgets.QLCDNumber(self.verticalLayoutWidget)
        self.lcdNumber.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lcdNumber.setFont(font)
        self.lcdNumber.setObjectName("lcdNumber")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lcdNumber)
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.lineEdit_11 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_11.setFont(font)
        self.lineEdit_11.setObjectName("lineEdit_11")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_11)
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.dateEdit_11 = QtWidgets.QDateEdit(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.dateEdit_11.setFont(font)
        self.dateEdit_11.setObjectName("dateEdit_11")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.dateEdit_11)
        self.label_6 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.comboBox_13 = QtWidgets.QComboBox(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comboBox_13.setFont(font)
        self.comboBox_13.setObjectName("comboBox_13")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.comboBox_13)
        self.label_7 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.timeEdit_14 = QtWidgets.QTimeEdit(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.timeEdit_14.setFont(font)
        self.timeEdit_14.setWrapping(False)
        self.timeEdit_14.setSpecialValueText("")
        self.timeEdit_14.setObjectName("timeEdit_14")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.timeEdit_14)
        self.label_8 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.spinBox_15 = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.spinBox_15.setFont(font)
        self.spinBox_15.setMaximum(300)
        self.spinBox_15.setSingleStep(15)
        self.spinBox_15.setObjectName("spinBox_15")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.spinBox_15)
        self.label_9 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.doubleSpinBox_16 = QtWidgets.QDoubleSpinBox(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.doubleSpinBox_16.setFont(font)
        self.doubleSpinBox_16.setPrefix("")
        self.doubleSpinBox_16.setObjectName("doubleSpinBox_16")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBox_16)
        self.label_10 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.label_10)
        self.spinBox_17 = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.spinBox_17.setFont(font)
        self.spinBox_17.setObjectName("spinBox_17")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.spinBox_17)
        self.doubleSpinBox_19b = QtWidgets.QDoubleSpinBox(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.doubleSpinBox_19b.setFont(font)
        self.doubleSpinBox_19b.setObjectName("doubleSpinBox_19b")
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBox_19b)
        self.doubleSpinBox_18 = QtWidgets.QDoubleSpinBox(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.doubleSpinBox_18.setFont(font)
        self.doubleSpinBox_18.setObjectName("doubleSpinBox_18")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBox_18)
        self.comboBox_19a = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.comboBox_19a.setEditable(True)
        self.comboBox_19a.setObjectName("comboBox_19a")
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.LabelRole, self.comboBox_19a)
        self.label_13 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.label_13)
        self.horizontalLayout_2.addLayout(self.formLayout)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.formLayout_3 = QtWidgets.QFormLayout()
        self.formLayout_3.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_3.setSpacing(6)
        self.formLayout_3.setObjectName("formLayout_3")
        self.comboBox_22a = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.comboBox_22a.setEditable(True)
        self.comboBox_22a.setObjectName("comboBox_22a")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.comboBox_22a)
        self.doubleSpinBox_22b = QtWidgets.QDoubleSpinBox(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.doubleSpinBox_22b.setFont(font)
        self.doubleSpinBox_22b.setObjectName("doubleSpinBox_22b")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBox_22b)
        self.totalCostLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.totalCostLabel.setObjectName("totalCostLabel")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.totalCostLabel)
        self.doubleSpinBox_23b = QtWidgets.QDoubleSpinBox(self.verticalLayoutWidget)
        self.doubleSpinBox_23b.setMaximum(150.0)
        self.doubleSpinBox_23b.setObjectName("doubleSpinBox_23b")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBox_23b)
        self.label_28 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_28.setFont(font)
        self.label_28.setObjectName("label_28")
        self.formLayout_3.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_28)
        self.comboBox_24b = QtWidgets.QComboBox(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comboBox_24b.setFont(font)
        self.comboBox_24b.setObjectName("comboBox_24b")
        self.formLayout_3.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.comboBox_24b)
        self.label_30 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_30.setFont(font)
        self.label_30.setObjectName("label_30")
        self.formLayout_3.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_30)
        self.comboBox_25b = QtWidgets.QComboBox(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comboBox_25b.setFont(font)
        self.comboBox_25b.setObjectName("comboBox_25b")
        self.formLayout_3.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.comboBox_25b)
        self.label_31 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_31.setFont(font)
        self.label_31.setObjectName("label_31")
        self.formLayout_3.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_31)
        self.comboBox_26b = QtWidgets.QComboBox(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comboBox_26b.setFont(font)
        self.comboBox_26b.setObjectName("comboBox_26b")
        self.formLayout_3.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.comboBox_26b)
        self.label_32 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_32.setFont(font)
        self.label_32.setObjectName("label_32")
        self.formLayout_3.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.label_32)
        self.label_33 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_33.setFont(font)
        self.label_33.setObjectName("label_33")
        self.formLayout_3.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.label_33)
        self.comboBox_28b = QtWidgets.QComboBox(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comboBox_28b.setFont(font)
        self.comboBox_28b.setObjectName("comboBox_28b")
        self.formLayout_3.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.comboBox_28b)
        self.label_34 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_34.setFont(font)
        self.label_34.setObjectName("label_34")
        self.formLayout_3.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.label_34)
        self.lineEdit_29b = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_29b.setFont(font)
        self.lineEdit_29b.setObjectName("lineEdit_29b")
        self.formLayout_3.setWidget(9, QtWidgets.QFormLayout.FieldRole, self.lineEdit_29b)
        self.doubleSpinBox_21b = QtWidgets.QDoubleSpinBox(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.doubleSpinBox_21b.setFont(font)
        self.doubleSpinBox_21b.setObjectName("doubleSpinBox_21b")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBox_21b)
        self.comboBox_21a = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.comboBox_21a.setEditable(True)
        self.comboBox_21a.setObjectName("comboBox_21a")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.comboBox_21a)
        self.dateEdit_27b = QtWidgets.QDateEdit(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.dateEdit_27b.setFont(font)
        self.dateEdit_27b.setObjectName("dateEdit_27b")
        self.formLayout_3.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.dateEdit_27b)
        self.horizontalLayout_2.addLayout(self.formLayout_3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.line = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(250, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pButton_Add_more = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pButton_Add_more.setObjectName("pButton_Add_more")
        self.horizontalLayout.addWidget(self.pButton_Add_more)
        self.pButton_Add = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pButton_Add.setFont(font)
        self.pButton_Add.setObjectName("pButton_Add")
        self.horizontalLayout.addWidget(self.pButton_Add)
        self.pButton_Cancel = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pButton_Cancel.setFont(font)
        self.pButton_Cancel.setObjectName("pButton_Cancel")
        self.horizontalLayout.addWidget(self.pButton_Cancel)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 1)
        self.verticalLayout_2.setStretch(2, 1)
        self.verticalLayout_2.setStretch(3, 1)
        self.verticalLayout_2.setStretch(4, 1)
        self.label_23.setBuddy(self.comboBox_1)
        self.label_25.setBuddy(self.comboBox_2)
        self.label_24.setBuddy(self.comboBox_1)
        self.label.setBuddy(self.lineEdit_11)
        self.label_2.setBuddy(self.lineEdit_11)
        self.label_4.setBuddy(self.dateEdit_11)
        self.label_6.setBuddy(self.comboBox_13)
        self.label_7.setBuddy(self.timeEdit_14)
        self.label_8.setBuddy(self.spinBox_15)
        self.label_9.setBuddy(self.doubleSpinBox_16)
        self.label_10.setBuddy(self.spinBox_17)
        self.label_13.setBuddy(self.doubleSpinBox_18)
        self.label_28.setBuddy(self.comboBox_24b)
        self.label_30.setBuddy(self.comboBox_25b)
        self.label_31.setBuddy(self.comboBox_26b)
        self.label_33.setBuddy(self.comboBox_28b)
        self.label_34.setBuddy(self.lineEdit_29b)

        self.retranslateUi(Dialog)
        self.pButton_Cancel.clicked.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.comboBox_1, self.comboBox_2)
        Dialog.setTabOrder(self.comboBox_2, self.lineEdit_11)
        Dialog.setTabOrder(self.lineEdit_11, self.dateEdit_11)
        Dialog.setTabOrder(self.dateEdit_11, self.comboBox_13)
        Dialog.setTabOrder(self.comboBox_13, self.timeEdit_14)
        Dialog.setTabOrder(self.timeEdit_14, self.spinBox_15)
        Dialog.setTabOrder(self.spinBox_15, self.doubleSpinBox_16)
        Dialog.setTabOrder(self.doubleSpinBox_16, self.spinBox_17)
        Dialog.setTabOrder(self.spinBox_17, self.comboBox_24b)
        Dialog.setTabOrder(self.comboBox_24b, self.comboBox_25b)
        Dialog.setTabOrder(self.comboBox_25b, self.comboBox_26b)
        Dialog.setTabOrder(self.comboBox_26b, self.comboBox_28b)
        Dialog.setTabOrder(self.comboBox_28b, self.lineEdit_29b)
        Dialog.setTabOrder(self.lineEdit_29b, self.pButton_Add)
        Dialog.setTabOrder(self.pButton_Add, self.pButton_Cancel)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Add Tuition Record"))
        self.label_23.setText(_translate("Dialog", "Choose Student:"))
        self.label_25.setText(_translate("Dialog", "&last name"))
        self.label_24.setText(_translate("Dialog", "first &name"))
        self.label.setText(_translate("Dialog", "student id"))
        self.label_2.setText(_translate("Dialog", "&unique tuition id"))
        self.label_4.setText(_translate("Dialog", "&tuition date"))
        self.label_6.setText(_translate("Dialog", "tuition wee&k day"))
        self.label_7.setText(_translate("Dialog", "start time"))
        self.label_8.setText(_translate("Dialog", "&duration"))
        self.label_9.setText(_translate("Dialog", "travel distance"))
        self.doubleSpinBox_16.setSuffix(_translate("Dialog", " miles"))
        self.label_10.setText(_translate("Dialog", "fees per hour"))
        self.spinBox_17.setPrefix(_translate("Dialog", "£ "))
        self.doubleSpinBox_19b.setPrefix(_translate("Dialog", "£ "))
        self.doubleSpinBox_18.setPrefix(_translate("Dialog", "£ "))
        self.label_13.setText(_translate("Dialog", "discount"))
        self.doubleSpinBox_22b.setPrefix(_translate("Dialog", "£ "))
        self.totalCostLabel.setText(_translate("Dialog", "total cost"))
        self.doubleSpinBox_23b.setPrefix(_translate("Dialog", "£ "))
        self.label_28.setText(_translate("Dialog", "travel method"))
        self.label_30.setText(_translate("Dialog", "pa&yment method"))
        self.label_31.setText(_translate("Dialog", "payment received"))
        self.label_32.setText(_translate("Dialog", "payment date"))
        self.label_33.setText(_translate("Dialog", "receipt completed"))
        self.label_34.setText(_translate("Dialog", "invoice number"))
        self.doubleSpinBox_21b.setPrefix(_translate("Dialog", "£ "))
        self.pButton_Add_more.setText(_translate("Dialog", "Add more"))
        self.pButton_Add.setText(_translate("Dialog", "Add"))
        self.pButton_Cancel.setText(_translate("Dialog", "Cancel"))
