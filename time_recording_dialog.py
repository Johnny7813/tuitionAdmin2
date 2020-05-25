# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtGui, QtSql, QtWidgets
import ui_time_recording
#from decimal  import *
import sys


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)



# multiple inheritance
class time_recording_Dialog(QtWidgets.QDialog, ui_time_recording.Ui_Dialog):
    def __init__(self, trec, desktop, parent=None):
        super(time_recording_Dialog, self).__init__(parent)
        self.setupUi(self)
        
        self.desktop    = desktop
        self.trec       = trec
        max_val         = round(self.trec.total/60000,2) #Decimal(self.trec.total)/Decimal(60000)
        self.doubleSpinBox.setDecimals(2)
        self.doubleSpinBox.setMaximum(max_val)
        self.doubleSpinBox.setValue(max_val)
        self.trec.wtime = float(max_val)
        self.populate_table()
        self.initWindow()
          
        # connect buttons to functions
        #self.connect(self.pushButton_4, QtCore.SIGNAL(_fromUtf8("clicked()")), self.zero_button)
        #self.connect(self.pushButton_3, QtCore.SIGNAL(_fromUtf8("clicked()")), self.continue_button)
        #self.connect(self.pushButton_2, QtCore.SIGNAL(_fromUtf8("clicked()")), self.ok_button)
        #self.connect(self.pushButton_1, QtCore.SIGNAL(_fromUtf8("clicked()")), self.cancel_button)
        #self.connect(self.doubleSpinBox, QtCore.SIGNAL(_fromUtf8("valueChanged(double)")), self.worked_time)
        
        self.pushButton_4.clicked.connect(self.zero_button)
        self.pushButton_3.clicked.connect(self.continue_button)
        self.pushButton_2.clicked.connect(self.ok_button)
        self.pushButton_1.clicked.connect(self.cancel_button)
        self.doubleSpinBox.valueChanged.connect(self.worked_time)
    
    
    
    # initiate Window with all necessary flags and correct placement
    def initWindow(self):
        self.setWindowFlags(QtCore.Qt.Popup)
        self.activateWindow()
        self.raise_()
        
        rectDesktop = self.desktop.screenGeometry()
        rectSelf    = self.frameGeometry()
        self.move( int((rectDesktop.width()-rectSelf.width())/2),
                   int((rectDesktop.height()-rectSelf.height())/2))         #   420,280)
    
    
    # all the buttons
    def zero_button(self):
        #self.trec.wtime = 0.0
        self.done(4)
    
    
    def continue_button(self):
        self.done(3)
        
    def ok_button(self):
        self.done(2)
    
    def cancel_button(self):
        self.done(1)
    
    def worked_time(self, tval):
        #print("WTime changed!")
        self.trec.wtime = tval
        
    # fill the table with data
    def populate_table(self):
        s  = self.trec.size
        self.tableWidget.setRowCount(s)
        
        for i in range(0,s):
            #word    = self.trec.stimes[i].date().toString()
            center  = QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter
            item = QtWidgets.QTableWidgetItem(self.trec.stimes[i].date().toString("dd/MM/yyyy"))
            item.setTextAlignment(center)
            self.tableWidget.setItem(i,0, item)
            item = QtWidgets.QTableWidgetItem(self.trec.stimes[i].time().toString("hh:mm:ss"))
            item.setTextAlignment(center)
            self.tableWidget.setItem(i,1, item)
            item = QtWidgets.QTableWidgetItem(self.get_time_str(i))
            item.setTextAlignment(center)
            self.tableWidget.setItem(i,2, item)
            item = QtWidgets.QTableWidgetItem(self.trec.etimes[i].time().toString("hh:mm:ss"))
            item.setTextAlignment(center)
            self.tableWidget.setItem(i,3, item)
    
    
    # produce time string from milliseconds
    def get_time_str(self, i):
        time0 = self.trec.msecs[i]
        time1 = round(time0/60000.0,2)
        time2 = "{:3.2f}".format(time1)
        return time2

