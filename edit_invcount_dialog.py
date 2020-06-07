# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtGui, QtSql, QtWidgets
import  ui_edit_invcount_dialog
from    settings import settings
import  re
import  sys



# multiple inheritance
# this is the invoice_counter dialog, it sets the invcounter model data
class edit_invcount_Dialog(QtWidgets.QDialog, ui_edit_invcount_dialog.Ui_Dialog):
    def __init__(self, model, parent=None):
        super(edit_invcount_Dialog, self).__init__(parent)
        self.setupUi(self)
        self.model = model
        
        inv_rec       =  self.model.invcount.record(0)
        self.counter  =  inv_rec.value("invoice_counter")
        self.prefix   =  inv_rec.value("invoice_number_prefix")
        self.rcounter =  inv_rec.value("reminder_counter")
        
        self.lineEdit.setText(self.prefix)
        self.spinBox.setValue(self.counter)
        self.spinBox_2.setValue(self.rcounter)
        self.pushButton_2.clicked.connect(self.set_model_data)
        
        
    def set_model_data(self):
        inv_rec       =  self.model.invcount.record(0)
        
        self.prefix   = self.lineEdit.text()
        self.counter  = self.spinBox.value()
        self.rcounter = self.spinBox_2.value()
        
        inv_rec.setValue("invoice_counter", self.counter)
        inv_rec.setValue("invoice_number_prefix", self.prefix)
        inv_rec.setValue("reminder_counter", self.rcounter)
        
        self.model.invcount.setRecord(0, inv_rec)
        
        #print("edit_invcount_Dialog: accept!")
        self.accept()
        
        
