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
class view_student_counters_Dialog(QtWidgets.QDialog, ui_view_table.Ui_Dialog):
    def __init__(self, model, parent=None):
        super(view_student_counters_Dialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Student Counters")
        
        # set internal data for this dialog
        self.model         = model
        self.show_student_counters()
        
        
        
    # show student_info in a separate window
    def show_student_counters(self):
        
        # setup TableView for student_counters table
        stdcount_proxy  = QtCore.QSortFilterProxyModel(self)
        stdcount_proxy.setSourceModel(self.model.stdcount)
        self.table_view.setModel(stdcount_proxy)
        self.table_view.resizeColumnsToContents()
        self.table_view.sortByColumn (0, QtCore.Qt.AscendingOrder )
        self.table_view.setSortingEnabled(True)
        self.table_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table_view.setColumnWidth(0,160)
        self.table_view.setColumnWidth(1,110)
        self.table_view.setColumnWidth(2,110)
        self.table_view.setColumnWidth(3,110)
        self.table_view.setColumnWidth(4,180)
        
        

