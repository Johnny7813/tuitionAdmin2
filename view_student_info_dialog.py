# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtGui, QtSql, QtWidgets
import ui_view_table
from   custom_modview import *
from   Hmodel import *
from   settings import *
#from   time_recording import *
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
class view_student_info_Dialog(QtWidgets.QDialog, ui_view_table.Ui_Dialog):
    def __init__(self, model, parent=None):
        super(view_student_info_Dialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Student Info")
        
        # set internal data for this dialog
        self.model         = model
        self.show_student_info()
        
        
    # show student_info in a separate window
    def show_student_info(self):
        dateDel       = dateDelegate(self)
        yesnoDel      = comboDelegate(settings.yesno, self)
        timeDel       = timeDelegate(self)
        weekdayDel    = comboDelegate(settings.weekday, self)
        paymentDel    = comboDelegate(settings.payment, self)
        yesnoTrigDel  = ynTriggerDelegate(self)
        travelDel     = comboDelegate(settings.travel, self)
        dateTrigDel   = dateTriggerDelegate(self)
        
        # TableView for student_info
        student_proxy  = QtCore.QSortFilterProxyModel(self)
        student_proxy.setSourceModel(self.model.student)
        self.table_view.setModel(student_proxy)
        self.table_view.resizeColumnsToContents()
        self.table_view.sortByColumn (0, QtCore.Qt.AscendingOrder )
        self.table_view.setSortingEnabled(True)
        self.table_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table_view.setItemDelegateForColumn(5, dateDel)
        self.table_view.setItemDelegateForColumn(6, dateDel)
        self.table_view.setItemDelegateForColumn(17, yesnoDel)
        self.table_view.setItemDelegateForColumn(18, yesnoDel)
        self.table_view.setItemDelegateForColumn(19, weekdayDel)
        self.table_view.setItemDelegateForColumn(20, timeDel)
        self.table_view.setItemDelegateForColumn(22, travelDel)
        self.table_view.setItemDelegateForColumn(23, paymentDel)



