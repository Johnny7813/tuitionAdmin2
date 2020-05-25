# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtGui, QtSql, QtWidgets
import ui_add_mileage
from custom_modview import HComboBox
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
class add_mileage_Dialog(QtWidgets.QDialog, ui_add_mileage.Ui_Dialog):
    def __init__(self, model, parent=None):
        super(add_mileage_Dialog, self).__init__(parent)
        self.setupUi(self)
        
        self.comboBox.insertItems(0, model.helperLists["help_travel_reason"])
        self.comboBox_2.insertItems(0, model.helperLists["help_vehicle"])
        
        self.comboBox.currentIndexChanged[str].connect(self.set_travel_reason)
        self.doubleSpinBox_2.valueChanged.connect(self.set_end_mileage2)
        self.comboBox.setCurrentIndex(0)
        self.comboBox_2.setCurrentIndex(1)
        self.lineEdit.setText("? tuition")
        
        #self.doubleSpinBox_1.valueChanged.connect(self.set_end_mileage1)
        self.pButton_Add.clicked.connect(self.add_mileage_record)
        self.pButton_AddMore.clicked.connect(self.add_more_mileage_record)
        self.pButton_AddNext.clicked.connect(self.add_next_mileage_record)
        
        # set internal data for this dialog
        self.model         = model
        record             = model.mileage.record(model.mileage.rowCount()-1)
        ind  = record.value(0) + 1
        val  = record.value(3)
        date = record.value(1)
        date = date.addDays(1)
        self.statusBar     = parent.statusBar()
        print("milage val=",val, "mileage ind=", ind)
        
        self.doubleSpinBox_1.setDecimals(0)
        self.doubleSpinBox_1.setSingleStep(3.0)
        self.doubleSpinBox_2.setDecimals(0)
        self.doubleSpinBox_2.setSingleStep(3.0)
        
        
        
        # init the widget of the dialog
        self.lcdNumber.setProperty("intValue", ind)
        self.doubleSpinBox_1.setProperty("value", val)
        self.doubleSpinBox_2.setProperty("value", val)
        self.record = QtSql.QSqlRecord( record );
        self.record.setValue(0, ind)
        self.dateEdit.setDate(date)
        
    
    def set_travel_reason(self, word):
        if word == "business":
           self.lineEdit.setText("? tuition")
        else :
           self.lineEdit.setText(" ")
           
           
           
    def set_end_mileage1(self, num1):
      num2 = self.doubleSpinBox_2.value()
      if num1 < num2:
          self.doubleSpinBox_2.setValue(num1)


    def set_end_mileage2(self, num1):
      num2 = self.doubleSpinBox_1.value()
      if num1 > num2:
          self.doubleSpinBox_1.setValue(num1)


    #fill the new record with the values from the dialog
    def fill_record(self):
        self.record.setValue(0, self.lcdNumber.intValue())
        self.record.setValue(1, self.dateEdit.date())
        self.record.setValue(2, self.doubleSpinBox_2.value())
        self.record.setValue(3, self.doubleSpinBox_1.value())
        self.record.setValue(4, self.comboBox.currentText())
        self.record.setValue(5, self.comboBox_2.currentText())
        self.record.setValue(6, self.lineEdit.text())

    # private add function that does part of the job
    def _add_mileage_record(self):
        
        # insert the record from the dialog into the main table (not database yet)
        if self.model.mileage.insertRecord(-1, self.record):
            self.statusBar.showMessage("Mileage successfully inserted in table", 3000)
        else:
            QtWidgets.QMessageBox.critical(self, "error", "mileage record could not be inserted in table")
            

    # initialise form again for further adding 
    def _reinit_form(self, tomorrow=0):
        
        val  = self.lcdNumber.intValue()
        val += 1
        self.lcdNumber.setProperty("intValue", val)
        
        val  = self.doubleSpinBox_1.value()
        self.doubleSpinBox_2.setProperty("value", val)
        
        text = self.comboBox.currentText()
        self.set_travel_reason(text)
        
        if tomorrow == 1 :
            #print("_reinit if executed!")
            date =  self.dateEdit.date().addDays(1)
            #date.addDays(2)
            #print("Date is ", date)
            self.dateEdit.setDate(date)
       
        
    # add the record from the dialog to the mileage_model
    def add_mileage_record(self):
        self.fill_record()
        self._add_mileage_record()
        self.accept()    
        self.done(0)


    # add the record from the dialog to the mileage_model
    def add_more_mileage_record(self):
        self.fill_record()
        self._add_mileage_record()
        self._reinit_form()


    # add the record from the dialog to the mileage_model and change the day
    def add_next_mileage_record(self):
        #print("add_next_mileage executed")
        self.fill_record()
        self._add_mileage_record()
        self._reinit_form(1)

