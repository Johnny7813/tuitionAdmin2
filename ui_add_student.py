# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_add_student.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(700, 567)
        Dialog.setMinimumSize(QtCore.QSize(621, 498))
        Dialog.setMaximumSize(QtCore.QSize(700, 800))
        font = QtGui.QFont()
        font.setPointSize(12)
        Dialog.setFont(font)
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 701, 561))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scrollArea = QtWidgets.QScrollArea(self.verticalLayoutWidget)
        self.scrollArea.setWidgetResizable(False)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 665, 675))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.layoutWidget = QtWidgets.QWidget(self.scrollAreaWidgetContents_2)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 651, 652))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setRowWrapPolicy(QtWidgets.QFormLayout.DontWrapRows)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.formLayout.setObjectName("formLayout")
        self.label_11 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_11)
        self.lcdNumber = QtWidgets.QLCDNumber(self.layoutWidget)
        self.lcdNumber.setEnabled(True)
        self.lcdNumber.setMinimumSize(QtCore.QSize(60, 40))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lcdNumber.setFont(font)
        self.lcdNumber.setLineWidth(2)
        self.lcdNumber.setMidLineWidth(1)
        self.lcdNumber.setDigitCount(3)
        self.lcdNumber.setSegmentStyle(QtWidgets.QLCDNumber.Outline)
        self.lcdNumber.setProperty("intValue", 4)
        self.lcdNumber.setObjectName("lcdNumber")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lcdNumber)
        self.label_12 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_12)
        self.lineEdit_11 = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_11.setFont(font)
        self.lineEdit_11.setObjectName("lineEdit_11")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_11)
        self.label_13 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_13)
        self.label_14 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_14)
        self.label_15 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_15)
        self.label_17 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_17.setFont(font)
        self.label_17.setObjectName("label_17")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.label_17)
        self.label_18 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.label_18)
        self.label_19 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_19.setFont(font)
        self.label_19.setObjectName("label_19")
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.LabelRole, self.label_19)
        self.label_1A = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_1A.setFont(font)
        self.label_1A.setObjectName("label_1A")
        self.formLayout.setWidget(11, QtWidgets.QFormLayout.LabelRole, self.label_1A)
        self.label_1B = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_1B.setFont(font)
        self.label_1B.setObjectName("label_1B")
        self.formLayout.setWidget(12, QtWidgets.QFormLayout.LabelRole, self.label_1B)
        self.label_1C = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_1C.setFont(font)
        self.label_1C.setObjectName("label_1C")
        self.formLayout.setWidget(13, QtWidgets.QFormLayout.LabelRole, self.label_1C)
        self.label_1D = QtWidgets.QLabel(self.layoutWidget)
        self.label_1D.setObjectName("label_1D")
        self.formLayout.setWidget(14, QtWidgets.QFormLayout.LabelRole, self.label_1D)
        self.label_1E = QtWidgets.QLabel(self.layoutWidget)
        self.label_1E.setObjectName("label_1E")
        self.formLayout.setWidget(15, QtWidgets.QFormLayout.LabelRole, self.label_1E)
        self.label_1F = QtWidgets.QLabel(self.layoutWidget)
        self.label_1F.setObjectName("label_1F")
        self.formLayout.setWidget(16, QtWidgets.QFormLayout.LabelRole, self.label_1F)
        self.dateEdit = QtWidgets.QDateEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.dateEdit.setFont(font)
        self.dateEdit.setObjectName("dateEdit")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.dateEdit)
        self.dateEdit_2 = QtWidgets.QDateEdit(self.layoutWidget)
        self.dateEdit_2.setMinimumDate(QtCore.QDate(1752, 9, 16))
        self.dateEdit_2.setObjectName("dateEdit_2")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.FieldRole, self.dateEdit_2)
        self.lineEdit_12 = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_12.setObjectName("lineEdit_12")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_12)
        self.lineEdit_16 = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_16.setObjectName("lineEdit_16")
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.FieldRole, self.lineEdit_16)
        self.lineEdit_17 = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_17.setObjectName("lineEdit_17")
        self.formLayout.setWidget(11, QtWidgets.QFormLayout.FieldRole, self.lineEdit_17)
        self.lineEdit_18 = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_18.setObjectName("lineEdit_18")
        self.formLayout.setWidget(12, QtWidgets.QFormLayout.FieldRole, self.lineEdit_18)
        self.lineEdit_19 = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_19.setObjectName("lineEdit_19")
        self.formLayout.setWidget(13, QtWidgets.QFormLayout.FieldRole, self.lineEdit_19)
        self.lineEdit_1A = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_1A.setObjectName("lineEdit_1A")
        self.formLayout.setWidget(14, QtWidgets.QFormLayout.FieldRole, self.lineEdit_1A)
        self.lineEdit_1B = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_1B.setObjectName("lineEdit_1B")
        self.formLayout.setWidget(15, QtWidgets.QFormLayout.FieldRole, self.lineEdit_1B)
        self.doubleSpinBox_11 = QtWidgets.QDoubleSpinBox(self.layoutWidget)
        self.doubleSpinBox_11.setObjectName("doubleSpinBox_11")
        self.formLayout.setWidget(16, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBox_11)
        self.lineEdit_14 = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_14.setObjectName("lineEdit_14")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.lineEdit_14)
        self.lineEdit_13 = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_13.setObjectName("lineEdit_13")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.lineEdit_13)
        self.lineEdit_15 = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_15.setObjectName("lineEdit_15")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.lineEdit_15)
        self.label_16 = QtWidgets.QLabel(self.layoutWidget)
        self.label_16.setObjectName("label_16")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_16)
        self.horizontalLayout_2.addLayout(self.formLayout)
        spacerItem = QtWidgets.QSpacerItem(13, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.formLayout_3 = QtWidgets.QFormLayout()
        self.formLayout_3.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_3.setSpacing(6)
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_21 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_21.setFont(font)
        self.label_21.setObjectName("label_21")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_21)
        self.doubleSpinBox_21 = QtWidgets.QDoubleSpinBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.doubleSpinBox_21.setFont(font)
        self.doubleSpinBox_21.setMinimum(20.0)
        self.doubleSpinBox_21.setSingleStep(1.0)
        self.doubleSpinBox_21.setProperty("value", 30.0)
        self.doubleSpinBox_21.setObjectName("doubleSpinBox_21")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBox_21)
        self.label_22 = QtWidgets.QLabel(self.layoutWidget)
        self.label_22.setObjectName("label_22")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_22)
        self.doubleSpinBox_22 = QtWidgets.QDoubleSpinBox(self.layoutWidget)
        self.doubleSpinBox_22.setObjectName("doubleSpinBox_22")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBox_22)
        self.label_24 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_24.setFont(font)
        self.label_24.setObjectName("label_24")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_24)
        self.label_25 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_25.setFont(font)
        self.label_25.setObjectName("label_25")
        self.formLayout_3.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_25)
        self.comboBox_22 = QtWidgets.QComboBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comboBox_22.setFont(font)
        self.comboBox_22.setObjectName("comboBox_22")
        self.formLayout_3.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.comboBox_22)
        self.label_27 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_27.setFont(font)
        self.label_27.setObjectName("label_27")
        self.formLayout_3.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_27)
        self.comboBox_23 = QtWidgets.QComboBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comboBox_23.setFont(font)
        self.comboBox_23.setObjectName("comboBox_23")
        self.formLayout_3.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.comboBox_23)
        self.label_28 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_28.setFont(font)
        self.label_28.setObjectName("label_28")
        self.formLayout_3.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.label_28)
        self.timeEdit = QtWidgets.QTimeEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.timeEdit.setFont(font)
        self.timeEdit.setWrapping(False)
        self.timeEdit.setSpecialValueText("")
        self.timeEdit.setTime(QtCore.QTime(14, 0, 0))
        self.timeEdit.setObjectName("timeEdit")
        self.formLayout_3.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.timeEdit)
        self.label_29 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_29.setFont(font)
        self.label_29.setObjectName("label_29")
        self.formLayout_3.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.label_29)
        self.spinBox_25 = QtWidgets.QSpinBox(self.layoutWidget)
        self.spinBox_25.setMaximum(240)
        self.spinBox_25.setSingleStep(30)
        self.spinBox_25.setObjectName("spinBox_25")
        self.formLayout_3.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.spinBox_25)
        self.label_2A = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2A.setFont(font)
        self.label_2A.setObjectName("label_2A")
        self.formLayout_3.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.label_2A)
        self.comboBox_24 = QtWidgets.QComboBox(self.layoutWidget)
        self.comboBox_24.setObjectName("comboBox_24")
        self.formLayout_3.setWidget(9, QtWidgets.QFormLayout.FieldRole, self.comboBox_24)
        self.label_2B = QtWidgets.QLabel(self.layoutWidget)
        self.label_2B.setObjectName("label_2B")
        self.formLayout_3.setWidget(10, QtWidgets.QFormLayout.LabelRole, self.label_2B)
        self.comboBox_25 = QtWidgets.QComboBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comboBox_25.setFont(font)
        self.comboBox_25.setObjectName("comboBox_25")
        self.formLayout_3.setWidget(10, QtWidgets.QFormLayout.FieldRole, self.comboBox_25)
        self.label_2C = QtWidgets.QLabel(self.layoutWidget)
        self.label_2C.setObjectName("label_2C")
        self.formLayout_3.setWidget(11, QtWidgets.QFormLayout.LabelRole, self.label_2C)
        self.lineEdit_21 = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_21.setObjectName("lineEdit_21")
        self.formLayout_3.setWidget(11, QtWidgets.QFormLayout.FieldRole, self.lineEdit_21)
        self.label_2D = QtWidgets.QLabel(self.layoutWidget)
        self.label_2D.setObjectName("label_2D")
        self.formLayout_3.setWidget(12, QtWidgets.QFormLayout.LabelRole, self.label_2D)
        self.spinBox_26 = QtWidgets.QSpinBox(self.layoutWidget)
        self.spinBox_26.setObjectName("spinBox_26")
        self.formLayout_3.setWidget(12, QtWidgets.QFormLayout.FieldRole, self.spinBox_26)
        self.label_2E = QtWidgets.QLabel(self.layoutWidget)
        self.label_2E.setObjectName("label_2E")
        self.formLayout_3.setWidget(13, QtWidgets.QFormLayout.LabelRole, self.label_2E)
        self.lineEdit_22 = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_22.setObjectName("lineEdit_22")
        self.formLayout_3.setWidget(13, QtWidgets.QFormLayout.FieldRole, self.lineEdit_22)
        self.comboBox_21 = QtWidgets.QComboBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comboBox_21.setFont(font)
        self.comboBox_21.setObjectName("comboBox_21")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.comboBox_21)
        self.label_23 = QtWidgets.QLabel(self.layoutWidget)
        self.label_23.setObjectName("label_23")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_23)
        self.doubleSpinBox_23 = QtWidgets.QDoubleSpinBox(self.layoutWidget)
        self.doubleSpinBox_23.setObjectName("doubleSpinBox_23")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBox_23)
        self.doubleSpinBox_24 = QtWidgets.QDoubleSpinBox(self.layoutWidget)
        self.doubleSpinBox_24.setObjectName("doubleSpinBox_24")
        self.formLayout_3.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBox_24)
        self.label_26 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_26.setFont(font)
        self.label_26.setObjectName("label_26")
        self.formLayout_3.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_26)
        self.horizontalLayout_2.addLayout(self.formLayout_3)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout_2.addWidget(self.scrollArea)
        self.line = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(350, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
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
        self.label_11.setBuddy(self.lineEdit_11)
        self.label_12.setBuddy(self.lineEdit_11)
        self.label_13.setBuddy(self.lineEdit_12)
        self.label_14.setBuddy(self.lineEdit_13)
        self.label_15.setBuddy(self.lineEdit_14)
        self.label_17.setBuddy(self.dateEdit)
        self.label_18.setBuddy(self.dateEdit_2)
        self.label_19.setBuddy(self.lineEdit_16)
        self.label_1A.setBuddy(self.lineEdit_17)
        self.label_1B.setBuddy(self.lineEdit_18)
        self.label_1C.setBuddy(self.lineEdit_19)
        self.label_1D.setBuddy(self.lineEdit_1A)
        self.label_1E.setBuddy(self.lineEdit_1B)
        self.label_1F.setBuddy(self.doubleSpinBox_11)
        self.label_21.setBuddy(self.doubleSpinBox_21)
        self.label_24.setBuddy(self.comboBox_21)
        self.label_25.setBuddy(self.comboBox_22)
        self.label_27.setBuddy(self.comboBox_23)
        self.label_28.setBuddy(self.timeEdit)
        self.label_29.setBuddy(self.spinBox_25)
        self.label_2A.setBuddy(self.comboBox_24)
        self.label_2B.setBuddy(self.comboBox_25)
        self.label_2C.setBuddy(self.lineEdit_21)
        self.label_2D.setBuddy(self.spinBox_26)
        self.label_2E.setBuddy(self.lineEdit_22)
        self.label_26.setBuddy(self.comboBox_21)

        self.retranslateUi(Dialog)
        self.pButton_Cancel.clicked.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.scrollArea, self.lineEdit_11)
        Dialog.setTabOrder(self.lineEdit_11, self.lineEdit_12)
        Dialog.setTabOrder(self.lineEdit_12, self.lineEdit_13)
        Dialog.setTabOrder(self.lineEdit_13, self.lineEdit_14)
        Dialog.setTabOrder(self.lineEdit_14, self.lineEdit_15)
        Dialog.setTabOrder(self.lineEdit_15, self.dateEdit)
        Dialog.setTabOrder(self.dateEdit, self.dateEdit_2)
        Dialog.setTabOrder(self.dateEdit_2, self.lineEdit_16)
        Dialog.setTabOrder(self.lineEdit_16, self.lineEdit_17)
        Dialog.setTabOrder(self.lineEdit_17, self.lineEdit_18)
        Dialog.setTabOrder(self.lineEdit_18, self.lineEdit_19)
        Dialog.setTabOrder(self.lineEdit_19, self.lineEdit_1A)
        Dialog.setTabOrder(self.lineEdit_1A, self.lineEdit_1B)
        Dialog.setTabOrder(self.lineEdit_1B, self.doubleSpinBox_11)
        Dialog.setTabOrder(self.doubleSpinBox_11, self.doubleSpinBox_21)
        Dialog.setTabOrder(self.doubleSpinBox_21, self.doubleSpinBox_22)
        Dialog.setTabOrder(self.doubleSpinBox_22, self.comboBox_21)
        Dialog.setTabOrder(self.comboBox_21, self.doubleSpinBox_23)
        Dialog.setTabOrder(self.doubleSpinBox_23, self.comboBox_22)
        Dialog.setTabOrder(self.comboBox_22, self.doubleSpinBox_24)
        Dialog.setTabOrder(self.doubleSpinBox_24, self.comboBox_23)
        Dialog.setTabOrder(self.comboBox_23, self.timeEdit)
        Dialog.setTabOrder(self.timeEdit, self.spinBox_25)
        Dialog.setTabOrder(self.spinBox_25, self.comboBox_24)
        Dialog.setTabOrder(self.comboBox_24, self.comboBox_25)
        Dialog.setTabOrder(self.comboBox_25, self.lineEdit_21)
        Dialog.setTabOrder(self.lineEdit_21, self.spinBox_26)
        Dialog.setTabOrder(self.spinBox_26, self.lineEdit_22)
        Dialog.setTabOrder(self.lineEdit_22, self.pButton_Add)
        Dialog.setTabOrder(self.pButton_Add, self.pButton_Cancel)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "add student"))
        self.label_11.setText(_translate("Dialog", "student id"))
        self.label_12.setText(_translate("Dialog", "unique tuition\n"
"id prefix"))
        self.label_13.setText(_translate("Dialog", "first name"))
        self.label_14.setText(_translate("Dialog", "last name"))
        self.label_15.setText(_translate("Dialog", "parent name"))
        self.label_17.setText(_translate("Dialog", "start date"))
        self.label_18.setText(_translate("Dialog", "end date"))
        self.label_19.setText(_translate("Dialog", "address"))
        self.label_1A.setText(_translate("Dialog", "post code"))
        self.label_1B.setText(_translate("Dialog", "phone student"))
        self.label_1C.setText(_translate("Dialog", "email student"))
        self.label_1D.setText(_translate("Dialog", "phone parent"))
        self.label_1E.setText(_translate("Dialog", "email parent"))
        self.label_1F.setText(_translate("Dialog", "travel distance"))
        self.doubleSpinBox_11.setSuffix(_translate("Dialog", " miles"))
        self.label_16.setText(_translate("Dialog", "extra info"))
        self.label_21.setText(_translate("Dialog", "fees per hour"))
        self.doubleSpinBox_21.setPrefix(_translate("Dialog", "£ "))
        self.label_22.setText(_translate("Dialog", "discount"))
        self.doubleSpinBox_22.setPrefix(_translate("Dialog", "£ "))
        self.label_24.setText(_translate("Dialog", "extra cost 1 amount"))
        self.label_25.setText(_translate("Dialog", "extra cost 2 type"))
        self.label_27.setText(_translate("Dialog", "usual day"))
        self.label_28.setText(_translate("Dialog", "usual start time"))
        self.label_29.setText(_translate("Dialog", "usual duration"))
        self.label_2A.setText(_translate("Dialog", "usual travel\n"
"method"))
        self.label_2B.setText(_translate("Dialog", "payment method"))
        self.label_2C.setText(_translate("Dialog", "invoice email"))
        self.label_2D.setText(_translate("Dialog", "sessions per\n"
"invoice"))
        self.label_2E.setText(_translate("Dialog", "invoice to"))
        self.label_23.setText(_translate("Dialog", "extra cost 1 type"))
        self.doubleSpinBox_23.setPrefix(_translate("Dialog", "£ "))
        self.doubleSpinBox_24.setPrefix(_translate("Dialog", "£ "))
        self.label_26.setText(_translate("Dialog", "extra cost 2 amount"))
        self.pButton_Add.setText(_translate("Dialog", "Add"))
        self.pButton_Cancel.setText(_translate("Dialog", "Cancel"))

